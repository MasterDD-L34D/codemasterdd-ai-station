# Prompt Library and Reference System

Questa versione è una **patch di completezza** costruita sulla trascrizione completa degli screenshot.

Obiettivo del file:
- mantenere i prompt esatti dove presenti negli screen
- conservare anche i frame non-prompt ma operativi
- distinguere tra contenuto **verbatim**, contenuto **derivato/normalizzato**, e **uso consigliato**
- evitare che la libreria perda i pezzi importanti solo perché non erano “prompt puri”

Fonte di verità primaria:
- `03_REFERENCE/01_Trascrizione_Completa_Screenshot.md`
- `03_REFERENCE/04_SCREENSHOTS_ORIGINALI/`
- `03_REFERENCE/03_OCR_RAW/`

Legenda stato testo:
- **Completo** = il testo utile dello screen è riportato in forma sostanzialmente fedele
- **Derivato** = il contenuto è stato normalizzato o sintetizzato, ma deriva dallo screen
- **Operativo** = lo screen non contiene un prompt puro, ma una regola/workflow importante

---

## 1. Prompt esatti completi estratti dagli screenshot

### R01 — The Database Designer
**Fonte:** `Screenshot_20260423_170432_TikTok.jpg`  
**Stato:** Completo

```text
Act as a Database Administrator. I am building [App Feature]. Design the optimal relational schema for this. Include tables, foreign keys, and the exact SQL commands to create them.
```

### R02 — The Security Auditor
**Fonte:** `Screenshot_20260423_170432_TikTok.jpg`  
**Stato:** Completo

```text
Review this code snippet for security vulnerabilities. Check for SQL injection, XSS, and authentication flaws. Provide the patched code and explain the exact exploit you prevented: [Paste Code]
```

### R03 — The Technical Interviewer
**Fonte:** `Screenshot_20260423_170453_TikTok.jpg`  
**Stato:** Completo

```text
Ask me one LeetCode medium question. Do not give me the answer. Give me hints only if I ask, and evaluate my final solution.
```

### R04 — The Career Strategist
**Fonte:** `Screenshot_20260423_170453_TikTok.jpg`  
**Stato:** Completo

```text
Act as a Tech Recruiter. Review my current tech stack: [List Skills]. Tell me the top 3 high paying remote roles I should target, and rewrite my professional summary to bypass ATS filters.
```

### R05 — Build Your Brand Voice
**Fonte:** `Screenshot_20260423_170551_TikTok.jpg`  
**Stato:** Completo

```text
Study these 3 samples of my content: [paste]. Define my brand voice in clear terms: tone, vocabulary I use, topics I own, how I open posts, how I close them. Then write me a brand voice guide I can paste into any AI tool so every piece of content sounds like me, not a robot.
```

### R06 — Make Your Data Tell You What to Do
**Fonte:** `Screenshot_20260423_170556_TikTok.jpg`  
**Stato:** Completo

```text
You're a social media analyst. Here's my data: [paste]. Tell me what's working, what's killing my reach, where my content gaps are, how often I should post, and a 90-day growth plan with clear KPIs. Be specific.
```

### R08 — Hack #1 The “Caveman” Method — v1
**Fonte:** `Screenshot_20260423_170701_TikTok.jpg`  
**Stato:** Completo

```text
From now on, remove all filler words. No 'the', 'is', 'am', 'are'. Direct answer only. Use short 3–6 word sentences. Run tools first, show the result, then stop. Do not narrate. Example: Instead of 'The solution is to use async', say 'Use async'.
```

### R10 — PDF Compression Prompt — v1
**Fonte:** `Screenshot_20260423_170715_TikTok.jpg`  
**Stato:** Completo

```text
Read this document thoroughly. Remove all filler words, extra text, & formatting. Extract the core info. Return as condensed plain text with key points.
```

### R12 — Compact Skill — v1
**Fonte:** `Screenshot_20260423_170721_TikTok.jpg`  
**Stato:** Completo

```text
When I say 'COMPACT', summarize our entire conversation into 5–7 key bullet points with all critical context, decisions, & code snippets. Format for easy copy-paste into new chat.
```

### R13 — Brand Strategist and Creative Director
**Fonte:** `Screenshot_20260423_171129_TikTok.jpg`  
**Stato:** Completo

