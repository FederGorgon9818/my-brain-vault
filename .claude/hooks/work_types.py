"""Auftrags-Typen und ihre Pflichtketten (Regel Max, 21.09.2026).

Warum es das gibt
-----------------
Bis heute gab es fuer "welcher Agent ist jetzt dran?" nur agent_triggers.py:
15 Einzelregeln, die per Regex auf Prompt/Datei/Kommando feuern und daraus eine
ERINNERUNG bauen. Das Audit vom 21.09.2026 (121 Sessions, 14 Tage) zeigt, wie gut
das traegt:

    logbook-distiller   3 Aufrufe / 30 Sessions mit Trigger ohne Aufruf
    design-guard        8          / 22
    alpha-scout         8          / 14
    verdict-auditor    14          / 16
    research-scout     30          / 25
    quant-Team         36-39       /  6   <- einzige gute Quote

Der Unterschied ist nicht der Agent, sondern die Durchsetzung: das Quant-Team ist
in den Workflows `ein-weg`/`konzept-weg` fest verdrahtet. Jede Session, die einen
Workflow gefahren hat, hat im Audit NULL Luecken. Jede Session, die nur eine
Erinnerung bekam, hat Luecken.

Daraus die Umstellung: nicht mehr 15 Wortregeln, die je nach Formulierung treffen
oder nicht (Max diktiert oft, dann trifft kein Regex sauber), sondern eine kleine
Zahl von AUFTRAGS-TYPEN. Jeder Auftrag faellt in genau einen Typ, jeder Typ hat
eine feste Kette. Der Typ wird nicht geraten, sondern in der Quittung
(receipt.py) festgeschrieben -- Regex liefert hier nur noch einen VORSCHLAG.

Diese Datei ist Daten, keine Logik. Verbraucher:
  - on_prompt.py     schlaegt beim Tippen den Typ vor und fordert die Quittung an
  - receipt.py       fuehrt die Quittung je Session (Typ, erledigte Schritte)
  - guard_chain.py   blockt Aktionen, deren Kette noch nicht gelaufen ist
  - on_stop.py       laesst die Session nicht enden, solange eine Quittung offen ist

Neuer Typ / geaenderte Kette? NUR hier. Nicht in Prosa in der CLAUDE.md.
"""

import re

