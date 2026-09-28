export const meta = {
  name: 'konzept-weg',
  description: 'Konzept -> familien-scout (Wege-Karte) -> verdict-auditor Vollstaendigkeits-Check -> research-scout (EIN Call) -> ein-weg (variant-scout + strategy-auditor Batch)',
  whenToUse: 'Sobald Max ein KONZEPT oder eine grobe Edge nennt (VWAP, Gap, Fibonacci, Volumenprofil ...), nicht eine einzelne fertige Hypothese (dafuer ein-weg). args: {concept: string, date: "YYYY-MM-DD", source?: string, market?: string, skip_research?: boolean, skip_ein_weg?: boolean}',
  phases: [
    { title: 'Wege', detail: 'familien-scout: Konzept in Preis-Wege zerlegen, Stand je Weg, Skelette, Karte + Report + JSON schreiben' },
    { title: 'Vollstaendigkeit', detail: 'verdict-auditor: fehlt ein Weg, stimmt ein Stand nicht, wurde ein toter Verwandter uebersehen?' },
    { title: 'Nachtrag', detail: 'familien-scout traegt die Luecken des Auditors in Karte/Report/JSON nach (nur wenn welche gefunden)' },
    { title: 'Research', detail: 'research-scout, EIN Call je Konzept: alle Research-Fragen, Cache zuerst, Whys auf belegt/widerlegt/offen' },
    { title: 'Rueckschreiben', detail: 'familien-scout traegt Research-Stand und Aussortiertes in Karte + JSON ein (Karte bleibt lebendes Register)' },
    { title: 'Ein Weg', detail: 'Workflow ein-weg mit der bereinigten Hypothesen-Liste (variant-scout je Hypothese, strategy-auditor Batch)' },
  ],
}

// ---------------------------------------------------------------------------
// Regel Max, 10./11.09.2026 (Familien-Scout, Konzept-Weg):
//   Ein Konzept wird NIE als eine Hypothese getestet, sondern erst in alle konkreten
//   Preis-Wege zerlegt (Breite), dann je Weg nach dem EINEN Weg (Tiefe).
//   Neu gegenueber dem Konzept vom 10.09.: der verdict-auditor schaut DIREKT nach dem
//   Mapper drueber, ob ein Weg vergessen wurde, bevor Research und Rechenzeit fliessen
//   (Max, 11.09.: "unser Agent, der am Ende noch drueberschaut, ob was vergessen wurde").
//   Der Stempel je Weg nach der Box bleibt beim verdict-auditor, das ist Handbetrieb.
// Der Workflow selbst schreibt keine Dateien; familien-scout schreibt Karte/Report/JSON,
// research-scout pflegt den Research-Cache. Nichts davon geht in queue.json/Bank/Buch.
// ---------------------------------------------------------------------------

const CONCEPT = args && typeof args.concept === 'string' ? args.concept.trim() : ''
const DATE = args && typeof args.date === 'string' ? args.date.trim() : ''
if (!CONCEPT) {
  return { error: 'args.concept fehlt. Erwartet: {concept: "VWAP plus Baender", date: "YYYY-MM-DD", source?, market?, skip_research?, skip_ein_weg?}' }
}
if (!/^\d{4}-\d{2}-\d{2}$/.test(DATE)) {
  return { error: 'args.date fehlt oder ist nicht YYYY-MM-DD (Workflows haben keine Uhr, das Datum kommt von aussen).' }
}
const SOURCE = (args && args.source) ? String(args.source) : 'Max'
const MARKET = (args && args.market) ? String(args.market) : ''
const SKIP_RESEARCH = !!(args && args.skip_research)
const SKIP_EIN_WEG = !!(args && args.skip_ein_weg)