```text
You are a Brand Strategist and Creative Director who builds category-defining brands. Build a strategic brand identity for [COMPANY].

Rules:
- Treat brand as a market positioning tool, not a visual exercise
- Every decision must answer: "Why does this help the brand win?"
- No moodboards, no logo concepts without strategic rationale

Deliver in this order:
1. Competitive landscape: where visual sameness exists, what white space is available
2. Brand narrative: the tension this brand creates in the category, the belief competitors implicitly deny
3. Visual system rationale: color, type, imagery tied to market context, not general aesthetics
4. Identity behavior: how the brand flexes across ads, product, social, email
5. Decision filter: 3–5 questions any future creative must answer “yes” to

Output must read like a CMO-level strategy brief.
```

### R14 — UI/UX Systems Thinker
**Fonte:** `Screenshot_20260423_171133_TikTok.jpg`  
**Stato:** Completo

```text
You are a Senior Product Designer who optimizes for user behavior, not screen aesthetics. Design a complete experience system for [APP TYPE].

Rules:
- Design friction intentionally, some should stay, some must go
- Assume real users, incomplete data, errors, and skill variance
- No wireframes without behavioral rationale

Deliver in this order:
1. Intent mapping: primary/conflicting user intents, where friction stays vs. goes
2. Behavioral design: how hierarchy, disclosure, and motion guide decisions before users consciously choose
3. Interface systems: navigation logic, form design, all feedback states with behavioral intent
4. Edge cases: empty states, incomplete data, error recovery
5. Skill-level adaptation: what changes for new vs. power users
6. Anti-patterns: 3–5 UX decisions that look correct but damage user decision quality

Output must read like a behavioral design brief, not a UX checklist.
```

### R15 — Design Operations Specialist / Figma
**Fonte:** `Screenshot_20260423_171140_TikTok.jpg`  
**Stato:** Completo

```text
You are a Design Operations Specialist who builds Figma systems that survive team growth and product pivots. Convert [IDEA/DESIGN] into a scalable Figma system.

Rules:
- Treat Figma architecture as infrastructure, not craft
- Optimize for onboarding speed, decision speed, zero-rework updates
- Assume 3–10 designers, multiple surfaces, ongoing dev handoff

Deliver in this order:
1. System architecture: file structure logic, layer hierarchy, where decisions are made once vs. where overrides are allowed
2. Component logic: composability rules, auto-layout philosophy, variant structure, what must never be overridden locally
3. Naming system: conventions for layers, components, variables, styles, plus the logic so new designers can extend it
4. Handoff infrastructure: what every spec must include, how states and edge cases are documented in-file
5. Maintenance protocol: how breaking changes are versioned, when to deprecate vs. extend
6. Onboarding standard: what new designers must know before touching the system, the 3 most common mistakes and how to prevent them

Output must read like a systems spec, not a design handoff note.
```

### R16 — Prompt Hack: IQ score
**Fonte:** `Screenshot_20260423_171158_TikTok.jpg`  
**Stato:** Completo

```text
You're an IQ 145 specialist in marketing. Analyze my campaign.
```

### R17 — Prompt Hack: Obviously trap
**Fonte:** `Screenshot_20260423_171158_TikTok.jpg`  
**Stato:** Completo

```text
Obviously, Python is better than JavaScript for web apps, right?
```

### R18 — Prompt Hack: audience
**Fonte:** `Screenshot_20260423_171207_TikTok.jpg`  
**Stato:** Completo

```text
Explain Claude Code like you're teaching a packed auditorium
```

### R19 — Prompt Hack: fake constraint
**Fonte:** `Screenshot_20260423_171207_TikTok.jpg`  
**Stato:** Completo

```text
Explain this using only kitchen analogies
```

### R20 — AI Art Prompt Builder
**Fonte:** `Screenshot_20260423_171351_TikTok.jpg`  
**Stato:** Completo

```text
Turn this coloring page idea into a detailed AI art prompt for Leonardo or Midjourney. Make it clean line art, black and white, centered composition, high contrast, printable 8.5x11.
```

### R21 — Book Structure Prompt
**Fonte:** `Screenshot_20260423_171353_TikTok.jpg`  
**Stato:** Completo

```text
Create a full structure for a 50-page coloring book including cover title ideas, subtitle ideas, page order, bonus pages, and back cover hook.
```

### R08b — Hack #1 The “Caveman” Method — v2
**Fonte:** `Screenshot_20260423_171713_TikTok.jpg`  
**Stato:** Completo

