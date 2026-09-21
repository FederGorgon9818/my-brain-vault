export const meta = {
  name: 'kette',
  description: 'Faehrt die Pflichtkette eines Auftrags-Typs deterministisch ab (Rechner parallel, Gegenleser danach mit deren Ergebnissen)',
  whenToUse: 'Sobald die Quittung (receipt.py) einen Auftrags-Typ mit Pflichtkette traegt und die Kette noch offen ist: rechnen, urteil, buch, deploy, ui, job, research, infra, logbuch, meta. Fuer `konzept` und `hypothese` gibt es die eigenen Workflows konzept-weg / ein-weg. args: {type, task, context?}',
  phases: [
    { title: 'Rechner', detail: 'Alle unabhaengigen Kettenglieder parallel (Quant-Team, Auditoren, Tester)' },
    { title: 'Gegenleser', detail: 'strategy-auditor / verdict-auditor zuletzt, MIT den Ergebnissen der ersten Phase' },
  ],
}

// ---------------------------------------------------------------------------
// Regel Max, 21.09.2026 (Typ-Router). Hintergrund:
//
// Das Agent-Audit vom 21.09. (121 Sessions, 14 Tage) hat gezeigt: Agents, die nur
// per Text-Erinnerung angefordert wurden, liefen in 9-56 % der Faelle. Agents, die
// in einem Workflow fest verdrahtet sind (ein-weg, konzept-weg), liefen zu 100 % --
// jede Session mit Workflow hatte NULL Luecken im Audit.
//
// Dieser Workflow zieht dieselbe Verdrahtung fuer alle uebrigen Typen ein, ohne je
// Typ ein eigenes Skript zu brauchen. Die Ketten spiegeln .claude/hooks/work_types.py;
// dort ist die Quelle der Wahrheit (der Hook blockt danach), hier nur die Ausfuehrung.
// Aendert sich eine Kette: ZUERST work_types.py, dann diese Tabelle nachziehen.
//
// Das Ordnungsprinzip: Rechner parallel, Gegenleser zuletzt. Ein Gegenleser, der die
// Zahlen der Rechner nicht sieht, prueft nur die Story im luftleeren Raum -- genau der
// Fehler, den die alte Reihenfolge "Agent XY halt irgendwann" produziert hat.
// ---------------------------------------------------------------------------

const CHAINS = {
  rechnen: ['quant-mathematician', 'quant-statistician'],
  urteil: ['verdict-auditor'],
  buch: ['quant-mathematician', 'quant-statistician', 'strategy-auditor'],
  deploy: ['engine-regression-tester'],
  ui: ['design-guard'],
  job: ['pipeline-auditor'],
  research: ['research-scout'],
  infra: ['box-ops'],
  logbuch: ['logbook-distiller'],
  meta: ['verdict-auditor'],
}

// Gegenleser laufen zuletzt und bekommen die Ergebnisse der ersten Phase mit.
const REVIEWERS = ['strategy-auditor', 'verdict-auditor']

const TYPE = String((args && args.type) || '').trim()
const TASK = String((args && args.task) || '').trim()
const CONTEXT = String((args && args.context) || '').trim()

if (!TYPE) {
  return { error: 'args.type fehlt. Erwartet einen Auftrags-Typ aus work_types.py, z.B. {type: "rechnen", task: "..."}' }
}
if (TYPE === 'konzept' || TYPE === 'hypothese') {
  return {
    error: `Typ \`${TYPE}\` hat einen eigenen Workflow: ` +
      (TYPE === 'konzept' ? '`konzept-weg` (familien-scout -> verdict-auditor -> research-scout -> ein-weg).'
                          : '`ein-weg` (variant-scout je Hypothese -> strategy-auditor Batch).'),
  }
}
const CHAIN = CHAINS[TYPE]
if (!CHAIN) {
  return { error: `Unbekannter oder ketten-loser Typ \`${TYPE}\`. Mit Kette: ${Object.keys(CHAINS).join(', ')}.` }
}
if (!TASK || TASK.length < 15) {
  // Ohne konkrete Aufgabe raet jeder Agent, was gemeint ist -- dann ist die Kette
  // zwar formal gelaufen, hat aber nichts geprueft. Das waere schlimmer als keine Kette.
  return { error: 'args.task fehlt oder ist zu kurz. Beschreib in 1-3 Saetzen, was konkret geprueft/gerechnet werden soll.' }
}