const ENGINE_NOTE = [
  'Engine-Pfad: C:\\Users\\maxlk\\Projects\\trading-data\\engine (auf Box und PC gleich; auf dem Laptop eine Kopie vom 03.09.2026).',
  'Fehlt der Pfad oder wirkt er veraltet, per `ssh Administrator@100.127.89.9` auf der Box greppen.',
  'Vault: Bereiche/Strategie-Logbuch.md, Bereiche/Hypothesen-Bank (*).md, Projekte/, Ressourcen/Research-Cache.md, nur gezielte Greps.',
].join(' ')

const PATH_ITEM = {
  type: 'object',
  properties: {
    id: { type: 'string', description: 'z.B. W5' },
    description: { type: 'string', description: 'Bewegung in einem Satz' },
    label: { type: 'string', description: 'Etikett: Trend / Mean Reversion / Intraday Bias / Swing / Relative Value / Filter' },
    role: { type: 'string', description: 'Signal / Filter / Level / Exit / Zeitfenster' },
    status: { type: 'string', description: 'im Buch (<Bein>) / tot (Logbuch #n) / gemessen ohne Kandidat (n Trials) / offen' },
    engine_path: { type: 'string', description: 'maband/tsmom-Achse mit Fundstelle, oder "Modul-Spec: ..."' },
    book_target: { type: 'string', description: 'Ersatz fuer <Bein> / neues Bein / Live-Buch-Merker' },
    related_dead: { type: 'string', description: 'Logbuch-/Bank-IDs toter Verwandter, sonst leer' },
    has_story: { type: 'boolean' },
    swing: { type: 'boolean' },
  },
  required: ['id', 'description', 'label', 'role', 'status', 'has_story'],
}

const HYP_ITEM = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    title: { type: 'string' },
    mechanism: { type: 'string' },
    why: { type: 'string', minLength: 20, description: 'mindestens 20 Zeichen, ein-weg stoppt sonst hart' },
    market: { type: 'string' },
    family: { type: 'string' },
    source: { type: 'string' },
    path: { type: 'string', description: 'Weg-ID + Richtung' },
    role: { type: 'string' },
    engine_path: { type: 'string' },
    module_spec: { type: 'string', description: 'leer, wenn engine-faehig' },
    book_target: { type: 'string' },
    related_dead: { type: 'string' },
    why_status: { type: 'string', enum: ['entwurf', 'belegt'] },
    research_questions: { type: 'array', items: { type: 'string' } },
    rank: { type: 'integer' },
    swing: { type: 'boolean' },
  },
  required: ['id', 'title', 'mechanism', 'why', 'path', 'why_status', 'rank'],
}

const MAP_SCHEMA = {
  type: 'object',
  properties: {
    concept: { type: 'string' },
    report_path: { type: 'string', description: 'ABSOLUTER Pfad, <engine>/discovery/scout_reports/familien_<konzept>_<YYMMDD>.md' },
    json_path: { type: 'string', description: 'ABSOLUTER Pfad, <engine>/discovery/jobs_proposed/familien_<konzept>_<YYMMDD>.json' },
    card_path: { type: 'string', description: 'ABSOLUTER Pfad, <vault>/Projekte/<Konzept> Wege-Karte.md' },
    existing_card: { type: 'string', description: 'ABSOLUTER Pfad einer schon vorhandenen HAND-Karte zum selben Konzept (nicht die eigene Wege-Karte), sonst leer' },
    inventory: { type: 'string', description: 'Inventar-Stand in zwei Saetzen (Trials, Bank-Zeilen, Logbuch-Nummern)' },
    paths: { type: 'array', items: PATH_ITEM },
    hypotheses: { type: 'array', items: HYP_ITEM },
    module_specs: { type: 'string', description: 'Was in maband/tsmom fehlt, sonst leer' },
    not_checked: { type: 'string' },
    report: { type: 'string', description: 'Deine komplette Chat-Antwort im Ausgabeformat deiner Anleitung (Markdown)' },
  },
  required: ['concept', 'report_path', 'json_path', 'card_path', 'inventory', 'paths', 'hypotheses', 'report'],
}

