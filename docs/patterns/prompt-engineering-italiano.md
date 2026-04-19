# Pattern: Prompt engineering in italiano con AI

**Data formalizzazione**: 2026-04-20
**Basato su**: sessioni intensive con Claude Opus 4.7 + Claude Code
**Scopo**: consolidare pattern efficaci per conversazioni italiane con AI

## Executive summary

**Lavoro con AI in italiano** ha vantaggi e svantaggi specifici.

**Vantaggi**:
- Fluidità naturale (thinking nella mia lingua)
- Sfumature culturali italiane (ironia, understatement, formalità)
- Meno cognitive load di traduzione mentale

**Svantaggi**:
- Meno documentazione tecnica in italiano di modelli
- Alcuni termini tecnici hanno meno "peso" in italiano
- Modelli più piccoli (Qwen 7B) possono avere qualità ridotta su italiano

**Pattern scelto**: **italiano per conversazione + pensiero, inglese per termini
tecnici quando necessario**. Mix pragmatico, non purismo.

## Principi base

### 1. Italiano come lingua di conversazione

**Input a AI in italiano**:
- Naturale per me
- Claude Opus 4.7 gestisce benissimo italiano
- Risposte in italiano equivalenti a inglese come qualità

**Eccezione tecnica**: termini API/code/protocollo in inglese
(es. "function", "endpoint", "repository") — italiano keeps the technical accuracy.

### 2. Commit messages in inglese

**Perché**: convenzione Git/open source universale.

**Esempio**:
- `feat: install complete dev stack (node, python, vscode, ollama)` ✓
- `feat: installa stack completo (node, python, vscode, ollama)` ✗

**Eccezione**: se repo è chiaramente italiano-only (es. progetto personale no-contribute), ok italiano.

### 3. Documentation interna in italiano

**Scelgo italiano per**:
- CLAUDE.md
- JOURNAL.md
- ADR (Architecture Decision Records)
- Research notes
- Questa pagina

**Motivazione**:
- Sono io il reader principale (oggi e futuro)
- Sfumatura di ragionamento meglio in italiano
- Apprendimento approfondito in lingua madre
- Documenti sovrani (miei, non per open source)

### 4. Code comments: lingua mista consapevole

**Pattern che uso**:
- Commenti di alto livello (spiegazione logica): **italiano**
- Docstring per funzioni pubbliche: **inglese**
- TODO/FIXME: **inglese**
- Print/log debug: **italiano** (debug mio)
- Error messages user-facing: **italiano** se app italiana, **inglese** se internazionale

## Prompt patterns efficaci

### Pattern 1: "Voglio Y, propongo X, verifica"

**Struttura**:
```
Voglio <obiettivo finale>.
Il mio approccio è <approccio proposto>.
Verifica che: <vincoli specifici>.
Prima di eseguire mostrami <cosa>.
```

**Esempio reale**:
```
Voglio creare repo privato codemasterdd-ai-station su GitHub.
Approccio: gh repo create con --private --source=. --push.
Verifica che gh è installato, se non trovato usa path assoluto come workaround.
Prima di eseguire mostrami il comando esatto che userai.
```

**Perché funziona**:
- Obiettivo chiaro
- Approccio proposto (riduce Claude guessing)
- Vincoli espliciti (preserva intent)
- Review gate (preview prima di execute)

### Pattern 2: "Contesto, problema, richiesta"

**Struttura**:
```
Contesto: <situazione attuale>.
Problema: <cosa non va o decisione da prendere>.
Richiesta: <cosa vuoi da me>.
```

**Esempio reale**:
```
Contesto: ho installato Ollama, benchmark 93 tok/s Qwen 7B.
Problema: Claude Code ha committato "feat: install dev stack" senza Ollama.
Richiesta: propongo 3 approach per integrare Ollama nella storia:
  A) nuovo commit separato
  B) amend del commit esistente + force-push
  C) squash dei 2 commit
  Dammi trade-off chiari prima di eseguire.
```

### Pattern 3: Correzione diretta

**Quando Claude drift**:

**Struttura**:
```
[correzione diretta].
Non l'ho autorizzato.
Rimuovi/modifica [cosa].
Per futuro: [linea guida].
```

**Esempio reale**:
```
No. Mac mini non è dependency del piano, è estensione opzionale futura.
Non l'ho deciso come necessario.
Aggiorna CLAUDE.md: "Mac mini arriverà SE e QUANDO budget permette".
Per futuro: Lenovo deve essere autosufficiente da oggi.
```

**Perché**:
- Ferma propagazione dell'errore
- Propone fix esplicito
- Imposta pattern per evitare errore futuro

### Pattern 4: "Scelgo tra opzioni"

**Quando ho già opzioni e devo decidere**:

