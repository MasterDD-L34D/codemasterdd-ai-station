# Pre-flight Audit Checklist UI -- 2026-05-14

**Tempo stimato**: 10-15 min. Da eseguire PRIMA del bulk export. Output: decisioni informate su scope reale + scelta path Custom GPTs (manual vs Playwright).

**Pre-req**:
- Browser desktop loggato a workspace ChatGPT Business "Area di lavoro di Master DD Business"
- DevTools accessibile (F12)

---

## A. Verifica workspace attivo

1. [ ] Apri `https://chatgpt.com`
2. [ ] In alto a sinistra: clicca avatar/nome workspace
3. [ ] Conferma workspace selezionato = "Area di lavoro di Master DD Business" (NON "Personal")
4. [ ] Compila: workspace name visibile = `_______________________________`
5. [ ] Compila: tuo ruolo nel workspace (Owner / Admin / Member) = `_______`

**Decisione**: se NON sei Owner/Admin del workspace, alcune API responses potrebbero essere ristrette. Procedi comunque, brianjlacy fetcha solo le TUE conversations comunque.

---

## B. Conta Projects (cartelle "Progetti")

1. [ ] Nella sidebar sinistra cerca sezione "Progetti" (o "Projects")
2. [ ] Conta totale Projects visibili: N = `___`
3. [ ] Lista Project names (sanitizzati per filename, max 50 char ognuno):
   - [ ] `_____________________________________`
   - [ ] `_____________________________________`
   - [ ] `_____________________________________`
   - [ ] `_____________________________________`
   - [ ] (aggiungi righe se >4)

**Target verifica primaria**: presenza di "Progetto Gioco Evo Tactics" (o nome simile contenente "Evo Tactics") = SI / NO

4. [ ] Per ogni Project, click brevemente per stimare # conversations dentro:
   - Project 1 (`_____________________`): ~`___` conversations
   - Project 2 (`_____________________`): ~`___` conversations
   - (continua)

5. [ ] Totale conversations dentro Projects stimato: `___`

---

## C. Conta chat regolari (non-project)

1. [ ] Sidebar sinistra sezione "Chat" o lista cronologica
2. [ ] Scroll completo verso il basso, conta approssimativamente: `___` chat
3. [ ] Range temporale (data prima chat visibile - data ultima): `_________` - `_________`

**Decisione throttle**: se totale chat (regular + projects) > 500, considera aumentare `--delay 3000` invece di 2500.

---

## D. Conta chat archiviate

1. [ ] Settings (icona ingranaggio) -> "Data Controls" -> "Archived Chats"
2. [ ] Conta totale archiviate: `___`

**Decisione flag**: se > 0 -> usa flag `--include-archived` nel bulk export. Default OpenAI esclude le archiviate silenziosamente.

---

## E. Audit Custom GPTs

1. [ ] Sidebar sinistra cerca "Esplora GPT" (o "Explore GPTs") + sezione "I miei GPT" (o "My GPTs")
2. [ ] Hai creato Custom GPTs nel workspace? SI / NO
3. [ ] Se SI, conta totale: `___`
4. [ ] Lista per ognuno:

| # | Nome GPT | Has knowledge files? | Has Actions? | Has dedicated chats? | Priority recover |
|---|---|---|---|---|---|
| 1 | `_______________` | Y/N | Y/N | Y/N | H/M/L |
| 2 | `_______________` | Y/N | Y/N | Y/N | H/M/L |
| 3 | `_______________` | Y/N | Y/N | Y/N | H/M/L |
| ... | | | | | |

5. [ ] Custom GPTs nella workspace ma NON creati da te (shared)? Quantity = `___`. Sono recoverable solo i tuoi.

**DECISIONE PATH CUSTOM GPTs**:
- Se totale GPTs creati da te ≤ 5 -> path manuale (Opzione A)
- Se 6-15 -> path manuale ma laborioso, considera Playwright se hai 30+ min
- Se >15 -> usa `scripts/scrape-custom-gpts.js` (Opzione B Playwright)
- Path scelto: A manuale / B Playwright = `___`

---

## F. Memory items

1. [ ] Settings -> "Personalization" -> "Memory" -> "Manage memories"
2. [ ] Conta memory items totali: `___`
3. [ ] Stima rilevanza (quanti contengono context importante per UniUPO/Evo-Tactics/dev?): `___`

**DECISIONE memory tool**:
- Se < 10 items + tutti rilevanti -> copy manuale in `memory-items.md`
- Se > 10 OR vuoi backup completo -> install **MemPort** Chrome extension (free, 100% local) -> Export CSV

