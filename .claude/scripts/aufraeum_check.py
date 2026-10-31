"""Aufraeum-Check fuer C:\\Claude (Regel Max 31.10.2026, Ablage-Workflow in C:\\Claude\\README.md).

Meldet, was liegen geblieben ist. Ohne --apply wird nichts angefasst.
  python aufraeum_check.py            Bericht, schreibt die Vorschlagsliste
  python aufraeum_check.py --ticket   dasselbe als Backlog-Ticket (Board infra), sonntags per Task "MaxLab Aufraeum-Check"
  python aufraeum_check.py --apply    nach Max' OK: genau die Vorschlagsliste (nicht neu sammeln), nur verschieben
Fertige Projekt-Notizen und lose Dateien werden nur gemeldet, die sortiert Claude nach Blick auf den Inhalt.

Haertung nach dem Gegenleser (verdict-auditor 31.10.): .bak/.log nur, wenn kein Code, keine Daten-JSON und kein
Scratch-Skript den Namen nennt; Worktrees nur gemergt (gemessen IM Worktree), sauber, ungesperrt (angepinnte sind
per `git worktree lock` geschuetzt); vor dem Ticket der Box-Stand per inbox_tool --pull (AP-Nummern); git ohne Fenster.
"""
import argparse, json, os, re, subprocess, sys, time
from datetime import date, datetime
from pathlib import Path

ROOT = Path(r"C:\Claude")
VAULT = ROOT / "My Brain"
TD = ROOT / "projekte" / "trading-data"
ENG = TD / "engine"
ARCH = ENG / "archiv"
VORSCHLAG = ARCH / "aufraeum_vorschlag.json"
NOW = time.time()
NOWIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)
TAGE = lambda t: (NOW - t) / 86400

KNOWN_ROOT = {"README.md", "My Brain", "projekte", "content", "buero", "archiv", "_umzug"}
KNOWN_VAULT = {"Inbox", "Projekte", "Bereiche", "Ressourcen", "Daily Notes", "Archiv", "Anhänge", "Kontext",
               "CLAUDE.md", "Home.md", ".claude", ".obsidian", ".claudian", ".git", ".gitignore", ".mcp.json",
               ".gitattributes", ".trash"}
KNOWN_TD = {"README.md", ".gitignore", ".git", "engine", "exported_data", "exported_data_nt8", "exported_data_xau",
            "orderflow", "multicharts", "Strategy Lab", "tools", "archiv", "secrets", "mnq_falsification.txt"}


def git(*a, cwd=VAULT):
    return subprocess.run(["git", *a], capture_output=True, text=True, cwd=str(cwd), creationflags=NOWIN)


def newest(p):
    m = p.stat().st_mtime
    for dp, dn, fn in os.walk(p):
        for f in fn:
            try:
                m = max(m, os.stat(os.path.join(dp, f)).st_mtime)
            except OSError:
                pass
    return m


