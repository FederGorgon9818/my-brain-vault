export const meta = {
  name: 'ein-weg',
  description: 'Der EINE Weg, Schritt 2: variant-scout je Hypothese, dann EIN strategy-auditor-Batch-Call, Ergebnis als Entscheidungstabelle',
  whenToUse: 'Sobald eine oder mehrere neue Hypothesen vorliegen (Research, Discovery-Auswertung, Idee von Max) und BEVOR sie als Zeile in eine Hypothesen-Bank-Notiz oder als H()-Job in hypothesis_bank.py geschrieben werden. args: {hypotheses: [{id, title, mechanism, why, market?, family?, source?}]}',
  phases: [
    { title: 'Varianten', detail: 'variant-scout je Hypothese (parallel), gegen echte Engine-Achsen + bestehende Bank' },
    { title: 'Story-Check', detail: 'strategy-auditor Batch-Vorpruefung: EIN Call ueber alle testbaren Whys' },
  ],
}

// ---------------------------------------------------------------------------
// Regel Max, 23.08.2026 ("Der EINE Weg") + 01.09.2026 (variant-scout, Batch-Vorpruefung):
//   1. WHY zuerst (kommt mit der Hypothese rein, wird hier nur weitergereicht).
//   2. ARTEN: variant-scout misst je Hypothese die echten Varianten (n >= 10?).
//      Danach strategy-auditor im Batch-Modus: EIN Aufruf ueber die ganze Gruppe,
//      die variant-scout als testbar eingestuft hat, nie ein Call pro Hypothese.
//   3./4. FALLEN + RECHNEN passieren danach: die Hauptsession traegt die H()-Zeilen ein,
//      pipeline-auditor gibt frei (Hook pipeline_ok), hypothesis_bank.py --enqueue --push.
// Der Workflow schreibt nie Dateien. Er liefert die Entscheidungsgrundlage zurueck,
// inklusive der vollen Agent-Reports, damit nichts gegenueber dem Handbetrieb verloren geht.
// ---------------------------------------------------------------------------

const HYPS = Array.isArray(args && args.hypotheses) ? args.hypotheses.filter(Boolean) : []
if (!HYPS.length) {
  return { error: 'args.hypotheses fehlt oder ist leer. Erwartet: {hypotheses: [{id, title, mechanism, why, market?, family?, source?}]}' }
}
const missingWhy = HYPS.filter(h => !h.why || String(h.why).trim().length < 20)
if (missingWhy.length) {
  // Schritt 1 des EINEN Wegs: ohne Why kein Test. Das ist kein Fall fuer einen Agent, sondern ein harter Stopp.
  return { error: 'Ohne Why kein Test (Regel 23.08.2026). Fehlendes/zu kurzes Why bei: ' + missingWhy.map(h => h.id || h.title).join(', ') }
}

const ENGINE_NOTE = [
  'Engine-Pfad: C:\\Users\\maxlk\\Projects\\trading-data\\engine (PC; auf dem Laptop liegt dort eine Kopie vom 03.09.2026).',
  'Fehlt der Pfad oder wirkt er veraltet, per `ssh Administrator@100.127.89.9` auf der Box greppen (gleicher Pfad dort).',
  'Vault-Bank: Bereiche/Hypothesen-Bank (*).md und Bereiche/Strategie-Logbuch.md, nur gezielte Greps.',
].join(' ')