**Struttura**:
```
Opzioni:
A) <descrizione>
B) <descrizione>
C) <descrizione>

I miei criteri: <criterio 1>, <criterio 2>, <criterio 3>.

Claude: fai ranking con pro/contro per ciascuna, poi dimmi quale sceglieresti e perché.
La decisione finale è mia.
```

**Esempio reale**:
```
Opzioni nome repo:
A) lenovo-ai-station (attuale)
B) codemasterdd-ai-station (mio PC name)
C) ai-workstation (generico)
D) codemasterdd (solo nome macchina)

Criteri: future-proof, identity, leggibilità.

Claude: ranking pro/contro. Io decido.
```

### Pattern 5: Esplorare prima, eseguire dopo

**Per task non banali**:

**Struttura**:
```
Fase 1: ESPLORA
- Leggi <file/contesto>
- Cerca <pattern>
- Verifica <hypothesis>
- Riporta cosa trovato

Fase 2: PROPONI (dopo mio OK)
- Approccio basato su exploration
- Trade-off chiari

Fase 3: ESEGUI (dopo mio OK)
- Step-by-step
- Approvazione per ogni step
```

**Beneficio**: evita "Claude decide velocemente, io faccio da fermare".

### Pattern 6: Lavoro in più lingue

**Se serve output multilingue**:

**Struttura**:
```
Descrizione in italiano.
Output richiesto: <parte italiana> + <parte inglese>.
Esempio: README bilingue con # Titolo italiano / # English title.
```

**Esempio**: README progetto open source con header italiano + inglese.

## Anti-pattern da evitare

### Anti-pattern 1: "fai tu"

**Brutto prompt**: "fai setup Lenovo per AI".
**Problema**: scope infinito, Claude deve guessing.

**Meglio**:
```
Obiettivo: setup Lenovo per AI dev workstation personale.
Stack primario: Claude Code + Ollama + progetti Node/Python.
Stato iniziale: Windows 11 fresh install post-negoziazione.
Constraints: 8GB VRAM, 16GB RAM, 1TB SSD.
Priorità: sicurezza > stabilità > velocità > features.
Mio approccio: un comando alla volta con approvazione.
Iniziamo da: [specifico primo task].
```

### Anti-pattern 2: Copia incolla senza contesto

**Brutto**: copia error message da terminal, chiedi "fix this".
**Problema**: Claude senza contesto tenta random fix.

**Meglio**:
```
Context: sto facendo X nel repo Y.
Comando eseguito: [esatto].
Output/errore: [completo].
Cosa ho provato: [se qualcosa].
Ipotesi mia: [se hai un sospetto].
Cosa ti chiedo: [diagnosi? fix? spiegazione?]
```

### Anti-pattern 3: "Scrivi tutto"

**Brutto**: "scrivi ADR completo per Node 24".
**Problema**: Claude genera 2000 parole, mix di valide e hallucination.

**Meglio**:
```
Devo scrivere ADR "Node 24 vs 22".
Contesto: ho deciso Node 24 per supporto 3y + compat Evo-Tactics `^22`.
Struttura richiesta: Contesto | Decisione | Conseguenze | Alternative.
Lunghezza: ~1500-2000 parole.
Stile: tecnico + meta-learning personale.
Fatti chiave da includere: [lista].
Mostrami struttura outline prima, poi espandiamo sezione per sezione.
```

### Anti-pattern 4: Non correggere drift

**Brutto**: Claude dice qualcosa di impreciso → tu lasci passare → errore si propaga.

**Meglio**: correzione real-time con tono neutro:
```
Precisazione: [correzione].
Perché è importante: [ragione].
Aggiorna mental model per questa sessione.
```

### Anti-pattern 5: Lingua mista random

**Brutto**: mix italiano/inglese senza pattern.
**Problema**: Claude incertezza stile risposta.

**Meglio**: scegli consciamente (es. "italiano principale, inglese per termini tech inevitabili") e rimani consistente.

## Terminologia tecnica italiana: glossario personale

### Termini che TRADUCO in italiano

| English | Italiano (uso) |
|---------|----------------|
| commit | commit (invariato) |
| repository | repo / repository |
| branch | branch (invariato) |
| pull request | PR / pull request |
| file system | file system |
| database | database |
| server | server |
| client | client |
| code review | code review |
| deploy | deploy |

### Termini che PRESERVO in inglese

| English | Non tradotto perché... |
|---------|------------------------|
| framework | "struttura" perde specificità |
| middleware | termine puramente tech |
| API | standard internazionale |
| endpoint | idem |
| backend / frontend | idem |
| debugging | "correzione bug" clunky |
| refactoring | "rifattorizzazione" accademico |

### Concetti filosofici in italiano

