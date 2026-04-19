# Research: MCP servers priorità per Claude Code

**Data ricerca**: 2026-04-19 (pre-setup) + decisione 2026-04-20
**Scopo**: valutare quali MCP servers installare per potenziare Claude Code
**Metodologia**: web search Anthropic docs + community lists + filtro YAGNI
**Conclusione breve**: **ZERO MCP installati**, valutazione differita

## Executive summary

**Model Context Protocol (MCP)** è lo standard Anthropic per estendere
agenti AI (Claude Code, Claude Desktop, altri) con tool esterni.

**Ecosistema MCP 2026**: molto attivo, centinaia di MCP servers open source
disponibili su GitHub, Smithery registry, Anthropic catalog.

**Decisione finale per Eduardo**: **0 MCP installati stanotte**.
Claude Code base ha già:
- File system access (read, write, edit)
- Bash execution
- Web search (via tool)
- Git operations (tramite bash + gh CLI installato)

Aggiungerò MCP **solo quando pattern specifici emergono** che Claude Code
base non copre adeguatamente.

## Cosa è MCP

**MCP** = **Model Context Protocol**, standard Anthropic pubblicato fine 2024.

**Analogia**: MCP sta a LLM come LSP (Language Server Protocol) sta a IDE.
Permette a un agente LLM di connettersi a **server** esterni che forniscono:
- Tools (azioni eseguibili)
- Resources (dati accessibili)
- Prompts (template richiesti)

**Formato**: JSON-RPC over stdio o HTTP.

**Client MCP** attuali:
- Claude Desktop
- Claude Code
- Cline (VS Code extension)
- Continue
- Zed
- (lista in crescita)

## Categorie MCP servers popolari

### Developer tools

| MCP Server | Fornitore | Funzione |
|------------|-----------|----------|
| github-mcp | GitHub | Repo, issues, PR management |
| gitlab-mcp | Community | GitLab equivalente |
| filesystem-mcp | Anthropic | File access cross-platform (alternativa a built-in) |
| git-mcp | Community | Git operations avanzate (rebase, cherry-pick assistiti) |
| sqlite-mcp | Anthropic | Query SQLite databases |
| postgres-mcp | Community | PostgreSQL access |

### Productivity / Knowledge

| MCP Server | Funzione |
|------------|----------|
| context7 | Documentation search (librerie, framework) |
| notion-mcp | Notion workspace |
| obsidian-mcp | Obsidian vault |
| gmail-mcp | Email read/write (OAuth) |
| google-calendar-mcp | Calendar access |
| supermemory | Memory/knowledge graph personale |

### Web / browsing

| MCP Server | Funzione |
|------------|----------|
| puppeteer-mcp | Browser automation headless |
| playwright-mcp | Alternative browser automation |
| fetch-mcp | HTTP fetch avanzato |
| brave-search-mcp | Search con Brave API |
| firecrawl-mcp | Web scraping structured |

### DevOps

| MCP Server | Funzione |
|------------|----------|
| docker-mcp | Docker containers management |
| kubernetes-mcp | K8s cluster operations |
| aws-mcp | AWS services (various) |
| cloudflare-mcp | Cloudflare Workers, KV, ecc. |

### Data / ML

| MCP Server | Funzione |
|------------|----------|
| pandas-mcp | Data manipulation helper |
| huggingface-mcp | HF model hub access |
| python-exec-mcp | Sandboxed Python execution |

## Community MCP server lists notable

- **Anthropic official catalog**: https://modelcontextprotocol.io/servers
- **Smithery.ai registry**: https://smithery.ai (~500+ MCP registered)
- **awesome-mcp-servers GitHub**: https://github.com/punkpeye/awesome-mcp-servers

**Growth rate** (aprile 2026): stimato ~100 nuovi MCP al mese.

## Decisione YAGNI per Eduardo (20/04/2026)

### Analisi bisogni attuali

**Task attualmente eseguiti con Claude Code**:
1. Lettura/scrittura file (✅ built-in)
2. Bash commands (✅ built-in)
3. Git operations (✅ via bash + gh CLI)
4. Edit di codice (✅ built-in)
5. Planning/strategy docs (✅ scrittura file MD)
6. Research online (✅ web_search tool di Claude)
7. Configurare Windows (✅ PowerShell via bash)

**Task NON attualmente eseguiti** (non emerge bisogno):
- Gestione issue GitHub complessa (per ora gh CLI da bash basta)
- Database queries (nessun DB attivo)
- Notion/Obsidian sync (uso Markdown puri)
- Browser automation (nessun use case)
- Docker (nessun workload container)

### Valutazione MCP candidati

**GitHub MCP** — potenzialmente utile ma YAGNI:
- Beneficio: navigazione issue/PR/repo più fluida in conversazione
- Costo: setup + OAuth + 1 altra dependency
- Attualmente: gh CLI via bash copre il 95% dei casi
- **Decisione**: rimando, aggiungerò solo se faccio issue management pesante

**Context7** — valutare in futuro:
- Beneficio: search docs di librerie (Node, Python, ecc.)
- Costo: setup + potenziale sottoscrizione
- Attualmente: web_search built-in Claude basta per ricerche doc
- **Decisione**: rimando, ideal candidate se emerge frustrazione

**Supermemory** — interessante, personal knowledge:
- Beneficio: memoria cross-sessione, RAG personale
- Costo: setup + manutenzione index
- Attualmente: memoria Claude Code + file doc in repo
- **Decisione**: rimando, ideal quando ho 6+ mesi di decisioni archiviate