# --------------------------------------------------------------------------
# Ein Typ:
#   id       kurzer Schluessel, steht so in der Quittung
#   label    Klartext fuer Hook-Meldungen
#   chain    Pflicht-Schritte. Agent-Name ODER "wf:<workflow>" (Workflow ruft die
#            Agents selbst auf und zaehlt als erledigt, wenn er lief).
#   also     empfohlen, aber nicht erzwungen (nur Hinweis)
#   gate     True  = guard_chain.py blockt die typischen Aktionen dieses Typs,
#                    solange die Kette nicht gelaufen ist
#            False = nur Ansage (Typen, deren Aktion man nicht am Tool erkennt)
#   what     was die Kette verhindert (steht in der Block-Meldung)
# --------------------------------------------------------------------------
TYPES = [
    dict(
        id="konzept", label="Konzept / grobe Edge zerlegen",
        chain=["wf:konzept-weg"],
        also=["familien-scout", "research-scout"],
        gate=True,
        what="Ohne Wege-Karte wird aus einem Konzept sofort EINE Hypothese gebaut und die "
             "anderen Preis-Wege desselben Konzepts nie gemessen (Regel 11.09.2026).",
    ),
    dict(
        id="hypothese", label="Neue Hypothese vor dem Bank-Eintrag",
        chain=["wf:ein-weg"],
        also=["variant-scout", "strategy-auditor"],
        gate=True,
        what="Ohne variant-scout kennen wir die Zahl der echten Testarten nicht (Zufallsdecke), "
             "ohne strategy-auditor geht eine kaputte Story auf die Box (Regel 01.09.2026).",
    ),
    dict(
        id="job", label="Job in die Discovery-Queue",
        chain=["pipeline-auditor"],
        also=["variant-scout"],
        gate=True,
        what="Ohne pipeline-auditor verbrennt ein methodisch kaputter Job Box-Rechenzeit "
             "(Regel 25.08.2026, Marker pipeline_ok).",
    ),
    dict(
        id="rechnen", label="Rechnen / Ergebnis auswerten",
        chain=["quant-mathematician", "quant-statistician"],
        also=["pipeline-auditor"],
        gate=False,
        what="Ohne das Quant-Team sind es Punktschaetzungen ohne Fehlerbalken: kein CI, kein "
             "Nulldrift-Zwilling, keine Multiple-Testing-Korrektur (Regel 16.08.2026).",
    ),
    dict(
        id="urteil", label="Stempel setzen (tot / gut / fertig)",
        chain=["verdict-auditor"],
        also=["quant-statistician"],
        gate=True,
        what="Ohne verdict-auditor wird eine Hypothese fuer tot erklaert, die nur schlecht "
             "gemessen wurde -- oder etwas Halbfertiges fuer fertig (Regel 30.08.2026).",
    ),
    dict(
        id="buch", label="Buch / Portfolio aendern",
        chain=["quant-mathematician", "quant-statistician", "strategy-auditor"],
        also=["session-guard"],
        gate=True,
        what="Ein Bein rein/raus ohne Marginal-Rechnung und Gegenleser aendert direkt, was "
             "live gehandelt wird (Regel 10.08.2026, Entscheidungskriterium E[Zeit bis 50k]).",
    ),
    dict(
        id="deploy", label="Deploy / Box-Sync / Live",
        chain=["engine-regression-tester"],
        also=["strategy-auditor", "box-ops"],
        gate=True,
        what="Ohne Golden-Master rechnet die Box nach dem Sync mit veraenderter Engine weiter, "
             "ohne dass es jemand merkt (Regel 27.08.2026, Marker regression_ok).",
    ),
    dict(
        id="ui", label="Oberflaeche bauen (Hub / Lab / Report)",
        chain=["design-guard"],
        also=[],
        gate=True,
        what="Ohne design-guard driftet jedes neue Element von der App-Charta weg "
             "(Regel 30.08.2026). Zweitschlechteste Quote im Audit nach logbook-distiller.",
    ),
    dict(
        id="infra", label="Box / Runner / Dienste",
        chain=["box-ops"],
        also=["session-guard"],
        gate=False,
        what="Stale-State (stehender Runner, leere Queue, stumme Telegram-Meldungen) faellt "
             "sonst erst auf, wenn er schon Tage laeuft.",
    ),
    dict(
        id="research", label="Externe Recherche",
        chain=["research-scout"],
        also=[],
        gate=True,
        what="Direkte Websuche umgeht die Cache-Pflicht: dieselbe Frage wird mehrfach bezahlt "
             "und neue Claims landen nie im Research-Cache (CLAUDE.md Token-Disziplin).",
    ),
    dict(
        id="logbuch", label="Lehre ins Strategie-Logbuch",
        chain=["logbook-distiller"],
        also=[],
        gate=True,
        what="Eine Lehre, die nur als Text im Logbuch steht, wird beim naechsten Mal wieder "
             "uebersehen. logbook-distiller fragt, ob sie als Code-Gate lebt (Regel 27.08.2026).",
    ),
    dict(
        id="meta", label="Arbeit am Prozess selbst (Hooks, Agents, Workflows, CLAUDE.md)",
        chain=["verdict-auditor"],
        also=["session-guard"],
        gate=False,
        what="Ein neu gebautes Gate gilt erst als fertig, wenn jemand geprueft hat, ob es "
             "wirklich greift -- sonst haben wir eine Regel mehr und dieselbe Luecke.",
    ),
    dict(
        id="vault", label="Vault-Pflege (Notizen, Tickets, Doku)",
        chain=[], also=[], gate=False,
        what="Keine Pflichtkette. Betrifft es das Strategie-Logbuch -> Typ `logbuch`.",
    ),
    dict(
        id="frage", label="Reine Frage / Lookup, keine Aenderung",
        chain=[], also=[], gate=False,
        what="Keine Pflichtkette. Sobald daraus Rechnen, Bauen oder ein Urteil wird: Typ neu setzen.",
    ),
]

BY_ID = {t["id"]: t for t in TYPES}

