# Estrazione testo screenshot - trascrizione ordinata

Nota: ho corretto solo errori OCR evidenti. Dove il testo nello screenshot è realmente tagliato o poco leggibile, l'ho segnato come `[parte tagliata/illeggibile]` invece di inventarlo.

## 1. Screenshot_20260423_170432_TikTok.jpg
**Blue Viper — @blueviper.ai — 4/1**

**5. The Database Designer**  
Bad data structures ruin good apps.

**Prompt:**  
"Act as a Database Administrator. I am building [App Feature]. Design the optimal relational schema for this. Include tables, foreign keys, and the exact SQL commands to create them."

**6. The Security Auditor**  
Do not let your app get hacked on day one.

**Prompt:**  
"Review this code snippet for security vulnerabilities. Check for SQL injection, XSS, and authentication flaws. Provide the patched code and explain the exact exploit you prevented: [Paste Code]"

---

## 2. Screenshot_20260423_170453_TikTok.jpg
**Blue Viper — @blueviper.ai — 10/1**

**17. The Technical Interviewer**  
Practice makes perfect.

**Prompt:**  
"Ask me one LeetCode medium question. Do not give me the answer. Give me hints only if I ask, and evaluate my final solution."

**18. The Career Strategist**  
Your skills mean nothing if you cannot sell them.

**Prompt:**  
"Act as a Tech Recruiter. Review my current tech stack: [List Skills]. Tell me the top 3 high paying remote roles I should target, and rewrite my professional summary to bypass ATS filters."

---

## 3. Screenshot_20260423_170551_TikTok.jpg
**9/8**

**Build Your Brand Voice**

"Study these 3 samples of my content: [paste]. Define my brand voice in clear terms: tone, vocabulary I use, topics I own, how I open posts, how I close them. Then write me a brand voice guide I can paste into any AI tool so every piece of content sounds like me, not a robot."

---

## 4. Screenshot_20260423_170556_TikTok.jpg
**7?/8**

**Make Your Data Tell You What to Do**

"You're a social media analyst. Here's my data: [paste]. Tell me what's working, what's killing my reach, where my content gaps are, how often I should post, and a 90-day growth plan with clear KPIs. Be specific."

---

## 5. Screenshot_20260423_170612_TikTok.jpg
**9–16**

9. **/AUDIENCE** adapts the response to a chosen audience.  
10. **/TONE** changes the tone (formal, witty, empathetic, etc.).  
11. **/DEV MODE** simulates a raw, technical developer style.  
12. **/PM MODE** gives a project-management perspective.  
13. **/SWOT** produces a strengths/weaknesses/opportunities/threats analysis.  
14. **/FORMAT AS** enforces a specific format (table, XML, JSON, etc.).  
15. **/COMPARE** puts two or more things side by side.  
16. **/MULTI-PERSPECTIVE** shows several points of view.

---

## 6. Screenshot_20260423_170657_TikTok.jpg
**7 Hacks To Stop Claude From Hitting Usage Limits Early**

@okaashish

---

## 7. Screenshot_20260423_170701_TikTok.jpg
@okaashish

**Hack #1 — The “Caveman” Method**

- Make Claude talk like a caveman.  
- No filler. No yapping. Direct answers.

**Use this prompt:**

"From now on, remove all filler words. No 'the', 'is', 'am', 'are'. Direct answer only. Use short 3–6 word sentences. Run tools first, show the result, then stop. Do not narrate. Example: Instead of 'The solution is to use async', say 'Use async'."

- This will save ~40% tokens per response.

---

## 8. Screenshot_20260423_170707_TikTok.jpg
@okaashish

**Hack #3 — Code Review Graph**

Stop making Claude read your entire codebase over and over.

Check it out:

`github.com/tirth8205/code-review-graph` (Public)

Turns your code into a structured map.  
Claude sees the structure, not every line.  
Saves 60–70% tokens on code projects.

---

## 9. Screenshot_20260423_170715_TikTok.jpg
@okaashish

**Hack #4 — [Don't Upload PDFs] Directly To Claude**