---

## G. Custom Instructions

1. [ ] Settings -> "Personalization" -> "Custom Instructions"
2. [ ] Hai compilato textarea "What would you like ChatGPT to know about you"? SI / NO
3. [ ] Hai compilato textarea "How would you like ChatGPT to respond"? SI / NO
4. [ ] Se SI a uno dei due -> backup manual copy-paste in `custom-instructions.md` (2 min)

---

## H. Edge cases bonus

1. [ ] Voice transcripts: hai usato voice mode con transcript salvati? SI / NO
   - Se SI: i text appaiono nelle conversations regolari? (Inspect 1-2 conv voice manuale) `___`
   - Audio file binari NON recuperabili via API (limitation OpenAI)

2. [ ] Shared chat links: hai shareato chat con `https://chat.openai.com/share/...` URLs?
   - Quantità: `___`
   - Sono in `/conversations` endpoint? -> brianjlacy le catturera comunque

3. [ ] Canvas documents: hai usato Canvas extensivamente? SI / NO
   - Default brianjlacy le scarica. Mantieni flag `--no-canvas` OFF.

4. [ ] DALL-E images generate: stima totale `___`
   - Default brianjlacy le scarica. Pesano spazio disco (5-50MB cad).

5. [ ] User-uploaded files (PDF/img/code): stima totale `___`
   - Default brianjlacy le scarica.

---

## I. Bearer token extraction (DevTools)

Da fare IMMEDIATAMENTE PRIMA del bulk export. Token JWT scade ~1h.

1. [ ] In ChatGPT (loggato), apri DevTools: F12
2. [ ] Tab "Network"
3. [ ] Filtra per "conversations" (search box)
4. [ ] Refresh sidebar (clicca su qualsiasi chat o icona "New chat")
5. [ ] Click su qualsiasi request `backend-api/conversations`
6. [ ] Pannello Headers (destra/sotto) -> sezione "Request Headers"
7. [ ] Trova header `Authorization: Bearer eyJ...`
8. [ ] Copy VALUE intero dopo "Bearer " (lunghezza tipica ~500-1500 char, inizia con `eyJ...`)

Token raw -> salva temporaneamente in variabile env:
```powershell
$env:CHATGPT_BEARER_TOKEN = "eyJ..."
```

**SECURITY**: NON committare mai questo token. Vita ~1h. Non scriverlo in file.

(Opzionale ma utile) Account ID per Teams workspace:
1. [ ] Stesso request "conversations", header `chatgpt-account-id: ___-___-___-___-___`
2. [ ] Copy UUID (formato 8-4-4-4-12 hex). brianjlacy lo auto-detecta da JWT, ma esplicito = safer.

---

## J. Output decisioni finali

Riempire questo blocco prima di lanciare bulk export:

```yaml
audit_completed: 2026-05-14
workspace_name: "Area di lavoro di Master DD Business"
my_role: "_______"  # Owner / Admin / Member

scope_counts:
  projects_total: ___
  projects_target_evo_tactics: true/false
  conversations_regular: ___
  conversations_archived: ___
  custom_gpts_owned: ___
  memory_items: ___
  dalle_images_estimate: ___
  user_uploads_estimate: ___

paths:
  custom_gpts: "A_manual"  # or "B_playwright"
  memory_tool: "memport"   # or "manual"

flags_for_brianjlacy:
  - "--include-archived"   # se archived > 0
  - "--delay 2500"         # default safe, 3000 se >500 conv
  - "--output ./exports"

estimated_time:
  bulk_export_minutes: ___
  manual_steps_minutes: ___
  total_phase_1_minutes: ___

risks_identified:
  - "_____________________________"  # eg "GPT X ha 50 chat dedicate, gap se path A"
```

---

## K. Go/no-go checklist

Prima di procedere a step 2 (smoke test brianjlacy):

- [ ] Workspace verificato Business attivo
- [ ] Scope counts noti (sezioni B-G compilate)
- [ ] Bearer token estratto + salvato in env var
- [ ] Path Custom GPTs scelto (A o B)
- [ ] Memory tool scelto (MemPort install vs manual)
- [ ] Output path destination deciso (`./exports` locale o direct vault path)
- [ ] Disk space disponibile >3GB (worst case DALL-E heavy)

Se tutti ✓ -> proceed a `02-bulk-export-runbook.md` step 1 (smoke test).