const ENGINE_NOTE = [
  'Engine-Pfad: C:\\Users\\maxlk\\Projects\\trading-data\\engine (PC).',
  'Fehlt der Pfad, per `ssh Administrator@100.127.89.9` auf der Box arbeiten (gleicher Pfad dort).',
  'Vault: Bereiche/, Projekte/, Ressourcen/ -- nur gezielte Greps, nie volle Logs oder results/*.json.',
].join(' ')

const ZIEL = [
  'Entscheidungskriterium seit 18.09.2026: verkuerzt oder verlaengert es E[Zeit bis 50.000 $ Eigenkapital aus Payouts],',
  'bei begrenzter Auslage? Nicht Einzel-Edge, nicht Sharpe. Nulldrift-Zwilling und Auslage p90 gehoeren zu jeder Zahl (Logbuch #106).',
].join(' ')

const STEP_BRIEF = {
  'quant-mathematician': 'Struktur und Formeln: geschlossene oder semi-analytische Antwort, numerisch gegengerechnet.',
  'quant-statistician': 'Beweislage und Unsicherheit: CIs (Block-Bootstrap), DSR/PSR/PBO, n_trials, Regime-Splits, Nulldrift-Kontrolle. Zahlen mit Fehlerbalken, keine Punktschaetzungen.',
  'strategy-auditor': 'Adversarialer Gegenleser: Why kausal, Look-ahead, Anatomie vollstaendig, zu gut um wahr zu sein.',
  'verdict-auditor': 'Traegt die Beweislage den Stempel? Welche Tests fehlen, was waere rational der naechste Schritt?',
  'pipeline-auditor': 'Methodisch sauber? Wiederholen wir einen bekannten Fehler? Setzt bei "keine Blocker" den Marker pipeline_ok.',
  'engine-regression-tester': 'Golden-Master gegen die eingefrorene Referenz. Bei "Sync frei" den Marker regression_ok setzen.',
  'design-guard': 'Gegen die App-Charta in Ressourcen/Design-System (Hub & Apps).md: sieht es aus wie der Rest, Tokens statt loser Werte.',
  'research-scout': 'ZUERST Research-Cache + Strategie-Logbuch greppen, erst danach Web. Neue Claims zurueck in den Cache.',
  'box-ops': 'Rundgang per SSH: Runner, Queue, Buch-Sync, RiskGuard/Telegram, NT8. Stale-State melden.',
  'logbook-distiller': 'Lebt die Lehre als Code-Gate oder nur als Text? Wenn nur Text: wo waere das Gate.',
}

const STEP_SCHEMA = {
  type: 'object',
  properties: {
    verdict: { type: 'string', description: 'Dein Kern-Urteil in einem Satz' },
    findings: {
      type: 'array',
      description: 'Die tragenden Befunde, wichtigster zuerst',
      items: {
        type: 'object',
        properties: {
          point: { type: 'string' },
          evidence: { type: 'string', description: 'Worauf stuetzt sich das (Zahl, Datei:Zeile, Logbuch-Nummer)' },
          severity: { type: 'string', enum: ['blocker', 'wichtig', 'hinweis'] },
        },
        required: ['point', 'evidence', 'severity'],
      },
    },
    open: { type: 'array', items: { type: 'string' }, description: 'Was offen bleibt / nicht geprueft werden konnte' },
    next: { type: 'string', description: 'Der naechste rationale Schritt' },
    report: { type: 'string', description: 'Dein vollstaendiger Report im Format deiner Anleitung (Markdown), nichts weglassen' },
  },
  required: ['verdict', 'findings', 'next', 'report'],
}