const COMPLETENESS_SCHEMA = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['vollstaendig', 'Luecken'] },
    missing_paths: {
      type: 'array',
      description: 'Wege, die aus Elementen x Beziehungen x Richtung folgen, aber in der Karte fehlen',
      items: { type: 'object', properties: { description: { type: 'string' }, reason: { type: 'string' } }, required: ['description', 'reason'] },
    },
    wrong_status: {
      type: 'array',
      description: 'Wege, deren Stand nicht zur Beweislage passt (z.B. "offen", obwohl im Register 40 Trials liegen; "tot" ohne nachgelesene Nummer)',
      items: { type: 'object', properties: { path_id: { type: 'string' }, issue: { type: 'string' } }, required: ['path_id', 'issue'] },
    },
    contamination_missed: {
      type: 'array',
      description: 'Tote Verwandte aus Logbuch/Bank/ideas.json, die die Karte nicht nennt',
      items: { type: 'object', properties: { path_id: { type: 'string' }, ref: { type: 'string' }, issue: { type: 'string' } }, required: ['path_id', 'ref'] },
    },
    report: { type: 'string', description: 'Dein Block im Ausgabeformat (Urteil, Ausgelassenes, max. 3 Nachtraege, nicht geprueft)' },
  },
  required: ['verdict', 'missing_paths', 'wrong_status', 'contamination_missed', 'report'],
}

const RESEARCH_SCHEMA = {
  type: 'object',
  properties: {
    rows: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          hypothesis_id: { type: 'string' },
          status: { type: 'string', enum: ['belegt', 'widerlegt', 'offen'] },
          evidence: { type: 'string', description: 'Quelle(n) mit Link oder Cache-Zeile, ein Satz' },
          why_revised: { type: 'string', description: 'Ueberarbeitetes Why mit Beleg, sonst leer' },
        },
        required: ['hypothesis_id', 'status', 'evidence'],
      },
    },
    cache_updated: { type: 'boolean', description: 'true, wenn neue externe Claims in Ressourcen/Research-Cache.md eingetragen wurden' },
    report: { type: 'string', description: 'Volle Antwort mit Quellen (Markdown)' },
  },
  required: ['rows', 'cache_updated', 'report'],
}

function pathsTable(paths) {
  return (paths || []).map(p => `${p.id} | ${p.description} | ${p.label} | ${p.role} | ${p.status} | ${p.engine_path || ''} | ${p.book_target || ''} | tot: ${p.related_dead || '-'}${p.swing ? ' | (Swing)' : ''}`).join('\n')
}

// ---- Phase 1: familien-scout -------------------------------------------------
log(`konzept-weg: "${CONCEPT}" (Quelle ${SOURCE}${MARKET ? ', Markt ' + MARKET : ''})`)
let map = await agent(
  [
    `Konzept: ${CONCEPT}`,
    `Quelle: ${SOURCE}`,
    MARKET ? `Markt-Fokus: ${MARKET}` : null,
    `Datum fuer Dateinamen und "erstellt": ${DATE}`,
    '',
    'Zerlege das Konzept nach deiner Anleitung in alle Preis-Wege (Elemente -> Beziehungen -> Richtung), Inventar zuerst,',
    'Stand je Weg gegen Register/Logbuch/Bank/Engine, Skelette nur fuer offene Wege mit Story, Swing-Wege mitfuehren und markieren.',
    'Schreibe die drei Dateien (Report, Hypothesen-JSON, Vault-Karte; bestehende Karte nie ueberschreiben, daneben legen).',
    ENGINE_NOTE,
    'Antworte ausschliesslich ueber StructuredOutput; `report` traegt deine komplette Chat-Antwort, `paths`/`hypotheses` exakt wie in den Dateien.',
  ].filter(Boolean).join('\n'),
  { agentType: 'familien-scout', label: `familien-scout:${CONCEPT}`, phase: 'Wege', schema: MAP_SCHEMA }
)
if (!map) {
  return { error: 'familien-scout ohne Ergebnis (uebersprungen/abgebrochen). Nichts geschrieben, nichts weitergereicht.' }
}
log(`Wege: ${map.paths.length}, Skelette: ${map.hypotheses.length}${map.existing_card ? ', bestehende Karte: ' + map.existing_card : ''}`)