def verweise_text():
    """Alles, was eine Datei oder einen Scratch-Ordner noch braucht: Engine-Code und -Daten-JSON, Scratch-Skripte
    (auch untereinander), Discovery-Inbox/Jobs, Tickets, CLAUDE.md, Hooks/Skills/Agents, aktive Notizen."""
    teile = []
    globs = [(ENG, "*.py"), (ENG, "*.ps1"), (ENG, "*.json"), (ENG / "discovery", "*.py"), (ENG / "discovery", "*.ps1"),
             (ENG / "discovery", "inbox.json"), (ENG / "discovery" / "jobs_proposed", "*.json"),
             (ENG / "discovery" / "scout_reports", "*.md"), (ENG / "konten", "*.py"), (TD / "tools", "*.py"),
             (VAULT, "CLAUDE.md"), (VAULT / "Projekte", "**/*.md"), (VAULT / "Bereiche", "*.md"), (VAULT / "Ressourcen", "*.md")]
    for d in ENG.glob("_scratch*"):
        if d.is_dir():
            globs += [(d, "**/*.py"), (d, "**/*.ps1"), (d, "**/*.json"), (d, "**/*.md")]
    for base, pat in globs:
        for p in base.glob(pat):
            try:
                if p.is_file() and p.stat().st_size < (1_000_000 if base.name.startswith("_scratch") else 5_000_000):
                    teile.append(p.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                pass
    for p in (VAULT / ".claude").rglob("*"):
        if p.is_file() and "worktrees" not in p.parts and p.suffix in (".py", ".md", ".js", ".json"):
            teile.append(p.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(teile)


def worktree_kandidaten():
    """Gemergt (master..HEAD im Worktree selbst gemessen), sauber inkl. unversionierter Dateien,
    nicht gesperrt, Metadaten vorhanden und seit 2 Tagen unberuehrt."""
    out, cur = [], {}
    for l in git("worktree", "list", "--porcelain").stdout.splitlines() + [""]:
        if not l:
            if cur.get("worktree") and "/.claude/worktrees/" in cur["worktree"]:
                out.append(cur)
            cur = {}
            continue
        k, _, v = l.partition(" ")
        cur[k] = v or True
    wts = []
    for c in out:
        wt = Path(c["worktree"])
        if c.get("locked") or c.get("prunable") or not wt.exists():
            continue
        meta = VAULT / ".git" / "worktrees" / wt.name
        stamps = [(meta / f).stat().st_mtime for f in ("HEAD", "index") if (meta / f).exists()]
        if not stamps or TAGE(max(stamps)) <= 2:
            continue
        if git("rev-list", "--count", "master..HEAD", cwd=wt).stdout.strip() != "0":
            continue
        if git("status", "--porcelain", cwd=wt).stdout.strip():
            continue
        wts.append(wt)
    return wts


def sammeln():
    txt = verweise_text()
    f = {"worktrees": worktree_kandidaten()}
    f["scratch"] = [d for d in ENG.iterdir() if d.is_dir() and d.name.startswith("_scratch")
                    and TAGE(newest(d)) > 21 and d.name not in txt]
    f["bak"] = [p for p in ENG.iterdir() if p.is_file() and ".bak" in p.name and TAGE(p.stat().st_mtime) > 14 and p.name not in txt]
    f["logs"] = [p for p in ENG.glob("*.log") if TAGE(p.stat().st_mtime) > 30 and p.name not in txt]
    fertig = []
    for p in (VAULT / "Projekte").rglob("*.md"):
        m = re.search(r"^status:\s*(.+)$", p.read_text(encoding="utf-8", errors="replace")[:1500], re.M)
        if m and re.match(r"(fertig|erledigt|abgeschlossen)\b", m.group(1).strip().lower()):
            fertig.append(p)
    f["projekte_fertig"] = fertig
    lose = [ROOT / n for n in os.listdir(ROOT) if n not in KNOWN_ROOT]
    lose += [VAULT / n for n in os.listdir(VAULT) if n not in KNOWN_VAULT]
    lose += [TD / n for n in os.listdir(TD) if n not in KNOWN_TD and not n.startswith(("nt8_staging_", "_ap"))]
    f["lose"] = lose
    return f


NAMEN = {"worktrees": "Worktrees gemergt+sauber (entfernen)", "scratch": "Scratch >21 Tage, unbenutzt (-> engine\\archiv\\scratch)",
         "bak": ".bak >14 Tage, unbenutzt (-> engine\\archiv\\backups)", "logs": "Logs >30 Tage, unbenutzt (-> engine\\archiv\\logs)",
         "projekte_fertig": "Projekt-Notizen mit Status fertig (Claude prueft, dann Archiv/)",
         "lose": "Lose/unbekannte Eintraege (Ablage-Workflow anwenden)"}


def bericht(f):
    z = [f"Aufraeum-Check {date.today().isoformat()}"]
    for k, label in NAMEN.items():
        v = f[k]
        z.append(f"- {label}: {len(v)}" + (": " + ", ".join(p.name for p in v) if v else ""))
    return "\n".join(z), sum(len(v) for v in f.values())


def vorschlag_schreiben(f):
    ARCH.mkdir(parents=True, exist_ok=True)
    VORSCHLAG.write_text(json.dumps({"datum": datetime.now().isoformat(timespec="seconds"),
                                     **{k: [str(p) for p in f[k]] for k in ("worktrees", "scratch", "bak", "logs")}},
                                    ensure_ascii=False, indent=1), encoding="utf-8")


def anwenden():
    """Nur die Vorschlagsliste, die Max gesehen hat. Jeder Eintrag wird vor dem Verschieben neu geprueft."""
    if not VORSCHLAG.exists():
        sys.exit("Keine Vorschlagsliste. Erst den Bericht laufen lassen und Max zeigen.")
    v = json.loads(VORSCHLAG.read_text(encoding="utf-8"))
    if TAGE(datetime.fromisoformat(v["datum"]).timestamp()) > 14:
        sys.exit("Vorschlagsliste aelter als 14 Tage. Bericht neu laufen lassen und Max zeigen.")
    aktuell = sammeln()
    gilt = {k: {str(p) for p in aktuell[k]} for k in ("worktrees", "scratch", "bak", "logs")}
    log = ARCH / "aufraeum_log.jsonl"
    n = 0
    for wt in v["worktrees"]:
        if wt in gilt["worktrees"] and git("worktree", "remove", wt).returncode == 0:   # ohne --force
            n += 1
    for k, ziel in (("scratch", "scratch"), ("bak", "backups"), ("logs", "logs")):
        for s in v[k]:
            p = Path(s)
            nach = ARCH / ziel / p.name
            if s not in gilt[k] or not p.exists() or nach.exists():
                continue
            nach.parent.mkdir(parents=True, exist_ok=True)
            os.rename(p, nach); n += 1
            with log.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps({"t": date.today().isoformat(), "von": s, "nach": str(nach)}, ensure_ascii=False) + "\n")
    git("worktree", "prune")
    VORSCHLAG.rename(VORSCHLAG.with_name(f"aufraeum_vorschlag_erledigt_{date.today().isoformat()}.json"))
    return n


def ticket(text, summe):
    """Wie auto_check: erst Box-Stand holen (Box ist Quelle der Wahrheit fuer tasks.json, sonst AP-Kollision)."""
    if not os.environ.get("TICKET_DIR"):
        r = subprocess.run([sys.executable.replace("pythonw.exe", "python.exe"), str(ENG / "discovery" / "inbox_tool.py"), "--pull", "--unseen"],
                           capture_output=True, text=True, timeout=600, cwd=str(ENG), creationflags=NOWIN)
        if r.returncode != 0:
            (ARCH / "aufraeum_letzter_bericht.txt").write_text(text + "\n\nKein Ticket: Box-Pull fehlgeschlagen.\n", encoding="utf-8")
            return None
    sys.path.insert(0, str(ENG))
    import ticket_lib as TL
    kw = date.today().isocalendar()
    return TL.auto_ticket(f"aufraeumen:{kw[0]}-W{kw[1]:02d}", "infra", "gelb",
                          f"Aufraeum-Bericht KW{kw[1]:02d}: {summe} Punkte in C:\\Claude",
                          why="Woechentlicher Aufraeum-Check (Regel Max 31.10.2026). Verschoben wird erst nach Max' OK.",
                          note_text=text[:1800],
                          guide=["Claude: python \"C:\\Claude\\My Brain\\.claude\\scripts\\aufraeum_check.py\" laufen lassen und Bericht zeigen",
                                 "Nach Max' OK: --apply (verschiebt genau die gezeigte Liste); fertige Projekte und lose Dateien sortiert Claude nach dem Ablage-Workflow",
                                 "Ticket danach loeschen"],
                          source="aufraeum_check.py", who="claude")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--ticket", action="store_true")
    a = ap.parse_args()
    if a.apply:
        print("verschoben/entfernt:", anwenden())
        return
    f = sammeln()
    text, summe = bericht(f)
    vorschlag_schreiben(f)
    print(text)
    if a.ticket and summe:
        print("Ticket:", ticket(text, summe))


if __name__ == "__main__":
    main()