const brief = (stepName, prior) => [
  `Auftrags-Typ: \`${TYPE}\`. Du bist Glied der Pflichtkette (${CHAIN.join(' -> ')}).`,
  `Deine Rolle hier: ${STEP_BRIEF[stepName] || 'nach deiner Anleitung pruefen.'}`,
  '',
  'AUFGABE:',
  TASK,
  CONTEXT ? `\nKONTEXT:\n${CONTEXT}` : '',
  prior ? `\nERGEBNISSE DER VORSTUFE (nutze sie, pruefe sie nicht blind nach):\n${prior}` : '',
  '',
  ZIEL,
  ENGINE_NOTE,
  'Antworte ausschliesslich ueber StructuredOutput; das Feld `report` traegt deinen vollstaendigen Block.',
].filter(Boolean).join('\n')

// ---- Phase 1: Rechner parallel ---------------------------------------------
const workers = CHAIN.filter(s => !REVIEWERS.includes(s))
const reviewers = CHAIN.filter(s => REVIEWERS.includes(s))

log(`kette[${TYPE}]: ${workers.length} Rechner parallel, danach ${reviewers.length} Gegenleser`)

const workerResults = workers.length ? await parallel(workers.map(s => () =>
  agent(brief(s, null), { agentType: s, label: `${s}`, phase: 'Rechner', schema: STEP_SCHEMA })
)) : []

const priorText = workers.map((s, i) => {
  const r = workerResults[i]
  if (!r) return `${s}: kein Ergebnis (uebersprungen oder abgebrochen)`
  const f = (r.findings || []).map(x => `  - [${x.severity}] ${x.point} (${x.evidence})`).join('\n')
  return `${s}: ${r.verdict}\n${f}\n  naechster Schritt laut ${s}: ${r.next}`
}).join('\n\n')

// ---- Phase 2: Gegenleser, MIT den Zahlen der ersten Phase -------------------
const reviewerResults = reviewers.length ? await parallel(reviewers.map(s => () =>
  agent(brief(s, priorText || null), { agentType: s, label: `${s}`, phase: 'Gegenleser', schema: STEP_SCHEMA })
)) : []

// ---- Zusammenfuehren --------------------------------------------------------
const all = [...workers, ...reviewers]
const allRes = [...workerResults, ...reviewerResults]

const ran = all.filter((s, i) => !!allRes[i])
const failed = all.filter((s, i) => !allRes[i])
const blockers = []
allRes.forEach((r, i) => {
  if (!r) return
  ;(r.findings || []).filter(f => f.severity === 'blocker')
    .forEach(f => blockers.push({ step: all[i], point: f.point, evidence: f.evidence }))
})

log(`kette[${TYPE}] fertig: ${ran.length}/${all.length} gelaufen, ${blockers.length} Blocker`)

return {
  type: TYPE,
  chain: CHAIN,
  ran,
  failed,
  blockers,
  verdicts: all.reduce((a, s, i) => { a[s] = allRes[i] ? allRes[i].verdict : null; return a }, {}),
  next_steps: all.reduce((a, s, i) => { a[s] = allRes[i] ? allRes[i].next : null; return a }, {}),
  open: all.reduce((a, s, i) => { a[s] = allRes[i] ? (allRes[i].open || []) : null; return a }, {}),
  reports: all.reduce((a, s, i) => { a[s] = allRes[i] ? allRes[i].report : null; return a }, {}),
  // Die Kette gilt erst als erledigt, wenn jedes Glied wirklich lief. Fehlende
  // Glieder sind KEIN Freibrief -- entweder nachholen oder per receipt.py --skip
  // mit Grund auslassen (der Grund landet in der Quittung und im Retro).
  complete: failed.length === 0,
  hint: failed.length
    ? `Nicht gelaufen: ${failed.join(', ')}. Entweder erneut starten oder mit Grund auslassen (receipt.py --skip <schritt> --why "...").`
    : 'Kette vollstaendig. Ergebnis zusammenfassen, dann weiterarbeiten.',
}