```text
Reply in the most concise form possible. Skip pleasantries, preambles, and recaps of my question. No phrases like 'I'd be happy to', 'Great question', or 'Let me explain'. Drop articles and filler words wherever the meaning stays clear. Prefer short declarative sentences. If a tool call is needed, run it first and show only the result. Do not narrate your steps. Example: instead of 'The solution is to use async functions with proper error handling', write 'Use async with try/catch'.
```

### R10b — PDF Compression Prompt — v2
**Fonte:** `Screenshot_20260423_171725_TikTok.jpg`  
**Stato:** Completo

```text
Read this document end to end. Output a condensed plain-text version that preserves: (1) all factual claims, numbers, dates, and names; (2) every actionable instruction or recommendation; (3) the document's structure as short headings. Drop filler phrases, repeated context, marketing language, formatting artifacts, and page headers and footers. Target 20 to 30 percent of the original length. Return only the condensed text, no commentary.
```

### R12b — Compact Skill — v2
**Fonte:** `Screenshot_20260423_171732_TikTok.jpg`  
**Stato:** Completo

```text
Summarize our entire conversation so I can paste it into a new chat and continue without losing context. Include: (1) the original goal or problem, (2) key decisions made and why, (3) any code, config, or data we settled on, verbatim, in code blocks, (4) open questions and next steps. Use short sections with headings. Skip small talk and exploratory tangents. Optimize the summary for a future Claude reading it cold.
```

---

## 2. Frame operativi estratti dagli screenshot

Questa sezione conserva i frame importanti che non sono solo “prompt da copiare”, ma regole, workflow, routing o setup.

### R07 — Slash Commands
**Fonte:** `Screenshot_20260423_170612_TikTok.jpg`  
**Stato:** Derivato

Contenuto operativo:
- `/AUDIENCE` adatta la risposta a un pubblico scelto
- `/TONE` cambia il tono (formale, witty, empatico, ecc.)
- `/DEV MODE` simula uno stile tecnico grezzo da developer
- `/PM MODE` porta una prospettiva da project management
- `/SWOT` produce un’analisi strengths/weaknesses/opportunities/threats
- `/FORMAT AS` forza un formato specifico (table, XML, JSON, ecc.)
- `/COMPARE` mette due o più cose side by side
- `/MULTI-PERSPECTIVE` mostra diversi punti di vista

Uso consigliato:
- come prefissi rapidi della libreria
- come modalità del prompt madre
- come controlli di formato e prospettiva

### R06b — Cover: 7 Hacks To Stop Claude From Hitting Usage Limits Early
**Fonte:** `Screenshot_20260423_170657_TikTok.jpg`  
**Stato:** Operativo

Contenuto:
- titolo serie: `7 Hacks To Stop Claude From Hitting Usage Limits Early`
- valore: frame di contesto che unifica i successivi hack su token, routing e session management

### R09 — Code Review Graph
**Fonte:** `Screenshot_20260423_170707_TikTok.jpg`  
**Stato:** Completo

Contenuto operativo:
- Stop making Claude read your entire codebase over and over.
- Check it out: `github.com/tirth8205/code-review-graph` (Public)
- Turns your code into a structured map.
- Claude sees the structure, not every line.
- Saves 60–70% tokens on code projects.

Uso consigliato:
- repo map compressa
- contesto strutturale invece di full reread
- preflight per Claude Code

### R10 — PDF Compression Workflow — v1
**Fonte:** `Screenshot_20260423_170715_TikTok.jpg`  
**Stato:** Completo

Workflow estratto:
1. Upload the PDF to ChatGPT first
2. Use the compression prompt
3. Copy the condensed output
4. Paste into Claude

Idea chiave:
- i PDF possono mangiare gran parte della sessione
- la compressione deve avvenire prima del ragionamento profondo

### R11 — Session Timing Trick — v1
**Fonte:** `Screenshot_20260423_170719_TikTok.jpg`  
**Stato:** Completo

Contenuto operativo:
- Your 5-hour window starts with your FIRST message.
- Send a basic message 2–3 hours before you actually need Claude.
- Example:
  - 6:00 AM — send “hey”
  - 9:00 AM — start the real work
  - 11:00 AM — your window resets mid workflow
- Fresh allocation when you need it the most.

### R12 — Compact Skill Workflow — v1
**Fonte:** `Screenshot_20260423_170721_TikTok.jpg`  
**Stato:** Completo

Contenuto operativo:
- Long chats eat tokens exponentially.
- But switching chats = losing context.
- La skill “COMPACT” serve a trasferire contesto senza trascinarsi tutto il thread.

