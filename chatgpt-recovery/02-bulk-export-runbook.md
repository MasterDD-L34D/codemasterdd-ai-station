# Bulk Export Runbook -- 2026-05-14

Procedure ordinate post-audit. Esegui sequenzialmente.

---

## Step 1: Setup brianjlacy/export-chatgpt (5 min, una sola volta)

```powershell
# Clone in workspace persistente (NON nel worktree codemasterdd)
cd C:\dev
git clone https://github.com/brianjlacy/export-chatgpt.git
cd export-chatgpt
npm install

# Verify
npx export-chatgpt --help
```

Atteso output: lista flag con `--include-archived`, `--projects-only`, `--no-canvas`, ecc.

---

## Step 2: Smoke test (15 min)

Goal: validare output structure + token funziona, su un singolo project piccolo PRIMA del full run.

```powershell
# Token estratto da DevTools (vedi audit sezione I)
$env:CHATGPT_BEARER_TOKEN = "eyJ..."  # YOUR JWT HERE

cd C:\dev\export-chatgpt

# Smoke test: solo projects (skippa regular conversations per ora)
# Nota: --throttle e' in SECONDS (default 60s). Adaptive throttle ON by default,
# scala da --throttle (start) verso --min-throttle 5 con sustained success.
# Per smoke test acceleriamo manualmente: --throttle 5 + adaptive auto-adjust.
npx export-chatgpt `
  --projects-only `
  --output ./smoke-test `
  --throttle 5 `
  --no-user-dir `
  --verbose