// ---- Phase 2: verdict-auditor Vollstaendigkeits-Check ---------------------------
// Barriere ist hier richtig: der Auditor braucht die GANZE Karte, nicht einzelne Wege.
const check = await agent(
  [
    `Vollstaendigkeits-Check einer frischen Wege-Karte von familien-scout zum Konzept "${CONCEPT}" (${DATE}).`,
    'Das ist ein "fertig"-Urteil ueber Gebautes: Frage ist NICHT, ob ein Weg eine Edge hat, sondern ob die Karte VOLLSTAENDIG ist',
    'und ob jeder Stand von der Beweislage getragen wird. Pruefe konkret:',
    '1. Gehe Elemente x Beziehungen (hin zu / weg von / hindurch / abprallen / entlanglaufen / kreuzen+halten / kreuzen+scheitern; Zustaende steigt/faellt/flach, eng/weit/wechselt) x Richtung selbst durch: fehlt ein Weg?',
    '2. Stimmt der Stand je Weg? "offen" gegen Register/Bank/Logbuch gegenpruefen (Counter-Greps, nie registry.json komplett); "tot" nur mit nachgelesener Nummer.',
    '3. Wurde ein toter Verwandter uebersehen (Logbuch-Friedhof, ideas.json, Bank-Notizen)?',
    '4. Swing-Wege mitgefuehrt und markiert (Regel Max 11.09.2026)?',
    'Du aenderst keine Dateien. Lies die Karte und den Report ueber ihre Pfade, nicht nur die Tabelle unten.',
    ENGINE_NOTE,
    '',
    `Karte: ${map.card_path}`,
    `Report: ${map.report_path}`,
    `JSON: ${map.json_path}`,
    map.existing_card ? `Bestehende Hand-Karte zum selben Konzept (Abgleich!): ${map.existing_card}` : null,
    `Inventar laut Scout: ${map.inventory}`,
    '',
    'Wege laut Scout (id | Bewegung | Etikett | Rolle | Stand | Engine | Buch | tote Verwandte):',
    pathsTable(map.paths),
    '',
    'Antworte ausschliesslich ueber StructuredOutput; `report` traegt deinen vollen Block.',
  ].filter(Boolean).join('\n'),
  { agentType: 'verdict-auditor', label: `verdict-auditor:vollstaendigkeit(${CONCEPT})`, phase: 'Vollstaendigkeit', schema: COMPLETENESS_SCHEMA }
)
if (!check) log('verdict-auditor ohne Ergebnis, Vollstaendigkeit ungeprueft (wird im Ergebnis vermerkt)')