# --------------------------------------------------------------------------
# Regex nur noch als VORSCHLAG (die Entscheidung faellt in der Quittung).
# Bewusst grosszuegig: lieber zwei Vorschlaege als keiner.
# --------------------------------------------------------------------------
SUGGEST = [
    ("konzept", r"\b(vwap|fibonacci|volumenprofil|volume profile|opening range|gap-?(fill|fade)|rundzahl|"
                r"konzept|wie (k[oö]nnte|kann|w[uü]rde) man .{0,60}(handeln|traden))\b"),
    ("hypothese", r"\b(neue hypothese|hypothese[n]? (bauen|anlegen|eintragen|formulieren)|in die (hypothesen-?)?bank)\b"),
    ("job", r"(--enqueue\b|--add-job\b|\bin die queue\b|\bjob (bauen|einreihen)\b)"),
    ("rechnen", r"\b(rechne|berechne|auswerten|ausrechnen|bewerten|passquote|erwartungswert|sizing|frac\b|"
                r"backtest-?ergebnis|discovery-?(batch|lauf|auswert)|monte-?carlo|simulier)\b"),
    ("urteil", r"\b(ist (das )?tot|f[uü]r tot|abhaken|taugt (das|es)|lohnt sich das|ist (das|es) fertig|"
               r"k[oö]nnen wir das abschliessen|urteil)\b"),
    ("buch", r"\b(ins buch|aus dem buch|buch-?bein|book_state|next-?week-?buch|live-?buch|portfolio (aendern|anpassen)|"
             r"bein (rein|raus|rauswerfen|aufnehmen))\b"),
    ("deploy", r"\b(deploy|nt8|box_deploy|-sync\b|syncen|auf die box|auf die eval|live schalten|ausrollen)\b"),
    ("ui", r"\b(baue im hub|im hub|hub-?fenster|tab (bauen|umbauen)|button|oberfl[aä]che|ui\b|layout|"
           r"lab-?report|design)\b"),
    ("infra", r"\b(l[aä]uft alles|check die box|box-?status|runner (steht|h[aä]ngt|neu starten)|heartbeat|"
              r"dienst|nssm|ssh)\b"),
    ("research", r"\b(paper|ssrn|arxiv|studie[n]?|literatur|recherchier|websuche|was sagt die forschung|"
                 r"such mal im (netz|web|internet))\b"),
    ("logbuch", r"\b(ins logbuch|logbuch-?eintrag|lehre|vorfall|als lehre)\b"),
    ("meta", r"\b(hook|agent (bauen|anlegen|einf[uü]hren)|workflow (bauen|anlegen)|claude\.?md|"
             r"pr[uü]fprozess|prozess (bauen|verbessern|entwickeln)|regel (einf[uü]hren|anlegen))\b"),
    ("vault", r"\b(daily note|notiz|ticket|doku|dokumentier|aufr[aä]umen|einsortieren)\b"),
]

_SUGGEST_C = [(tid, re.compile(rx, re.I)) for tid, rx in SUGGEST]


def suggest(text):
    """Typ-Vorschlaege fuer einen Prompt, Reihenfolge = Fundstelle im Text.
    Liefert [(type_id, snippet)] -- nie eine Entscheidung, nur ein Vorschlag."""
    hits = []
    if not text:
        return hits
    for tid, rx in _SUGGEST_C:
        m = rx.search(text)
        if m:
            s = max(0, m.start() - 20)
            hits.append((tid, re.sub(r"\s+", " ", text[s:m.end() + 20]).strip()))
    return hits


def chain_of(tid):
    t = BY_ID.get(tid)
    return list(t["chain"]) if t else []


def label_of(tid):
    t = BY_ID.get(tid)
    return t["label"] if t else tid


def what_of(tid):
    t = BY_ID.get(tid)
    return t["what"] if t else ""


def has_gate(tid):
    t = BY_ID.get(tid)
    return bool(t and t.get("gate"))


def step_is_workflow(step):
    return step.startswith("wf:")


def step_name(step):
    return step[3:] if step_is_workflow(step) else step


def overview():
    """Kompakte Tabelle fuer Hook-Meldungen und `receipt.py --types`."""
    rows = []
    for t in TYPES:
        chain = " -> ".join(step_name(s) for s in t["chain"]) or "(keine Kette)"
        rows.append(f"  {t['id']:<10} {t['label']:<46} {chain}")
    return "\n".join(rows)