const VARIANT_SCHEMA = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    mechanism: { type: 'string', description: 'Mechanismus in einem Satz' },
    relation: {
      type: 'object',
      properties: {
        status: { type: 'string', enum: ['neu', 'verwandt_lebt', 'verwandt_tot'] },
        ref: { type: 'string', description: 'ID/Logbuch-Nummer des Verwandten, sonst leer' },
        contamination: { type: 'string', description: 'Was gleich ist und was sich unterscheidet, sonst leer' },
      },
      required: ['status'],
    },
    axes: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          axis: { type: 'string' },
          values: { type: 'string' },
          engine_status: { type: 'string', description: 'vorhanden (Fundstelle) oder fehlt (was gebaut werden muesste)' },
        },
        required: ['axis', 'values', 'engine_status'],
      },
    },
    n: { type: 'integer', description: 'Zahl der echten Varianten nach Streichung von Redundanz' },
    calc: { type: 'string', description: 'Rechenweg, z.B. 3 Fenster x 2 Signale x 2 Stops' },
    redundancy: { type: 'string' },
    recommendation: { type: 'string', enum: ['Testbar', 'Grenzwertig', 'Nicht sinnvoll testbar'] },
    reason: { type: 'string', description: 'Ein Satz Begruendung' },
    needs_engine_work: { type: 'boolean', description: 'true, wenn eine Achse erst als mb_kind/tm_signal gebaut werden muss' },
    report: { type: 'string', description: 'Dein vollstaendiger Block im Ausgabeformat deiner Anleitung (Markdown), nichts weglassen' },
  },
  required: ['id', 'mechanism', 'relation', 'n', 'recommendation', 'reason', 'report'],
}

const BATCH_SCHEMA = {
  type: 'object',
  properties: {
    rows: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          verdict: { type: 'string', enum: ['Story haelt', 'Story haelt mit Vorbehalt', 'Story faellt durch, nicht bauen'] },
          reason: { type: 'string', description: 'Ein Satz; bei faellt durch 2-3 Saetze' },
          fix: { type: 'string', description: 'Was nachgebessert werden muesste, sonst leer' },
        },
        required: ['id', 'verdict', 'reason'],
      },
    },
    summary: { type: 'string', description: 'Wie viele direkt in hypothesis_bank.py gehen, welche zuerst nachgebessert werden' },
    report: { type: 'string', description: 'Die volle Tabelle im Report-Format Batch-Vorpruefung (Markdown)' },
  },
  required: ['rows', 'summary', 'report'],
}

function hypBlock(h) {
  return [
    `ID: ${h.id || '(ohne ID)'}`,
    `Titel: ${h.title || ''}`,
    `Mechanismus: ${h.mechanism || ''}`,
    `Why: ${h.why}`,
    h.market ? `Markt: ${h.market}` : null,
    h.family ? `Familie: ${h.family}` : null,
    h.source ? `Quelle: ${h.source}` : null,
  ].filter(Boolean).join('\n')
}

// ---- Phase 1: variant-scout je Hypothese -----------------------------------
// Barriere ist hier korrekt: die Batch-Vorpruefung braucht ALLE testbaren Hypothesen
// zusammen in EINEM Call (Regel 01.09.2026), nicht eine nach der anderen.
log(`ein-weg: ${HYPS.length} Hypothese(n), variant-scout laeuft parallel`)
const variants = await parallel(HYPS.map((h, i) => () =>
  agent(
    [
      'Neue Hypothese, noch NICHT in der Bank. Vermiss sie nach deiner Anleitung (Achsen gegen den echten Engine-Code,',
      'Verwandtschaft gegen die bestehende Bank und den Friedhof im Logbuch, Redundanz streichen, n berechnen, Empfehlung).',
      ENGINE_NOTE,
      'Antworte ausschliesslich ueber StructuredOutput; das Feld `report` traegt deinen kompletten Block im Ausgabeformat.',
      '',
      hypBlock(h),
    ].join('\n'),
    { agentType: 'variant-scout', label: `variant-scout:${h.id || i + 1}`, phase: 'Varianten', schema: VARIANT_SCHEMA }
  )
))

const byId = {}
HYPS.forEach((h, i) => { byId[h.id || String(i + 1)] = { hyp: h, variant: variants[i] || null } })
const skipped = HYPS.filter((h, i) => !variants[i])
if (skipped.length) log(`variant-scout ohne Ergebnis fuer: ${skipped.map(h => h.id || h.title).join(', ')} (uebersprungen/abgebrochen)`)

const testable = HYPS.filter((h, i) => variants[i] && ['Testbar', 'Grenzwertig'].includes(variants[i].recommendation))
log(`Varianten: ${testable.length}/${HYPS.length} testbar oder grenzwertig`)