// ---- Phase 3: Nachtrag durch familien-scout, nur bei Luecken -------------------
const gaps = check ? (check.missing_paths.length + check.wrong_status.length + check.contamination_missed.length) : 0
let map2 = null
if (check && gaps > 0) {
  log(`verdict-auditor: ${check.missing_paths.length} fehlende Wege, ${check.wrong_status.length} falsche Staende, ${check.contamination_missed.length} uebersehene Tote -> Nachtrag`)
  map2 = await agent(
    [
      `Nachtrag zu deiner Wege-Karte "${CONCEPT}" (${DATE}). Der verdict-auditor hat Luecken gefunden. Trage sie in DIESELBEN drei Dateien nach`,
      `(Karte ${map.card_path}, Report ${map.report_path}, JSON ${map.json_path}), ohne die bestehenden Wege umzunummerieren.`,
      map.existing_card ? `Die bestehende Hand-Karte ${map.existing_card} bleibt unangetastet und im Kopf deiner Karte verlinkt.` : null,
      'Neue Wege bekommen die naechste freie Nummer; korrigierte Staende bekommen die Begruendung des Auditors; uebersehene Tote wandern in "Verwandte Tote".',
      'Skelette nur fuer Wege, die danach wirklich offen sind und eine Story haben. Widersprichst du dem Auditor an einer Stelle, begruende das im Report statt es zu ignorieren.',
      ENGINE_NOTE,
      '',
      'Fehlende Wege:',
      check.missing_paths.map(m => `- ${m.description}: ${m.reason}`).join('\n') || '- keine',
      'Falsche Staende:',
      check.wrong_status.map(w => `- ${w.path_id}: ${w.issue}`).join('\n') || '- keine',
      'Uebersehene tote Verwandte:',
      check.contamination_missed.map(c => `- ${c.path_id}: ${c.ref} ${c.issue || ''}`).join('\n') || '- keine',
      '',
      'Antworte ausschliesslich ueber StructuredOutput mit dem VOLLSTAENDIGEN Stand (alle Wege, alle Skelette) nach dem Nachtrag.',
    ].filter(Boolean).join('\n'),
    { agentType: 'familien-scout', label: `familien-scout:nachtrag(${CONCEPT})`, phase: 'Nachtrag', schema: MAP_SCHEMA }
  )
  if (map2) {
    // Pfade und die Hand-Karte aus dem ersten Lauf behalten, falls der Nachtrag sie nicht wieder nennt.
    map = Object.assign({}, map, map2, {
      card_path: map2.card_path || map.card_path,
      report_path: map2.report_path || map.report_path,
      json_path: map2.json_path || map.json_path,
      existing_card: map2.existing_card || map.existing_card || '',
    })
    log(`Nach Nachtrag: ${map.paths.length} Wege, ${map.hypotheses.length} Skelette (Nachtrag selbst ungeprueft, kein zweiter Auditor-Lauf)`)
  } else log('Nachtrag ohne Ergebnis, es gilt der Stand vor dem Check (Luecken bleiben im Ergebnis sichtbar)')
} else if (check) {
  log('verdict-auditor: Karte vollstaendig')
}

// ---- Phase 4: research-scout, EIN Call je Konzept -----------------------------
const hyps = (map.hypotheses || []).filter(Boolean)
const withQuestions = hyps.filter(h => Array.isArray(h.research_questions) && h.research_questions.length)
let research = null
if (!SKIP_RESEARCH && withQuestions.length) {
  const qBlock = withQuestions.map(h => [
    `Hypothese ${h.id} (${h.path}): ${h.title}`,
    `Why-Entwurf: ${h.why}`,
    'Fragen:',
    h.research_questions.map(q => `  - ${q}`).join('\n'),
  ].join('\n')).join('\n\n')
  research = await agent(
    [
      `Research zu ${withQuestions.length} Hypothesen-Skeletten aus der Wege-Karte "${CONCEPT}" (familien-scout, ${DATE}). EIN Call fuer alle Fragen.`,
      'Reihenfolge ist Pflicht: Ressourcen/Research-Cache.md, dann Bereiche/Strategie-Logbuch.md, erst dann Web (defuddle statt WebFetch, Primaerquellen).',
      'Je Hypothese ein Status: belegt (Quelle stuetzt den Mechanismus kausal), widerlegt (Literatur oder eigenes Logbuch spricht dagegen), offen (nichts gefunden).',
      'Bei belegt: das Why mit Beleg neu formulieren (why_revised). Neue EXTERNE Claims in den Research-Cache eintragen (Format der Datei exakt einhalten).',
      'Keine Websuche aus Gewohnheit: steht es schon im Cache, ist das die Antwort. Ausnahme (Regel 28.09.2026, Logbuch #074): ein NEGATIVBEFUND ("kein Paper/keine Studie gefunden") in Cache oder Logbuch, der aelter als 60 Tage ist, ist keine Antwort, sondern eine Wiedervorlage: neu suchen, dann in der alten Zeile "geprüft TT.MM.JJJJ" ergaenzen.',
      '',
      qBlock,
      '',
      'Antworte ausschliesslich ueber StructuredOutput; `report` traegt die volle Antwort mit Quellen.',
    ].join('\n'),
    { agentType: 'research-scout', label: `research-scout:${CONCEPT}(${withQuestions.length})`, phase: 'Research', schema: RESEARCH_SCHEMA }
  )
  if (!research) log('research-scout ohne Ergebnis, Whys bleiben auf Entwurf')
} else {
  log(SKIP_RESEARCH ? 'Research uebersprungen (skip_research)' : 'Keine Research-Fragen, Research uebersprungen')
}

