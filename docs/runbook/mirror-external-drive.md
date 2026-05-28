# Mirror -> external drive (disk-loss insurance, manual)

> **Trigger**: punto 3 della governance cleanup 2026-05-28 (D3 mirror disk-loss).
> **Scope**: copia periodica `C:\dev\_mirror-backup\*.git` (7 bare mirror) su disco esterno per insurance da disk-loss locale. Complementa lo scheduled task `codemasterdd-mirror-backup` (settimanale Dom 10:00) che copre GitHub-account-loss ma vive sullo stesso disco di Lenovo (no disk-loss insurance).

## Quando farlo

- **Cadence consigliata**: 1x al mese (allineato fine-mese / inizio-mese, opportunistic quando colleghi il drive per altro).
- **Trigger reattivo**: dopo cambio storage hardware (es. SSD swap) o dopo eventi insolitamente attivi (es. release point, milestone Sprint).
- **Skip**: settimane senza commit significativi -> il bare mirror locale e' gia' identico alla settimana prima.

## Procedura (3 step)

### Step 1 -- Connetti il drive esterno

Identifica il drive letter (`E:`, `F:`, ecc.). Crea la dir target una volta sola:

```powershell
$drive = 'E:'   # adatta alla lettera reale
$dest = Join-Path $drive 'codemasterdd-mirror-backup'
if (-not (Test-Path $dest)) { New-Item -ItemType Directory -Force -Path $dest | Out-Null }
```

### Step 2 -- Esegui helper script

```powershell
.\scripts\backup\copy-mirror-to-external.ps1 -Destination $dest
```

L'helper usa `robocopy` con flag `/MIR` (mirror: aggiunge nuovi + aggiorna modificati + cancella file rimossi dal source) per riflettere esattamente `C:\dev\_mirror-backup\` sul drive esterno. Idempotente.

Output atteso: 7 directory bare mirror copiate (codemasterdd-ai-station / vault / Game / Game-Godot-v2 / Game-Database / evo-swarm / synesthesia), totale variabile (~size cumulativo dei bare mirror).

### Step 3 -- Verify + scollega

```powershell
# Conta dir copiate
(Get-ChildItem $dest -Directory | Where-Object Name -Like '*.git').Count   # expect 7

# Verifica HEAD su una bare a campione
$g = Join-Path $dest 'codemasterdd-ai-station.git'
git -C $g rev-parse HEAD   # expect SHA recente (= origin/main attuale)
```

Se OK, eject pulito: `Get-Volume -DriveLetter ($drive[0])` -> tool dismount / icona system tray Windows.

## Cosa NON copre

- **Account-loss**: gia' coperto dallo scheduled task locale (bare mirror sopravvive a GitHub account-loss; vive su Lenovo).
- **Off-site fire/theft**: il drive esterno deve essere fisicamente separato (cassetto altra stanza / armadio fuori-studio) per off-site reale. Storage co-locato = same-event-risk.
- **Storia post-ultimo-copy**: gli ultimi N giorni tra ultima copy esterna e disk-loss sono persi salvo GitHub-side recovery. Cadence 1x/mese = accetta finestra 30gg di latenza max.

## Pattern coerenza fleet

- Ryzen: stesso scheduled task locale (post deploy script + git pull canonical) + stessa procedura external-drive (eventuale). Eduardo-manual per ora; future opzionale = sync remoto via SSH ma fuori scope (sovereign-first contradiction se cloud, complicazione fleet-coordinated).

## Reference

- VC governance review 2026-05-28: `docs/research/2026-05-28-vc-governance-review.md` (D3 mirror decision).
- Scheduled task: `codemasterdd-mirror-backup` (Windows Task Scheduler, weekly).
- Script source: `scripts/backup/copy-mirror-to-external.ps1`.