**Filesystem-mcp** — NO, ridondante:
- Beneficio: alternative filesystem access
- Built-in Claude Code ha già tutto
- **Decisione**: non necessario

**SQLite-mcp** — valutare se Synesthesia DB diventa complesso:
- Beneficio: query SQLite diretto da AI
- Attualmente: nessun bisogno immediato
- **Decisione**: rimando, se emerge frustrazione con SQLite CLI

**Puppeteer/Playwright MCP** — no:
- Beneficio: browser automation
- Use case mio: zero
- **Decisione**: no

**Docker MCP** — no:
- Beneficio: container management
- Use case mio: zero (no Docker nel mio workflow)
- **Decisione**: no

### Conclusione

**0 MCP servers installati** stanotte.

Revisione periodica: mensile.
Trigger per installare: pattern specifico ripetuto >5 volte che MCP risolverebbe eleganza.

## Workflow setup (se/quando installerò MCP)

### Pattern base

```powershell
# 1. Find MCP server (GitHub, Smithery)
# 2. Install via Claude Code command:
claude mcp add <server-name>

# 3. Configure (JSON config)
# Edit ~/.claude/claude_code_config.json or equivalent

# 4. Restart Claude Code

# 5. Verify tool available:
# In conversation: "List available tools" → cercare nuovi tool da server
```

### Esempio config (hypothetical GitHub MCP)

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxx"
      }
    }
  }
}
```

## Risk analysis MCP

### Rischio 1: dependency sprawl

**Descrizione**: installare 5+ MCP = 5+ processi in background, 5+ auth,
5+ potenziali breaking update.

**Mitigation**: YAGNI severe. Minimum viable MCP count.

### Rischio 2: sicurezza

**Descrizione**: MCP server runna localmente ma può aver accesso a token,
API key, dati locali. Un MCP malicious (o compromised update) è backdoor.

**Mitigation**:
- Installa solo MCP da fonti verificate (Anthropic, org noto, >100 stars GitHub)
- Review del codice sorgente prima di install
- Pin versions (no auto-update)

### Rischio 3: lock-in

**Descrizione**: workflow dipende da MCP specifico. Se MCP deprecated
o incompatibile con nuova versione client, workflow si rompe.

**Mitigation**: documentare quale pattern MCP risolve, così posso
implementare alternative se needed.

### Rischio 4: performance overhead

**Descrizione**: ogni MCP = RPC chiamate extra, round-trip a stdio/HTTP.

**Mitigation**: misurare prima e dopo install (latency), de-installa se degradazione sensibile.

## Meta-learning

### Perché YAGNI vince su MCP ecosistema growth

MCP è ecosistema **crescente** = tentazione forte di installare "l'ultimo MCP cool".
Ma:
- Ogni nuovo MCP = cognitive load
- Molti MCP "duplicate" funzionalità esistenti (es. filesystem)
- Alcuni sono hype, non utility reale

**Filtro**: installo solo se **risolve un problema ricorrente che ho ora**,
non "potrebbe servire".

### Quando installare un MCP: checklist

**Cross-check prima di `claude mcp add`**:

1. Ho un workflow specifico che ripete >5 volte al mese?
2. Claude Code base NON copre questo workflow elegantemente?
3. Il MCP ha >100 stars GitHub (proxy reputazione)?
4. Ho letto il source o almeno il README del MCP?
5. Capisco che auth/token/permessi dà a Claude?
6. Posso tornare indietro facilmente se problematico?

Se tutti YES → install.
Se uno NO → rimanda, ri-valuta dopo 1 settimana.

### Il contrario del FOMO MCP

Vedo blog post "10 MCP servers must-have 2026". Normale reazione FOMO:
"devo installarli tutti".

Reazione YAGNI: "quale di questi risolve problema **che ho oggi**?".
Spesso la risposta è: **zero di essi**.

E va bene così.

## Fonti

- MCP official spec: https://modelcontextprotocol.io
- Anthropic docs MCP: https://docs.claude.com/en/docs/build-with-claude/model-context-protocol
- Smithery.ai registry: https://smithery.ai
- awesome-mcp-servers: https://github.com/punkpeye/awesome-mcp-servers
- GitHub MCP server: https://github.com/modelcontextprotocol/servers/tree/main/src/github
- Context7 docs: https://context7.com

## Follow-up

### Da monitorare

**Pattern di frustrazione** durante i prossimi 1-2 mesi:
- "Sarebbe bello se Claude potesse fare X senza bash boilerplate" → MCP candidato
- "Copio-incollo troppo Y" → MCP candidato
- "Manca contesto su Z" → MCP candidato

Se un pattern ricorre, valuto MCP specifico.

### Prossima revisione

**Fine maggio 2026** (fine Claude Max): valutare se MCP avrebbero fatto differenza
qualitativa nella transizione a Ollama/OpenRouter.

### Scenari hypothetical di installazione

**Se implemento RAG personale** (knowledge base propria):
→ Supermemory MCP o custom MCP su Obsidian vault

**Se Evo-Tactics diventa collaborativo** (team):
→ GitHub MCP per issue management fluido

**Se aggiungo Mac mini + Lenovo sync**:
→ Syncthing MCP o custom per sync context cross-device

**Se Synesthesia DB cresce**:
→ SQLite MCP per query rapide senza context switching