PDFs can consume 80% of your session.

So do this instead:
1. Upload the PDF to ChatGPT first  
2. Use this prompt:

"Read this document thoroughly. Remove all filler words, extra text, & formatting. Extract the core info. Return as condensed plain text with key points."

3. Copy the output given by ChatGPT  
4. Paste into Claude

---

## 10. Screenshot_20260423_170719_TikTok.jpg
@okaashish

**Hack #5 — The Session Timing Trick**

Your 5-hour window starts with your FIRST message. So follow this trick:

Send a basic message 2–3 hours before you actually need Claude. For example:
- 6:00 AM — Send something like “hey”
- 9:00 AM — Start the real work
- 11:00 AM — Your window resets mid workflow

- Fresh allocation when you need it the most.

---

## 11. Screenshot_20260423_170721_TikTok.jpg
@okaashish

**Hack #6 — Create a “Compact” Skill**

- Long chats eat tokens exponentially.  
- But switching chats = losing context.

**Create this skill:**

"When I say 'COMPACT', summarize our entire conversation into 5–7 key bullet points with all critical context, decisions, & code snippets. Format for easy copy-paste into new chat."

- This creates a Compact Conversation Skill.

---

## 12. Screenshot_20260423_171129_TikTok.jpg
**You are a Brand Strategist and Creative Director who builds category-defining brands. Build a strategic brand identity for [COMPANY].**

**Rules:**
- Treat brand as a market positioning tool, not a visual exercise
- Every decision must answer: "Why does this help the brand win?"
- No moodboards, no logo concepts without strategic rationale

**Deliver in this order:**
1. Competitive landscape: where visual sameness exists, what white space is available
2. Brand narrative: the tension this brand creates in the category, the belief competitors implicitly deny
3. Visual system rationale: color, type, imagery tied to market context, not general aesthetics
4. Identity behavior: how the brand flexes across ads, product, social, email
5. Decision filter: 3–5 questions any future creative must answer “yes” to

Output must read like a CMO-level strategy brief.

---

## 13. Screenshot_20260423_171133_TikTok.jpg
**UI/UX SYSTEMS THINKER**

**You are a Senior Product Designer who optimizes for user behavior, not screen aesthetics. Design a complete experience system for [APP TYPE].**

**Rules:**
- Design friction intentionally, some should stay, some must go
- Assume real users, incomplete data, errors, and skill variance
- No wireframes without behavioral rationale

**Deliver in this order:**
1. Intent mapping: primary/conflicting user intents, where friction stays vs. goes
2. Behavioral design: how hierarchy, disclosure, and motion guide decisions before users consciously choose
3. Interface systems: navigation logic, form design, all feedback states with behavioral intent
4. Edge cases: empty states, incomplete data, error recovery
5. Skill-level adaptation: what changes for new vs. power users
6. Anti-patterns: 3–5 UX decisions that look correct but damage user decision quality

Output must read like a behavioral design brief, not a UX checklist.

---

## 14. Screenshot_20260423_171140_TikTok.jpg
**You are a Design Operations Specialist who builds Figma systems that survive team growth and product pivots. Convert [IDEA/DESIGN] into a scalable Figma system.**

**Rules:**
- Treat Figma architecture as infrastructure, not craft
- Optimize for onboarding speed, decision speed, zero-rework updates
- Assume 3–10 designers, multiple surfaces, ongoing dev handoff

**Deliver in this order:**
1. System architecture: file structure logic, layer hierarchy, where decisions are made once vs. where overrides are allowed
2. Component logic: composability rules, auto-layout philosophy, variant structure, what must never be overridden locally
3. Naming system: conventions for layers, components, variables, styles, plus the logic so new designers can extend it
4. Handoff infrastructure: what every spec must include, how states and edge cases are documented in-file
5. Maintenance protocol: how breaking changes are versioned, when to deprecate vs. extend
6. Onboarding standard: what new designers must know before touching the system, the 3 most common mistakes and how to prevent them