// ---- Whys anwenden, widerlegte raus --------------------------------------------
const rByid = {}
if (research && Array.isArray(research.rows)) {
  const known = new Set(hyps.map(h => h.id))
  research.rows.forEach(r => {
    rByid[r.hypothesis_id] = r
    if (!known.has(r.hypothesis_id)) log(`research-scout nennt unbekannte Hypothesen-ID "${r.hypothesis_id}" (keinem Skelett zugeordnet)`)
  })
  hyps.filter(h => !rByid[h.id] && Array.isArray(h.research_questions) && h.research_questions.length)
    .forEach(h => log(`research-scout hat ${h.id} nicht beantwortet, bleibt "offen"`))
}
const dropped = []
const kept = []
hyps.forEach(h => {
  const r = rByid[h.id]
  if (h.swing) { dropped.push({ id: h.id, reason: 'Swing-Weg, Live-Buch-Merker, kein Prop-Buch-Job' }); return }
  // "widerlegt" durch Research ist KEIN "tot" (tot nur nach vollem Test, Regel Hypothese vor Urteil):
  // die Hypothese geht nur nicht in diese Rechenrunde und bleibt in der Karte mit Quelle sichtbar.
  if (r && r.status === 'widerlegt') { dropped.push({ id: h.id, reason: 'Research widerlegt, nicht in diese Runde (kein Tot-Stempel): ' + r.evidence }); return }
  const why = r && r.status === 'belegt' && r.why_revised && String(r.why_revised).trim().length >= 20 ? r.why_revised : h.why
  if (!why || String(why).trim().length < 20) { dropped.push({ id: h.id, reason: 'Why zu kurz (< 20 Zeichen), nicht an ein-weg; Scout muss nachbessern' }); return }
  kept.push({
    id: h.id, title: h.title, mechanism: h.mechanism, why,
    market: h.market || MARKET || undefined, family: h.family || undefined,
    source: (h.source || `familien-scout ${DATE}`) + (r ? ` / research ${r.status}` : ' / research offen'),
  })
})
if (dropped.length) log(`Raus vor ein-weg: ${dropped.map(d => d.id).join(', ')}`)

