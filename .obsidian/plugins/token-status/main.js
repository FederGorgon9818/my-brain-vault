/*
 * Token Status - minimaler Obsidian-Statusleisten-Indikator fuer Claude-Token-Verbrauch.
 *
 * Prinzip wie die echte Claude-Code-Statusline: nur Text, keine Bilder/Heatmap.
 * Reagiert "live" ueber einen Datei-Watcher (fs.watch) auf den Projekt-Log-Ordner,
 * nicht per festem Polling-Intervall - sobald Claude Code (Claudian) eine neue
 * Zeile in ~/.claude/projects/<vault>/*.jsonl schreibt, wird sofort neu berechnet.
 *
 * Gleiche Datenquelle/Definition wie Token-Tracker-App (server.py) und der
 * Skill token-usage (chat_report.py) - config.json wird geteilt, keine zweite
 * Wahrheit ueber Budgets.
 *
 * Bekannte Vereinfachungen (bewusst, siehe "Simplex beats Komplex"):
 * - Liest bei jedem Log-Update ALLE .jsonl-Dateien im Projektordner komplett neu
 *   (kein inkrementelles Tailen). Bei sehr grossen Logs (>>10 MB) kann das kurze
 *   Ruckler verursachen - bislang kein Problem bei den beobachteten Dateigroessen.
 * - Zaehlt KEINE Subagent-Sidechain-Unterordner mit (nur die Haupt-Session-Dateien
 *   direkt im Projektordner). Fuer den schnellen Blick in der Statusleiste okay,
 *   die ausfuehrlichen Reports (Skill/Dashboard) sind weiterhin die genaue Quelle.
 * - "5h"-Fenster ist ein einfaches rollierendes Zeitfenster, nicht die exakte
 *   Block-Logik mit fixem Stundenanker wie im Dashboard. Kann leicht abweichen.
 */

const { Plugin } = require("obsidian");
const fs = require("fs");
const path = require("path");
const os = require("os");

const LOG_ROOT = path.join(os.homedir(), ".claude", "projects");
const CONFIG_PATH = "C:\\Users\\maxlk\\Projects\\token-tracker\\config.json";
const DEFAULT_CFG = {
  block_hours: 5,
  block_token_budget: 20000000,
  weekly_token_budget: 300000000,
  count_cache_read: false,
  port: 8712,
};

function slugify(p) {
  return p.replace(/[^a-zA-Z0-9]/g, "-");
}

function loadConfig() {
  try {
    const raw = JSON.parse(fs.readFileSync(CONFIG_PATH, "utf8"));
    return Object.assign({}, DEFAULT_CFG, raw);
  } catch (e) {
    return Object.assign({}, DEFAULT_CFG);
  }
}

function fmt(n) {
  return Math.round(n).toLocaleString("de-DE");
}

module.exports = class TokenStatusPlugin extends Plugin {
  async onload() {
    this.cfg = loadConfig();
    this.projectDir = null;
    this.watcher = null;
    this.debounceTimer = null;

    this.statusEl = this.addStatusBarItem();
    this.statusEl.addClass("token-status-item");
    this.statusEl.setText("🎫 lade...");
    this.statusEl.addEventListener("click", () => {
      try {
        require("electron").shell.openExternal(`http://localhost:${this.cfg.port}`);
      } catch (e) {
        // kein Electron-Zugriff oder Dashboard laeuft nicht - einfach ignorieren
      }
    });

    try {
      const basePath = this.app.vault.adapter.basePath;
      this.projectDir = path.join(LOG_ROOT, slugify(basePath));
    } catch (e) {
      console.error("[token-status] Vault-Pfad nicht auflösbar:", e);
    }

    console.log("[token-status] Plugin geladen. Log-Ordner:", this.projectDir);

    this.refresh(false);
    this.setupWatcher();
  }

  onunload() {
    if (this.watcher) {
      try {
        this.watcher.close();
      } catch (e) {
        /* egal */
      }
    }
    if (this.debounceTimer) clearTimeout(this.debounceTimer);
  }

  setupWatcher() {
    if (!this.projectDir || !fs.existsSync(this.projectDir)) {
      this.statusEl.setText("🎫 kein Log-Ordner gefunden");
      return;
    }
    try {
      this.watcher = fs.watch(this.projectDir, { persistent: false }, (eventType, filename) => {
        if (filename && !filename.endsWith(".jsonl")) return;
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => this.refresh(true), 300);
      });
    } catch (e) {
      console.error("[token-status] fs.watch fehlgeschlagen:", e);
    }
  }

  refresh(pulse) {
    try {
      const stats = this.computeStats();
      this.statusEl.setText(
        `🎫 ${fmt(stats.todayBillable)} heute · 5h ${stats.pct5h.toFixed(1)}%`
      );
      this.statusEl.setAttribute(
        "title",
        `Heute: ${fmt(stats.todayBillable)} Tokens\n` +
          `Rollierendes 5h-Fenster: ${fmt(stats.used5h)} / ${fmt(this.cfg.block_token_budget)}\n` +
          `Klick: Dashboard oeffnen (python server.py muss laufen)`
      );
      console.log("[token-status] aktualisiert:", stats);
      if (pulse) this.pulse();
    } catch (e) {
      console.error("[token-status] refresh fehlgeschlagen:", e);
      this.statusEl.setText("🎫 Fehler (Konsole prüfen)");
    }
  }

  pulse() {
    this.statusEl.addClass("token-status-pulse");
    setTimeout(() => this.statusEl.removeClass("token-status-pulse"), 500);
  }

  computeStats() {
    const cfg = this.cfg;
    const now = Date.now();
    const todayKey = new Date().toDateString();
    const windowStart = now - cfg.block_hours * 3600 * 1000;

    let todayBillable = 0;
    let used5h = 0;
    const seen = new Set();

    if (!this.projectDir || !fs.existsSync(this.projectDir)) {
      return { todayBillable, used5h, pct5h: 0 };
    }

    const files = fs
      .readdirSync(this.projectDir, { withFileTypes: true })
      .filter((e) => e.isFile() && e.name.endsWith(".jsonl"))
      .map((e) => path.join(this.projectDir, e.name));

    for (const file of files) {
      let text;
      try {
        text = fs.readFileSync(file, "utf8");
      } catch (e) {
        continue;
      }
      const lines = text.split("\n");
      for (const line of lines) {
        if (!line.includes('"usage"')) continue;
        let o;
        try {
          o = JSON.parse(line);
        } catch (e) {
          continue;
        }
        const msg = o.message || {};
        const usage = msg.usage;
        if (!usage) continue;
        const model = msg.model || "";
        if (!model || model === "<synthetic>") continue;
        const key = msg.id || o.uuid;
        if (!key || seen.has(key)) continue;
        seen.add(key);

        const ts = Date.parse(o.timestamp);
        if (Number.isNaN(ts)) continue;

        const billable =
          (usage.input_tokens || 0) +
          (usage.output_tokens || 0) +
          (usage.cache_creation_input_tokens || 0) +
          (cfg.count_cache_read ? usage.cache_read_input_tokens || 0 : 0);

        if (new Date(ts).toDateString() === todayKey) todayBillable += billable;
        if (ts >= windowStart) used5h += billable;
      }
    }

    return { todayBillable, used5h, pct5h: (100 * used5h) / cfg.block_token_budget };
  }
};