Output must read like a systems spec, not a design handoff note.

---

## 15. Screenshot_20260423_171158_TikTok.jpg
**PROMPT 2 — 3/7**

2. **Assign it a random IQ score. This is absolutely ridiculous but:**

"You're an IQ 145 specialist in marketing. Analyze my campaign."

The responses get wildly more sophisticated. Change the number, change the quality. 130? Decent. 160? It starts citing principles you've never heard of.

3. **Use “Obviously...” as a trap**

"Obviously, Python is better than JavaScript for web apps, right?"

It'll actually CORRECT you and explain nuances instead of agreeing. Weaponized disagreement.

---

## 16. Screenshot_20260423_171207_TikTok.jpg
**PROMPT 4 — 4/7**

4. **Pretend there's an audience**

"Explain Claude Code like you're teaching a packed auditorium"

The structure completely changes. It adds emphasis, examples, even anticipates questions. Way better than "explain clearly."

5. **Give it a fake constraint**

"Explain this using only kitchen analogies"

Forces creative thinking. The weird limitation makes it find unexpected connections. Works with any random constraint (sports, movies, nature, whatever).

---

## 17. Screenshot_20260423_171351_TikTok.jpg
**Drew Huibregtse — Prompt 4 (AI Art Prompt Builder)**

Paste a page concept from Slide 3 into this prompt. The AI will convert it into a professional illustration prompt ready for image generation.

Turn this coloring page idea into a detailed AI art prompt for Leonardo or Midjourney. Make it clean line art, black and white, centered composition, high contrast, printable 8.5x11.

**Result you get:**
- High quality coloring pages
- Consistent design style
- Production in minutes instead of weeks

---

## 18. Screenshot_20260423_171353_TikTok.jpg
**Drew Huibregtse — Prompt 5 (Book Structure Prompt)**

Create a full structure for a 50-page coloring book including cover title ideas, subtitle ideas, page order, bonus pages, and back cover hook.

**How to use it:**
Run this after generating your pages. It helps you organize the book professionally before uploading to Canva or KDP.

**Result you get:**
- Professional book layout
- Strong branding
- Higher conversion potential

---

## 19. Screenshot_20260423_171512_TikTok.jpg
**Build Your 4 Folders**

Create a main folder called **Claude-Cowork** with these four subfolders:

- **About Me** — Store your identity details and writing guidelines
- **Projects** — Add one subfolder for each active project
- **Templates** — Keep your best past work for reuse
- **Claude Outputs** — The only folder where Claude saves new work

---

## 20. Screenshot_20260423_171526_TikTok.jpg
**Stop Writing Prompts**

Instead of creating new prompts each time, use a single master template. It will always load your context.

- Your template automatically reads the full ABOUT ME before every task
- On Mac: set up a Text Shortcut (e.g. type `/prompt` to expand it anywhere)
- Use clear file naming conventions like `project_sent_v1.ext`
- Save work only in **CLAUDE OUTPUTS** — all other folders remain read-only

---

## 21. Screenshot_20260423_171530_TikTok.jpg
**Let Claude Prompt You**

Turn the process around — Claude asks, you choose answers.

- **Multi-select descriptions:** pick options instead of writing long paragraphs
- **Multi-select & drag-to-rank:** set priorities by ordering what matters most
- **Answer in under a minute:** Claude builds the plan, you approve, it executes

"We're getting sidetracked... Generate an AskUserQuest..." — That's what effective AI-assisted planning feels like.

---

## 22. Screenshot_20260423_171535_TikTok.jpg
**Install One Plugin**

Browse available plugins to add a sidebar. Choose one that fits your workflow:

- **Marketing**
- **Data** — CSV files and dashboards / `/data:explore`
- **Legal** — Contract review directly in your sidebar

Start with just one plugin. Don't overload yourself — master it first, then add more.

---

## 23. Screenshot_20260423_171539_TikTok.jpg
**Connect Your [Tools]**

Go to **Settings > Connectors > Browse > Add**

**Connectors**  
Claude works directly inside your apps