### R16/R17 — Prompt hacks context
**Fonte:** `Screenshot_20260423_171158_TikTok.jpg`  
**Stato:** Completo

Contenuto operativo:
- Assign it a random IQ score.
- The responses get wildly more sophisticated.
- Change the number, change the quality.
- Use “Obviously...” as a trap.
- It'll correct you and explain nuances instead of agreeing.
- Weaponized disagreement.

### R18/R19 — Prompt hacks context
**Fonte:** `Screenshot_20260423_171207_TikTok.jpg`  
**Stato:** Completo

Contenuto operativo:
- Pretend there's an audience.
- The structure changes, adds emphasis, examples, anticipates questions.
- Give it a fake constraint.
- Weird limitations force creative thinking and unexpected connections.

### R20 — AI Art Prompt Builder context
**Fonte:** `Screenshot_20260423_171351_TikTok.jpg`  
**Stato:** Completo

Contenuto operativo:
- Paste a page concept from Slide 3 into this prompt.
- The AI will convert it into a professional illustration prompt ready for image generation.
- Result you get:
  - High quality coloring pages
  - Consistent design style
  - Production in minutes instead of weeks

### R21 — Book Structure Prompt context
**Fonte:** `Screenshot_20260423_171353_TikTok.jpg`  
**Stato:** Completo

Contenuto operativo:
- Run this after generating your pages.
- It helps you organize the book professionally before uploading to Canva or KDP.
- Result you get:
  - Professional book layout
  - Strong branding
  - Higher conversion potential

### R22 — Build Your 4 Folders
**Fonte:** `Screenshot_20260423_171512_TikTok.jpg`  
**Stato:** Completo

Contenuto operativo:
Create a main folder called `Claude-Cowork` with these four subfolders:
- About Me — Store your identity details and writing guidelines
- Projects — Add one subfolder for each active project
- Templates — Keep your best past work for reuse
- Claude Outputs — The only folder where Claude saves new work

Uso consigliato:
- base per `95_Reference_Library`, `99_Templates`, `90_AI_Output`
- setup iniziale di un workspace AI-driven

### R23 — Stop Writing Prompts
**Fonte:** `Screenshot_20260423_171526_TikTok.jpg`  
**Stato:** Completo

Contenuto operativo:
- Instead of creating new prompts each time, use a single master template.
- Your template automatically reads the full ABOUT ME before every task.
- On Mac: set up a Text Shortcut (e.g. `/prompt`).
- Use clear file naming conventions like `project_sent_v1.ext`.
- Save work only in `CLAUDE OUTPUTS`; all other folders remain read-only.

### R24 — Let Claude Prompt You
**Fonte:** `Screenshot_20260423_171530_TikTok.jpg`  
**Stato:** Completo

Contenuto operativo:
- Turn the process around — Claude asks, you choose answers.
- Multi-select descriptions: pick options instead of writing long paragraphs.
- Multi-select & drag-to-rank: set priorities by ordering what matters most.
- Answer in under a minute: Claude builds the plan, you approve, it executes.
- “We're getting sidetracked... Generate an AskUserQuest...” — example feel of AI-assisted planning.

### R25 — Install One Plugin
**Fonte:** `Screenshot_20260423_171535_TikTok.jpg`  
**Stato:** Completo

Contenuto operativo:
- Browse available plugins to add a sidebar.
- Choose one that fits your workflow:
  - Marketing
  - Data — CSV files and dashboards / `/data:explore`
  - Legal — Contract review directly in your sidebar
- Start with just one plugin.
- Don't overload yourself — master it first, then add more.

### R26 — Connect Your Tools
**Fonte:** `Screenshot_20260423_171539_TikTok.jpg`  
**Stato:** Completo

Contenuto operativo:
- Go to `Settings > Connectors > Browse > Add`
- Connectors: Claude works directly inside your apps
- Plugins: you handle the work, Claude supports
- Claude can search your Slack, pull from your Docs, and reference Notion during tasks.
- Connect Google, Notion, and Slack — Claude becomes a teammate who understands your workflow.

### R27 — Build One Project
**Fonte:** `Screenshot_20260423_171542_TikTok.jpg`  
**Stato:** Completo

Contenuto operativo:
- Stop working with Claude alone — extend its value to your entire team.
- Create a shared Project with global instructions that benefit everyone.
- Add a subfolder for each active project containing briefs, drafts, and references.
- Claude now supports your whole team, not just you.
- One well-organized project transforms Claude from a personal assistant into a team multiplier.