```

**Validation checklist post-smoke**:
- [ ] `smoke-test/projects/project-index.json` esiste con N projects
- [ ] `smoke-test/projects/{ProjectName}/json/*.json` contiene file
- [ ] Apri 1 JSON: verifica presenza `mapping` tree + `gizmo_id` + `title` + `create_time`
- [ ] `smoke-test/projects/{ProjectName}/markdown/*.md` esiste
- [ ] Apri 1 MD: verifica YAML frontmatter + sezioni `## User` / `## Assistant`
- [ ] Confronta titolo + timestamp ultimo messaggio MD vs UI ChatGPT (manual cross-check 1 conv)
- [ ] Se DALL-E images presenti: verifica `smoke-test/projects/{ProjectName}/files/*.png` scaricate

**Go/no-go**:
- ✅ Tutti check passati -> proceed Step 3 full export
- ❌ Token expired (401) -> refresh token, re-run smoke (same command, riprende da cursor)
- ❌ Output structure inattesa -> investiga, NON proceed full (corruzione potenziale)
- ❌ Files non scaricati -> aggiungi `--verbose`, controlla rate-limit messages

Cancella `smoke-test/` dopo validation (sara' duplicato di full run).

---

## Step 3: Full bulk export (30-60 min)

```powershell
# Token refresh se passati >30 min da estrazione (precauzione)
# Re-extract da DevTools se necessario

$env:CHATGPT_BEARER_TOKEN = "eyJ..."  # FRESH TOKEN

cd C:\dev\export-chatgpt

# Full run: regular + projects + archived + tutti files
# --throttle 8 = start con 8s tra request, adaptive scala su/giu' [5-300s]
# --no-user-dir = output flat (senza subdir user-id, piu' pulito per ingest)
npx export-chatgpt `
  --include-archived `
  --output ./full-export-2026-05-14 `
  --throttle 8 `
  --no-user-dir `
  --verbose 2>&1 | Tee-Object -FilePath ./export.log
```

**Note**:
- `Tee-Object` salva log a file + mostra stdout. Utile per debug se interruzioni.
- Token expiration mid-run: tool salva progress in `.export-progress.json`, re-run con `$env:CHATGPT_BEARER_TOKEN = "<fresh>"` e stesso comando = resume da cursor.
- Rate limit 429: backoff exponential automatico, max 3 retry per request. Se persistente -> aumenta `--delay 3500`.
- Disk usage previsto: 100MB-3GB dipende da DALL-E + uploads volume.

**Monitor durante run**:
```powershell
# In altra finestra PowerShell, watch progress (refresh ogni 5s)
while ($true) {
    Clear-Host
    Get-Content C:\dev\export-chatgpt\full-export-2026-05-14\.export-progress.json -Raw | ConvertFrom-Json | Select-Object indexingComplete, lastOffset, projectsIndexingComplete
    Start-Sleep 5
}
```

---

## Step 4: MemPort Memory items (10 min)

1. Install **MemPort** Chrome extension:
   - URL: `https://chromewebstore.google.com/detail/memport-%E2%80%93-chatgpt-memory/cmjmnopfdophhnfnfeflgmlfifahnbie`
   - Add to Chrome (free, 100% local processing)

2. In ChatGPT loggato:
   - Settings (avatar) -> Personalization -> Memory -> "Manage memories"
   - Si apre modal "Saved memories"
   - Click icona MemPort (toolbar Chrome) o pulsante in-page se appare
   - Click "Export CSV"
   - Salva come `C:\dev\export-chatgpt\full-export-2026-05-14\memory-items-2026-05-14.csv`

3. Verify CSV: aprire in Excel/Notepad, verificare colonne (typical: `id`, `text`, `created_at`).

---

## Step 5: Custom Instructions manual (5 min)

1. ChatGPT Settings -> Personalization -> Custom Instructions
2. Copy textarea 1: "What would you like ChatGPT to know about you"
3. Copy textarea 2: "How would you like ChatGPT to respond"
4. Salva come `C:\dev\export-chatgpt\full-export-2026-05-14\custom-instructions-2026-05-14.md`:

```markdown
# Custom Instructions Export -- 2026-05-14

## About you (textarea 1)
[paste here]

## Response style (textarea 2)
[paste here]
```

---

## Step 6: Custom GPTs (Path B Playwright)

Solo se path B scelto in audit sezione E.

```powershell
cd C:\dev\codemasterdd-ai-station\chatgpt-recovery\scripts

# Setup una volta sola
.\setup-playwright.ps1

# Run scrape
node scrape-custom-gpts.js `
  --output C:\dev\export-chatgpt\full-export-2026-05-14\custom-gpts `
  --delay 2000
```

Vedere `scripts/scrape-custom-gpts.js` per dettaglio + flag.

---

## Step 7: Staging to vault (5 min)

```powershell
# Decide vault destination path (sovereign-only sibling-peer)
# Lenovo clone: C:\dev\vault-shared\
# Ryzen origin: C:\Users\VGit\Vault\ (via SSH se vuoi sync remoto)

$exportSrc = "C:\dev\export-chatgpt\full-export-2026-05-14"
$vaultDest = "C:\dev\vault-shared\Sources\raw\chatgpt-export-2026-05-14"

# Crea destination
New-Item -ItemType Directory -Path $vaultDest -Force

# Copy con preserve attributes
robocopy $exportSrc $vaultDest /E /COPY:DAT /R:3 /W:5 /LOG:$vaultDest\_meta\copy.log

# Verify count
$srcCount = (Get-ChildItem $exportSrc -Recurse -File).Count
$dstCount = (Get-ChildItem $vaultDest -Recurse -File).Count
"Source: $srcCount files | Destination: $dstCount files"
```

**Reminder boundary**: vault-shared e' sibling-peer NO-WRITE default da codemasterdd. Per questa operazione Eduardo media write esplicito (override per-task pattern L-012 vault-shared sibling-peer write under explicit authorization).

---

## Step 8: Classification pipeline (vedere `pipeline/classify.py`)

```powershell
cd C:\dev\codemasterdd-ai-station\chatgpt-recovery\pipeline
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run classification
python classify.py `
  --input C:\dev\vault-shared\Sources\raw\chatgpt-export-2026-05-14 `
  --output C:\dev\vault-shared\Sources\processed\chatgpt-2026-05-14 `
  --embed-model nomic-embed-text `
  --label-model qwen2.5-coder:14b-instruct-q2_K
```

---

## Troubleshooting common errors

| Error | Cause | Fix |
|---|---|---|
| `401 Unauthorized` | Token JWT expired | Refresh token da DevTools, re-run same command |
| `403 Forbidden` | Account ID missing (Teams) | Aggiungi `--account-id <UUID>` flag |
| `429 Too Many Requests` persistent | Rate-limit hit | Adaptive throttle gestisce auto, ma se persiste pausa 5 min + aumenta `--throttle 30` |
| `ENOENT` su files | Path Windows con spazi | Quote path `"C:\path with space\..."` |
| Progress file corrupt | Crash mid-write | Cancella `.export-progress.json`, re-run from scratch |
| `Cloudflare challenge` | Cloudflare bot detection | Issue #19 brianjlacy open, fallback: pausa lunga (10 min) e retry, o disable `--no-adaptive-throttle` con `--throttle 60` fixed |

---

## Post-export cleanup

```powershell
# Verifica completezza export
$exportRoot = "C:\dev\export-chatgpt\full-export-2026-05-14"

"=== Export summary ==="
"Regular conversations: $((Get-ChildItem $exportRoot\json -Filter *.json -ErrorAction SilentlyContinue).Count)"
"Projects: $((Get-ChildItem $exportRoot\projects -Directory -ErrorAction SilentlyContinue | Where-Object Name -ne '_meta').Count)"
"Total Markdown: $((Get-ChildItem $exportRoot -Filter *.md -Recurse).Count)"
"Total JSON: $((Get-ChildItem $exportRoot -Filter *.json -Recurse).Count)"
"Total files: $((Get-ChildItem $exportRoot\files -ErrorAction SilentlyContinue).Count + (Get-ChildItem $exportRoot\projects\*\files -ErrorAction SilentlyContinue).Count)"
"Disk usage: $([math]::Round((Get-ChildItem $exportRoot -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB, 2)) MB"
```

**Backup raccomandato**: prima di Phase 3 classification, fare backup tarball di `exports/`:
```powershell
Compress-Archive -Path $exportRoot -DestinationPath "$exportRoot-backup.zip" -CompressionLevel Optimal
```

Se classification corrompe qualcosa = restore in 1 min.