**Plugins**  
You handle the work, Claude supports

Claude can search your Slack, pull from your Docs, and reference Notion during tasks.

Connect Google, Notion, and Slack — Claude becomes a teammate who understands your workflow.

---

## 24. Screenshot_20260423_171542_TikTok.jpg
**Build One Project**

Stop working with Claude alone — extend its value to your entire team.

- Create a shared Project with global instructions that benefit everyone
- Add a subfolder for each active project containing briefs, drafts, and references
- Claude now supports your whole team, not just you

One well-organized project transforms Claude from a personal assistant into a team multiplier.

---

## 25. Screenshot_20260423_171713_TikTok.jpg
**Evolving AI — Hack #1 The “Caveman” Method**

- Make Claude talk like a caveman
- No filler. No preamble. Direct answers

**Use this prompt:**

"Reply in the most concise form possible. Skip pleasantries, preambles, and recaps of my question. No phrases like 'I'd be happy to', 'Great question', or 'Let me explain'. Drop articles and filler words wherever the meaning stays clear. Prefer short declarative sentences. If a tool call is needed, run it first and show only the result. Do not narrate your steps. Example: instead of 'The solution is to use async functions with proper error handling', write 'Use async with try/catch'."

Cuts roughly 30 to 50 percent of output tokens on conversational replies.

---

## 26. Screenshot_20260423_171721_TikTok.jpg
**Evolving AI — Hack #3 Don’t Use Opus All The Time**

- Opus costs roughly 5x more per token than Sonnet. Same answer, much higher bill
- Use **Sonnet** for: code, data analysis, general Q&A, summarization
- Use **Opus** for: hard architecture trade-offs, deep multi-file debugging, nuanced long-form writing
- Use **Haiku** for: quick lookups, classification, formatting, high-volume simple tasks

---

## 27. Screenshot_20260423_171725_TikTok.jpg
**Evolving AI — Hack #4 Don’t Upload PDFs Directly To Claude**

Image-heavy or scanned PDFs can eat a huge chunk of your context window. So do this instead:

- Run the PDF through a cheaper model first (Haiku, GPT-4o mini, or any local tool)
- Use the prompt below to compress it
- Paste the condensed text into your main Claude session

**Use this prompt:**

"Read this document end to end. Output a condensed plain-text version that preserves: (1) all factual claims, numbers, dates, and names; (2) every actionable instruction or recommendation; (3) the document's structure as short headings. Drop filler phrases, repeated context, marketing language, formatting artifacts, and page headers and footers. Target 20 to 30 percent of the original length. Return only the condensed text, no commentary."

---

## 28. Screenshot_20260423_171729_TikTok.jpg
**Evolving AI — Hack #5 The Session Timing Trick**

Usage windows on Claude.ai start with your first message. The clock is already ticking the moment you say "hey."

- Open your window when you're actually ready to work, not earlier
- For long sessions, plan the start so the window doesn't expire mid-task
- Batch your heaviest work into the first half of the window

Fresh allocation when you need it the most.

---

## 29. Screenshot_20260423_171732_TikTok.jpg
**Evolving AI — Hack #6 Create a “Compact” Skill**

- Long chats balloon your context window with every turn
- Starting fresh loses everything you've built up

**Use this prompt:**

"Summarize our entire conversation so I can paste it into a new chat and continue without losing context. Include: (1) the original goal or problem, (2) key decisions made and why, (3) any code, config, or data we settled on, verbatim, in code blocks, (4) open questions and next steps. Use short sections with headings. Skip small talk and exploratory tangents. Optimize the summary for a future Claude reading it cold."

This creates a Compact Conversation Skill.

---

## 30. Screenshot_20260423_171736_TikTok.jpg
**Evolving AI — Hack #7 Avoid Peak Hours**

Peak load doesn't change how many tokens you spend, but it raises your odds of hitting rate limits mid-task.

- Worst times to start a long session: weekdays during your region's main business hours
- Best times for heavy work: weekends, weekday evenings, early mornings

Same token cost, fewer interruptions.