### R28 — Don’t Use Opus All The Time
**Fonte:** `Screenshot_20260423_171721_TikTok.jpg`  
**Stato:** Completo

Contenuto operativo:
- Opus costs roughly 5x more per token than Sonnet.
- Use Sonnet for: code, data analysis, general Q&A, summarization.
- Use Opus for: hard architecture trade-offs, deep multi-file debugging, nuanced long-form writing.
- Use Haiku for: quick lookups, classification, formatting, high-volume simple tasks.

Uso consigliato:
- model routing
- scelta del motore in base al tipo di lavoro
- integrazione multi-AI o multi-model

### R10b — PDF Compression Workflow — v2
**Fonte:** `Screenshot_20260423_171725_TikTok.jpg`  
**Stato:** Completo

Contenuto operativo:
- Image-heavy or scanned PDFs can eat a huge chunk of your context window.
- Run the PDF through a cheaper model first (Haiku, GPT-4o mini, or any local tool).
- Use the compression prompt below.
- Paste the condensed text into your main Claude session.

### R11b — Session Timing Trick — v2
**Fonte:** `Screenshot_20260423_171729_TikTok.jpg`  
**Stato:** Completo

Contenuto operativo:
- Usage windows on Claude.ai start with your first message.
- Open your window when you're actually ready to work, not earlier.
- For long sessions, plan the start so the window doesn't expire mid-task.
- Batch your heaviest work into the first half of the window.
- Fresh allocation when you need it the most.

### R12b — Compact Skill Workflow — v2
**Fonte:** `Screenshot_20260423_171732_TikTok.jpg`  
**Stato:** Completo

Contenuto operativo:
- Long chats balloon your context window with every turn.
- Starting fresh loses everything you've built up.
- The compact summary becomes a transport layer between sessions.

### R29 — Avoid Peak Hours
**Fonte:** `Screenshot_20260423_171736_TikTok.jpg`  
**Stato:** Completo

Contenuto operativo:
- Peak load doesn't change how many tokens you spend, but raises odds of rate limits mid-task.
- Worst times to start a long session: weekdays during your region's main business hours.
- Best times for heavy work: weekends, weekday evenings, early mornings.
- Same token cost, fewer interruptions.

---

## 3. Sistema reference da usare in archivio

Ogni reference utile va archiviata così:

```text
Codice:
Titolo:
Fonte screenshot:
Categoria:
Funzione:
Prompt sorgente o contenuto operativo:
Stato del testo: completo / derivato / operativo
Uso consigliato:
Modulo collegato:
Note:
```

---

## 4. Indice reference catalogate

- R01 Database Designer
- R02 Security Auditor
- R03 Technical Interviewer
- R04 Career Strategist
- R05 Build Your Brand Voice
- R06 Make Your Data Tell You What to Do
- R07 Slash Commands
- R06b Cover: 7 Hacks To Stop Claude From Hitting Usage Limits Early
- R08 Caveman Method v1
- R09 Code Review Graph
- R10 PDF Compression Workflow v1
- R11 Session Timing Trick v1
- R12 Compact Skill v1
- R13 Brand Strategist and Creative Director
- R14 UI/UX Systems Thinker
- R15 Design Operations Specialist / Figma
- R16 Prompt Hack: IQ score
- R17 Prompt Hack: Obviously trap
- R18 Prompt Hack: audience
- R19 Prompt Hack: fake constraint
- R20 AI Art Prompt Builder
- R21 Book Structure Prompt
- R22 Build Your 4 Folders
- R23 Stop Writing Prompts
- R24 Let Claude Prompt You
- R25 Install One Plugin
- R26 Connect Your Tools
- R27 Build One Project
- R08b Caveman Method v2
- R28 Don’t Use Opus All The Time
- R10b PDF Compression Workflow v2
- R11b Session Timing Trick v2
- R12b Compact Skill v2
- R29 Avoid Peak Hours

---

## 5. Nota finale di fedeltà

Questo file ora non è più solo una raccolta di prompt “copiabili”.
È una libreria mista che conserva:
- prompt esatti
- workflow di utilizzo
- frame di setup workspace
- frame di routing modelli
- frame di efficienza sessione

Per il mirror più fedele possibile dello screenshot, usare sempre insieme:
- questo file
- `01_Trascrizione_Completa_Screenshot.md`
- gli screenshot originali
