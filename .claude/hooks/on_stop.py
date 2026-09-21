"""Stop: Session darf nicht enden, solange offene Pflichten stehen.

1. book_state*.json geaendert, aber kein push-next seitdem (nur mit lokalem
   Engine-Ordner, also PC/Box).
2. Regel Max, 09.09.2026: diese Session hat Dateien geaendert, aber die heutige
   Daily Note nicht angefasst - Kontextverlust soll "quasi nicht moeglich" sein.
   Greift ueberall (auch Laptop ohne Engine-Ordner), da die Daily Note die
   geraeteuebergreifende Garantie ist (Git-synchronisiert, anders als die
   lokalen Session-Transkripte).

Einmal blocken, dann nur erinnern -- JE BEFUND UND SESSION. `stop_hook_active`
allein reicht dafuer nicht: es gilt nur fuer den Stopp direkt nach dem Block, beim
naechsten Prompt blockte derselbe Befund wieder (Vorfall 16.09.2026, viermal in
Folge). Deshalb merkt sich der Hook je session_id, welche Befunde schon geblockt
haben (Temp-Ordner, geraeteunabhaengig).
"""
from _common import *  # noqa
import hashlib
import json as _json
import tempfile

SEEN_DIR = Path(tempfile.gettempdir()) / "claude_stop_blocks"


def _seen_file(inp):
    sid = str(inp.get("session_id") or "")
    return SEEN_DIR / f"{hashlib.md5(sid.encode()).hexdigest()}.json" if sid else None


def _load_seen(inp):
    f = _seen_file(inp)
    try:
        return set(_json.loads(f.read_text(encoding="utf-8"))) if f and f.is_file() else set()
    except Exception:
        return set()


def _save_seen(inp, keys):
    f = _seen_file(inp)
    if not f:
        return
    try:
        SEEN_DIR.mkdir(parents=True, exist_ok=True)
        f.write_text(_json.dumps(sorted(keys)), encoding="utf-8")
    except Exception:
        pass