// ---- Phase 4b: Research-Stand in Karte + JSON zurueckschreiben -------------------
// Ohne das veraltet die Karte am Tag ihrer Entstehung genau in dem Punkt, der neu dazukam.
let writeback = null
const researchRows = research && Array.isArray(research.rows) ? research.rows : []
if (researchRows.length || dropped.some(d => !d.reason.startsWith('Swing'))) {
  writeback = await agent(
    [
      `Rueckschreiben in deine Wege-Karte "${CONCEPT}" (${DATE}): Karte ${map.card_path} und JSON ${map.json_path}.`,
      'Trage je Skelett den Research-Stand ein (why_status belegt/widerlegt/offen, Quelle, bei belegt das ueberarbeitete Why) und vermerke, welche Skelette',
      'in dieser Runde NICHT weiter an ein-weg gehen und warum. Wichtig: "Research widerlegt" ist KEIN Tot-Stempel (tot nur nach vollem Test);',
      'der Weg bleibt in der Karte mit Stand "Research widerlegt (Quelle)", nichts wird geloescht, keine Wege umnummeriert. Report nicht anfassen.',
      'Kurze Textantwort: was geaendert wurde, eine Zeile je Skelett.',
      '',
      'Research-Zeilen:',
      researchRows.map(r => `- ${r.hypothesis_id}: ${r.status}; ${r.evidence}${r.why_revised ? '; Why neu: ' + r.why_revised : ''}`).join('\n') || '- keine',
      'Nicht an ein-weg:',
      dropped.map(d => `- ${d.id}: ${d.reason}`).join('\n') || '- keine',
    ].join('\n'),
    { agentType: 'familien-scout', label: `familien-scout:rueckschreiben(${CONCEPT})`, phase: 'Rueckschreiben' }
  )
  if (!writeback) log('Rueckschreiben ohne Ergebnis: Research-Stand von Hand in Karte + JSON nachtragen')
}

// ---- Phase 5: ein-weg als Kind-Workflow ----------------------------------------
let einWeg = null
if (SKIP_EIN_WEG) {
  log('ein-weg uebersprungen (skip_ein_weg)')
} else if (!kept.length) {
  log('Keine Hypothese uebrig, ein-weg entfaellt')
} else {
  log(`ein-weg mit ${kept.length} Hypothese(n)`)
  try {
    einWeg = await workflow('ein-weg', { hypotheses: kept })
  } catch (e) {
    einWeg = { error: 'ein-weg konnte nicht gestartet werden: ' + String(e && e.message || e) }
    log(einWeg.error)
  }
}

// ---- Ergebnis --------------------------------------------------------------------
const statusCounts = (map.paths || []).reduce((a, p) => {
  const k = String(p.status || 'unbekannt').split(' ')[0].toLowerCase()
  a[k] = (a[k] || 0) + 1; return a
}, {})
log('konzept-weg fertig: ' + Object.entries(statusCounts).map(([k, n]) => `${n}x ${k}`).join(', '))

return {
  concept: CONCEPT,
  date: DATE,
  files: { card: map.card_path, report: map.report_path, json: map.json_path, existing_card: map.existing_card || null },
  paths: map.paths,
  path_status_counts: statusCounts,
  completeness: check
    ? { verdict: map2 ? 'Luecken nachgetragen (Nachtrag ungeprueft)' : check.verdict, gaps, nachtrag: !!map2, report: check.report }
    : { verdict: 'ungeprueft', gaps: null, nachtrag: false, report: null },
  research: research ? { rows: research.rows, cache_updated: research.cache_updated, report: research.report } : null,
  writeback: writeback === null ? 'nicht noetig oder uebersprungen' : (writeback || 'FEHLGESCHLAGEN, von Hand nachtragen'),
  hypotheses_to_ein_weg: kept.map(h => h.id),
  dropped,
  ein_weg: einWeg,
  reports: { familien_scout: map.report, module_specs: map.module_specs || null, not_checked: map.not_checked || null },
  reminder: [
    'Hauptsession: Karte lesen und mit einer bestehenden Hand-Karte abgleichen (Abnahmetest). Steht writeback auf FEHLGESCHLAGEN, Research-Zeilen und dropped von Hand in Karte + JSON nachtragen.',
    'Danach Schritt 3/4 des EINEN Wegs: H()-Zeilen eintragen, pipeline-auditor (Hook pipeline_ok), hypothesis_bank.py --enqueue --push.',
    'Nach der Box: verdict-auditor stempelt je Weg, Stand wandert in die Karte zurueck. Buch-Luecke je Weg mitnennen.',
  ].join(' '),
}