// ---- Phase 2: strategy-auditor Batch-Vorpruefung, EIN Call ------------------
let batch = null
if (testable.length) {
  const group = testable.map(h => {
    const v = byId[h.id || String(HYPS.indexOf(h) + 1)].variant
    return [
      hypBlock(h),
      `variant-scout: n=${v.n} (${v.calc || ''}), Empfehlung ${v.recommendation}: ${v.reason}`,
      v.relation && v.relation.status !== 'neu' ? `Verwandtschaft: ${v.relation.status} ${v.relation.ref || ''} ${v.relation.contamination || ''}` : null,
    ].filter(Boolean).join('\n')
  }).join('\n\n---\n\n')

  batch = await agent(
    [
      'Batch-Vorpruefung (billiger Modus, 01.09.2026): variant-scout hat die folgende Gruppe als testbar/grenzwertig eingestuft.',
      'Pruefe in DIESEM EINEN Aufruf nur die oekonomische Story jeder Hypothese (Why kausal? Look-ahead schon im Text erkennbar?',
      'Familie eindeutig? zu gut um wahr zu sein?), ohne Backtest-Daten, nach deinem Report-Format Batch-Vorpruefung.',
      'Keine 5-Punkte-Vollpruefung pro Zeile. Antworte ausschliesslich ueber StructuredOutput; `report` traegt die volle Tabelle.',
      '',
      group,
    ].join('\n'),
    { agentType: 'strategy-auditor', label: `strategy-auditor:batch(${testable.length})`, phase: 'Story-Check', schema: BATCH_SCHEMA }
  )
  if (!batch) log('strategy-auditor Batch-Call ohne Ergebnis (uebersprungen/abgebrochen)')
}

// ---- Entscheidungstabelle ---------------------------------------------------
const storyById = {}
if (batch && Array.isArray(batch.rows)) batch.rows.forEach(r => { storyById[r.id] = r })

const decisions = HYPS.map((h, i) => {
  const id = h.id || String(i + 1)
  const v = variants[i]
  const s = storyById[id] || null
  let status, next
  if (!v) {
    status = 'offen'; next = 'variant-scout erneut laufen lassen (kein Ergebnis)'
  } else if (v.recommendation === 'Nicht sinnvoll testbar') {
    status = 'nicht bauen (Varianten)'; next = v.reason
  } else if (!s) {
    status = 'offen'; next = 'Story-Check fehlt (Batch-Call ohne Ergebnis)'
  } else if (s.verdict === 'Story faellt durch, nicht bauen') {
    status = 'nicht bauen (Story)'; next = s.reason
  } else if (s.verdict === 'Story haelt mit Vorbehalt' || v.recommendation === 'Grenzwertig' || v.needs_engine_work) {
    status = 'nachbessern, dann Bank'
    next = [s.fix, v.needs_engine_work ? 'Engine-Achse fehlt (mb_kind/tm_signal bauen, dann Job)' : null, v.recommendation === 'Grenzwertig' ? v.reason : null].filter(Boolean).join('; ')
  } else {
    status = 'in Bank + H()-Zeile'
    next = `n=${v.n} Varianten eintragen (Bank-Notiz + hypothesis_bank.py), dann pipeline-auditor (setzt pipeline_ok), dann --enqueue --push`
  }
  return {
    id, title: h.title || '', status, next,
    variants: v ? { n: v.n, recommendation: v.recommendation, relation: v.relation, needs_engine_work: !!v.needs_engine_work } : null,
    story: s ? { verdict: s.verdict, reason: s.reason } : null,
  }
})

const counts = decisions.reduce((a, d) => { a[d.status] = (a[d.status] || 0) + 1; return a }, {})
log('ein-weg fertig: ' + Object.entries(counts).map(([k, n]) => `${n}x ${k}`).join(', '))

return {
  decisions,
  counts,
  batch_summary: batch ? batch.summary : null,
  reports: {
    variant_scout: HYPS.map((h, i) => ({ id: h.id || String(i + 1), report: variants[i] ? variants[i].report : null })),
    strategy_auditor_batch: batch ? batch.report : null,
  },
  reminder: 'Schritt 3/4 bleiben bei der Hauptsession: H()-Zeilen eintragen, pipeline-auditor (Hook pipeline_ok), hypothesis_bank.py --enqueue --push. Buch-Luecke je Hypothese mitnennen.',
}