def main():
    inp = read_input()
    issues = []

    # --- 1. Buch geaendert, nicht gepusht ------------------------------------
    if ENGINE:
        stale = book_newer_than_marker("push_next_at")
        if stale:
            issues.append(("book:" + ",".join(sorted(stale)),
                f"{', '.join(stale)} wurde geaendert, aber seitdem kein `inbox_tool.py --push-next` "
                f"(letzter Push {fmt_age(marker_time('push_next_at'))}). Regel 21.08.2026: "
                "funded_finalize (+--next) laufen lassen und pushen, sonst promotet die Box in einen alten Stand. "
                "Wenn der Push bewusst nicht gewollt ist (Datei nur neu formatiert o.ae.): "
                "`python .claude/hooks/mark.py push_next_at` setzt den Marker von Hand."
            ))

    # --- 2. Diese Session hat geaendert, Daily Note nicht --------------------
    tp = inp.get("transcript_path")
    if tp and Path(tp).is_file():
        meta = scan_transcript_light(Path(tp))
        if meta["made_changes"] and meta["first_activity"]:
            today = VAULT / "Daily Notes" / f"{time.strftime('%Y-%m-%d')}.md"
            note_t = mtime(today)
            if note_t is None or note_t < meta["first_activity"]:
                issues.append((f"daily:{today.name}",
                    f"diese Session hat Dateien geaendert, aber die heutige Daily Note "
                    f"({today.name}) wurde seitdem nicht angefasst. Regel 09.09.2026: kurz "
                    "nachtragen was gemacht/entschieden wurde (Stichpunkte reichen), danach "
                    "erneut beenden. Betrifft nur diese Session - eine andere Session kann die "
                    "Note zwischenzeitlich schon aktualisiert haben, dann greift das hier nicht."
                ))

    # --- 3. Trigger gefeuert, Agent nie aufgerufen (Regel Max, 11.09.2026) --
    # Heuristik aus agent_triggers.py, gleiche Quelle wie der Prompt-Hook und das
    # Audit-Skript. Einmal blocken, dann nur erinnern: bewusst ausgelassen heisst,
    # den Grund in der Antwort nennen und erneut beenden.
    if tp and Path(tp).is_file():
        try:
            sys.path.insert(0, str(VAULT / ".claude" / "scripts"))
            from agent_usage_audit import scan, gaps
            s = scan(Path(tp))
            found = gaps(s) if s["turns"] else []
            # Nur Trigger, die im Prompt oder an Dateien/Kommandos hingen (nicht bloss im Antworttext),
            # sonst erinnert der Hook an jede beilaeufige Erwaehnung.
            strong = [g for g in found if any(sc in ("user", "file", "bash", "tool") for sc in g[3])]
            if strong:
                parts = [f"{'/'.join(m)} ({tid}: \"{snip[:60]}\")" for tid, m, n, sc, why, snip in strong[:5]]
                key = "agent:" + ",".join(sorted(f"{g[0]}={'/'.join(g[1])}" for g in strong))
                issues.append((key,
                    "diese Session hat Einschalt-Regeln getroffen, den Agent aber nie aufgerufen: "
                    + "; ".join(parts)
                    + ". Regel 11.09.2026: entweder jetzt einschalten oder in der Antwort in einem Satz sagen, "
                    "warum er hier nicht passt, dann erneut beenden."
                ))
        except Exception:
            pass

    # --- 4. Prozess-Quittung offen (Regel Max, 21.09.2026) ------------------
    # Punkt 3 oben ist Heuristik ueber Transkript-Regex und trifft bei diktierten
    # Prompts oft daneben. Die Quittung ist die deterministische Variante: welcher
    # Auftrags-Typ, welche Pflichtkette, was davon lief. Greift nur, wenn die
    # Session ueberhaupt gearbeitet hat -- reine Frage-Antwort-Sessions bleiben frei.
    if tp and Path(tp).is_file():
        try:
            sys.path.insert(0, str(VAULT / ".claude" / "hooks"))
            import receipt as R
            import work_types as WT
            rec = R.load(inp.get("session_id"))
            meta4 = scan_transcript_light(Path(tp))
            worked = meta4["made_changes"]
            if rec and worked:
                sid = rec["sid"]
                if not rec.get("type"):
                    issues.append((f"receipt-type:{sid}",
                        f"diese Session hat gearbeitet, aber der Auftrags-Typ wurde nie "
                        f"festgeschrieben (Quittung {sid}). Regel 21.09.2026: ohne Typ steht "
                        f"keine Pflichtkette fest und niemand kann hinterher pruefen, ob der "
                        f"richtige Ablauf lief. Nachtragen: "
                        f"`python .claude/hooks/receipt.py --sid {sid} --type <typ>` "
                        f"(Liste: --types), dann erneut beenden."
                    ))
                else:
                    miss4 = R.missing_steps(rec, tp)
                    if miss4:
                        names4 = ", ".join(WT.step_name(s) for s in miss4)
                        issues.append((f"receipt-chain:{sid}:{names4}",
                            f"Auftrags-Typ `{rec['type']}` ({WT.label_of(rec['type'])}), aber die "
                            f"Pflichtkette ist offen: {names4}. {WT.what_of(rec['type'])} "
                            f"Entweder jetzt laufen lassen, oder mit Grund auslassen: "
                            f"`python .claude/hooks/receipt.py --sid {sid} "
                            f"--skip {WT.step_name(miss4[0])} --why \"<ein Satz>\"`."
                        ))
        except Exception:
            pass

    if not issues:
        sys.exit(0)
    msg = "Hook: " + " | ".join(t for _, t in issues)
    seen = _load_seen(inp)
    fresh = [k for k, _ in issues if k not in seen]
    if inp.get("stop_hook_active") or not fresh:
        out({"systemMessage": msg})
        sys.exit(0)
    _save_seen(inp, seen | {k for k, _ in issues})
    block_stop(msg)


run(main)