| English | Italiano (uso) |
|---------|----------------|
| sovereign | sovrano |
| ownership | proprietà / sovranità |
| resilience | resilienza |
| YAGNI | YAGNI (acronimo invariato) |
| workflow | workflow (consolidato) |
| thinking partner | partner di pensiero (traduco) |

## Pattern italiano-specific

### Formalità

**Italiano ha tu/Lei formalità implicita**.

Con Claude: uso **tu informale** (è mio "collega"):
- "Aggiorna il file X"
- "Dimmi cosa ne pensi"
- "Spiegami perché"

**Non uso**:
- "Potrebbe cortesemente aggiornare..."
- "Le sarei grato se..."

**Tono**: dev-style, efficienza > cortesia forzata.

### Ironia e understatement

**Italiano ha sfumature** di ironia/sarcasmo che AI gestisce ragionevolmente.

**Esempi miei usati**:
- "Ma dai, è ovvio che Node 24 funziona meglio" → ironic pragmatismo
- "Praticamente ho vinto alla lotteria" → 93 tok/s benchmark
- "Meglio fermarsi prima che Claude installi mezza Anthropic" → self-deprecating stop

**AI response**: Claude Opus 4.7 capisce questi registri bene in italiano.

### Costruzioni specifiche

**Italiano ha strutture peculiari**:

**"Mi pare che" / "Direi che"**: hedging linguistic che AI comprende come "soft claim".

**"Insomma"**: segnale di sintesi/pragmatismo. Uso: "Insomma, lascio Node 24".

**"Diciamo che"**: concedere + introduci nuance. Uso: "Diciamo che Qwen 7B va bene per 80% task".

**"Alla fine"**: conclusione pragmatica dopo esplorazione. Uso: "Alla fine scelgo B perché...".

## Il caso specifico Claude AI

### Claude Opus 4.7 in italiano

**Strengths**:
- Grammatica italiana eccellente
- Vocabolario tecnico dev fluido
- Tono naturale (non robotico)
- Comprende sfumature culturali

**Weaknesses osservate**:
- Occasionalmente anglicismi dove italiano avrebbe termine (es. "performare" vs "avere buone prestazioni")
- Preferenza per italiano "corretto" vs "parlato" (posso dirgli "parla più colloquiale" se serve)

### Qwen 2.5 Coder 7B in italiano

**Test da fare nelle prossime sessioni**:
- Quality risposte in italiano vs inglese
- Se degrada significativamente → switcho input a inglese per Qwen
- Se qualità simile → mantengo italiano per comfort

### Pattern per modelli locali piccoli (es. Qwen 7B)

**Ipotesi da validare**:
- Prompt più brevi e strutturati
- Terminologia tech in inglese strict
- Format output esplicito (JSON, bullet list)

**Fallback se qualità italiano insufficiente**:
- Prompt in inglese
- Request output in italiano
- Workflow asimmetrico ma accettabile

## Meta-learning

### L'italiano come strumento di pensiero

**Scrivere in italiano costringe me a chiarire pensiero**.

Traducendo in inglese, potrei nascondere vaghezze dietro termini "sophisticated".
In italiano, se un concetto è vago, suona goffo → riformula → chiarisce.

**Effetto collaterale**: doc italiane tendono essere **più precise** di quanto
avrei in inglese, perché l'italiano perdona meno copertura con jargon.

### Bilingual writer advantage

Essere bilingual dev (italiano + inglese) permette:
- Accesso a documentation best (inglese)
- Community global (inglese)
- Ma pensiero profondo (italiano)

**Sweet spot**: produrre in italiano, **leggere in entrambe**.

### Claude AI come language learner / teacher

Interessante: quando scrivo a Claude in italiano colloquiale, **percepisco**
che adatta lo stile.

**Test che farò**: chiedere Claude correzioni italiano (grammatical, stylistic) come se fosse tutor.

### Pattern per evoluzione futura

**Fase 1 (ora)**: italiano a Claude, italiano doc, inglese code.
**Fase 2 (Ollama)**: test Qwen italiano quality, eventuale switch.
**Fase 3 (mature)**: italiano consolidato ovunque possibile, inglese solo tech universale.

## Fonti

- Anthropic docs su multilingual Claude: https://docs.claude.com/en/docs/build-with-claude/multilingual
- Qwen multilingual support: https://github.com/QwenLM/Qwen2.5
- Conventional Commits spec: https://www.conventionalcommits.org
- Accademia della Crusca (per neologismi tech): https://accademiadellacrusca.it

## Follow-up

### Da testare

- Claude Code comandi in italiano vs inglese (differenza quality?)
- Qwen 7B italiano test reale (aspetto dopo migrazione Evo)
- Prompt patterns più refinati con più esperienza

### Da espandere

- Template specifici per task comuni (commit message, ADR, README)
- Glossario esteso quando emergono nuovi termini
- Best practices Italian per dev docs (community?)
