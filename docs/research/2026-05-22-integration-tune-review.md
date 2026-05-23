# Integration Tune Review — 2026-05-22

## Stato after fixes

| Componente | Stato | Note |
|---|---|---|
| Dashboard dogfood-ui | ✅ LIVE `:8080` | 34 test pass, health endpoint arricchito |
| LiteLLM | ✅ LIVE `:4000` | v1.82.6, DB connesso, callbacks Langfuse attivi |
| Langfuse | ✅ LIVE `:3000` | v2.95.11, reachable via dashboard |
| Postgres | ✅ UP (healthy) | Condiviso LiteLLM + Langfuse |
| OpenCode keys.env validation | ✅ DONE | script validate-only (no write) — schema 1.15.x non supporta `env` top-level |
| Tavily env detection | ✅ DONE | letto direttamente da `keys.env` standard path |
| NotebookLM auth | ⏸️ BLOCKED | Eduardo OAuth su Lenovo `.10` |

## Post-mortem 2026-05-23 — Bug OpenCode `env` top-level

**Cosa è successo**: script `sync-opencode-api-env.ps1 -Apply` ha scritto `"env": "...keys.env"` in `opencode.jsonc`, ma OpenCode 1.15.x **non riconosce quel campo**. Conseguenza: `opencode debug config` → `Unrecognized key: env`, OpenCode Desktop crashava al model picker.

**Anti-pattern attivato (#9)**: DRY-RUN dello script validava solo che le chiavi esistessero in keys.env — non eseguiva OpenCode per validare la config scritta. L'apply ha shipato un file che il consumer rifiuta.

**Fix da Codex (2026-05-23 01:33)**:
- `opencode.jsonc` ripristinato (solo `$schema`) da backup `opencode.jsonc.bak-20260522225042`
- file rotto isolato come `opencode.jsonc.bad-20260523013327`
- script `sync-opencode-api-env.ps1` neutralizzato: dry-run validate-only, `-Apply` rifiuta esplicitamente

**Refactor dashboard (questa sessione, 2026-05-23)**: la detection `providers` + tavily fallback non dipende più dal campo `env` (inesistente). Aggiunta costante `API_KEYS_FILE` con default `~/.config/api-keys/keys.env`, scansionata direttamente. Campo health rinominato `uses_api_keys_env_file` → `api_keys_file_present` (semantica onesta: file sul disco, non binding OpenCode).

**Lezione**: schema-validation del consumer è parte obbligatoria del QG Step-1 quando lo script scrive config per quel consumer. Per OpenCode/CLI con `debug config`: `opencode debug config` dopo Apply su sandbox config-dir prima di Apply al `~/.config/`. Da aggiungere come anti-pattern checklist quando si automatizza writes a config tool-specifici.

## Bug trovati e fixati

1. **MEDIUM — `uses_api_keys_env_file` sempre False su Windows** (`apps/dogfood-ui/app.py:453`)
   - Causa: `str.endswith("api-keys/keys.env")` con forward slash → Windows path usa backslash
   - Fix: usato `Path(env_file).parts` per controllo cross-platform

2. **MEDIUM — `ping()` e `health()` semanticamente identiche** (`apps/dogfood-ui/langfuse_client.py:24-37`)
   - Causa: refactor ha fatto delegare `ping()` a `health()` perdendo validazione auth
   - Fix: `ping()` ora usa endpoint autenticato (`/api/public/traces`) per validare reachability + credentials; `health()` resta pubblica senza auth

## Tuning raccomandati (non bloccanti)

### 1. OpenCode provider entries mancanti
- **Cosa**: `opencode.jsonc` ha solo `env` + `$schema`, zero provider entries
- **Perché**: Funziona — le chiavi vengono da `keys.env`
- **Tuning**: Se si vuole visibilità nel dashboard, aggiungere provider entries a `opencode.jsonc` con la sintassi `{ "type": "ollama", "apiBase": "http://...", "models": [...] }` per popolare `providers_count` nel health endpoint. Opzionale — non serve per funzionamento.

### 2. TAVILY_API_KEY in docker-compose: dead env var in LiteLLM
- **Cosa**: `infra/docker-compose.yml:32` passa `TAVILY_API_KEY` al container LiteLLM, ma `litellm/config.yaml` non lo referenzia
- **Fix**: o (a) rimuovere dal compose se non serve a LiteLLM, o (b) aggiungere un model entry Tavily in `config.yaml` se si vuole routing via LiteLLM. Raccomandato (a) ora, (b) quando serve Tavily via proxy.
- **Azione**: eliminare la riga da `docker-compose.yml` e da `.env.example` se non ci sono piani immediati per Tavily via LiteLLM.

### 3. Tavily non usabile via dashboard
- **Cosa**: `tavily.configured: false` nel health endpoint perché `TAVILY_API_KEY` non è nel process env del Flask
- **Root cause**: la dashboard legge `os.environ.get("TAVILY_API_KEY")` ma l'env var è in `keys.env`, non nel shell del processo
- **Tuning**: se serve Tavily via dashboard, o (a) precaricare `keys.env` prima di lanciare `python app.py`, o (b) far leggere alla dashboard da `keys.env` direttamente con fallback (come fa per OpenCode config)

### 4. Nessun integration test end-to-end
- **Cosa**: 29 test unit/hermetic, ma nessun test che verifichi dashboard + LiteLLM + Langfuse insieme
- **Tuning**: aggiungere un integration script `scripts/smoke/infra-smoke.ps1` che:
  1. Verifichi health endpoint dashboard (`:8080/api/health`)
  2. Verifichi LiteLLM readiness (`:4000/health/readiness`)
  3. Verifichi Langfuse health (`:3000/api/public/health`)
  4. Faccia una chiamata proxy a un model via LiteLLM (es. `/chat/completions` con ollama locale)
  5. Verifichi che la trace appaia in Langfuse

### 5. Dashboard process lifecycle
- **Cosa**: Flask in dev mode su `:8080` è stato avviato/fermato più volte con workaround (batch file, .NET Process)
- **Tuning**: sostituire con un wrapper robusto `scripts/setup/start-dashboard.ps1` che:
  - Sorgente `keys.env` nelle env vars del processo
  - Usi `waitress` o `gunicorn` (production WSGI) invece di Flask dev server
  - Logghi a file timestampato
  - Esponga comandi `start`, `stop`, `restart`, `status`

### 6. .env infra: keys in chiaro
- **Cosa**: `infra/.env` contiene API keys in chiaro (gitignored ma su filesystem locale)
- **Tuning**: sostituire con script wrapper `scripts/setup/start-infra.ps1` che source keys.env e lancia `docker compose up` con env passate, senza .env file

### 7. Coverage test per health/ping contract
- **Cosa**: nessun test verifica che `health()` vs `ping()` abbiano semantiche diverse
- **Tuning**: aggiungere test in `tests/test_langfuse_client.py` che mockano HTTP e verificano:
  - `health()` chiama `/api/public/health` (no auth header)
  - `ping()` chiama `/api/public/traces` (con auth header)
  - `ping()` ritorna False quando keys sono vuote
