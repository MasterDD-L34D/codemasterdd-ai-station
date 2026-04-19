# Sessione notturna 2026-04-19: recovery dopo trauma Victus

> Prima sessione operativa su CodeMasterDD.
> Durata: ~6 ore (03:43 → 10:00 circa)
> Stato finale: Lenovo hardened, infrastructure base pronta, primo commit locale

## Contesto

### Il trauma Victus (17/04/2026)

Il 14 aprile 2026 Microsoft ha rilasciato il Patch Tuesday KB5083769.
Il 17 aprile 2026, dopo aver acquistato un HP Victus 15L (i7-14700F +
RTX 4060 + 16GB DDR4) da Euronics Tufano a Nola per €1003, ho eseguito
il primo setup completo:

1. Windows 11 install + configurazione Microsoft Account
2. Installazione batch di 14 software (Git, Node, Python, Docker, VS Code,
   Claude Code, Chrome, Discord, Steam, ecc.)
3. Prima riavvio del sistema

Al riavvio: BitLocker Recovery Screen.
Chiave non disponibile nel mio account Microsoft.

**Causa**: bug KB5083769 + disinstallazione aggressiva di OneDrive durante
il setup (ho provato a rimuoverlo con script di debloat) hanno rotto la
sincronizzazione della recovery key verso l'account Microsoft.

**Tool forensi tentati**: repair-bde, manage-bde.exe da USB recovery,
Hiren's BootCD, tutti inefficaci senza la chiave.
**Microsoft Support**: nessun recovery possibile.
**Risultato**: dati persi, PC inutilizzabile.

### La negoziazione Euronics (18/04/2026)

Ho applicato il Codice del Consumo italiano (artt. 128-135) + evidenza
pubblica del bug KB5083769 (segnalato su Reddit, GitHub issues, forum
Microsoft) per argomentare difetto di conformità.

**Risultato negoziazione**:
- Sostituzione gratuita con Lenovo LOQ Tower 17IAX10 (CodeMasterDD)
- Hardware migliore: Intel Core Ultra 7 255HX + RTX 5060 8GB + 16GB DDR5 + SSD 1TB
- Extra gratuiti: microfono valore €70 + chiavetta USB 128GB valore €30
- A parità prezzo del Victus (€1003)

Valore aggiuntivo totale: €100 + upgrade hardware RTX 4060→5060 + DDR4→DDR5.

### Stato mentale iniziale

Quando ho iniziato la sessione notturna del 19/04 alle 03:43 ero:
- Fisicamente: sveglio dalla sera prima (trauma metabolizzato ma non digerito)
- Emotivamente: determinato ma teso
- Intellettualmente: con molte paranoie post-Victus da gestire

**Paura principale**: ripetere lo stesso errore (BitLocker + OneDrive +
batch install senza verifica) e perdere di nuovo il setup.

**Decisione strategica**: approccio "capire prima, fare dopo". Un comando
alla volta. Approvazione esplicita per ogni azione non banalmente reversibile.

## Fase 1: Triplo blocco BitLocker (03:43-04:30)

### Obiettivo
Eliminare completamente BitLocker come vettore di rischio. Non "disattivare"
solo, ma **impedire qualsiasi riattivazione automatica futura**.

### Livelli di protezione applicati

**Livello 1 — Decrittazione disco**
```powershell
manage-bde -status C:
# Output: BitLocker attivo, Protection ON, disco crittografato
manage-bde -off C:
# Decrittazione completa avviata
```
Durata decrittazione: ~25 min. Verifica con `manage-bde -status C:`
fino a "Fully Decrypted".

**Livello 2 — Registry anti-encryption-auto**
```powershell
# Aggiunto key che Windows rispetta
New-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Control\BitLocker" -Force
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\BitLocker" `
  -Name "PreventDeviceEncryption" -Value 1 -Type DWord
```
Effetto: Windows non tenterà encryption automatica al prossimo setup o
Microsoft Account login.

**Livello 3 — Servizio BDESVC disabilitato**
```powershell
Stop-Service -Name BDESVC
Set-Service -Name BDESVC -StartupType Disabled
```
Effetto: il servizio BitLocker Drive Encryption non parte all'avvio,
rendendo impossibile re-attivazione senza intervento manuale esplicito.

### Verifica finale
- `manage-bde -status`: "Fully Decrypted", "Protection Off", "No Key Protectors"
- `Get-Service BDESVC`: Status Stopped, StartType Disabled
- Test reboot: nessun prompt BitLocker, sistema boota pulito

### Lezione appresa
**BitLocker + Microsoft Account = accoppiata fragile**. La sync della
recovery key verso MSA non è garantita sempre. Per dev workstation senza
necessità compliance enterprise, BitLocker è più rischio che beneficio.

## Fase 2: OneDrive disconnect pulito (04:30-05:20)

### Il problema di OneDrive su Windows 11

OneDrive è ***aggressive by default***:
- Auto-login con Microsoft Account
- Redirect di Desktop/Documents/Pictures a cloud sync
- Backup "automatic" che può includere cartelle dev
- File placeholders (0.98MB ma "virtuali") che confondono tool forensi

**Durante disastro Victus**, uno dei fattori complicanti era che molti file
erano placeholders OneDrive. Impossibile recuperare dati quando BitLocker
li rende illeggibili E OneDrive li aveva solo come reference.

### Approach: disconnect NON uninstall

Uninstall aggressivo = quello che ha danneggiato il Victus.
**Disconnect pulito** = OneDrive resta installato ma inerte.

### Script di disconnect

Ho scritto `scripts/disconnect-onedrive.ps1`:

```powershell
# 1. Backup registry pre-operazione
$backupDir = "C:\dev\backup-20260419-0518"
New-Item -Path $backupDir -ItemType Directory -Force
reg export HKCU "$backupDir\HKCU-before.reg" /y
reg export "HKCU\Software\Microsoft\OneDrive" "$backupDir\OneDrive-registry-backup.reg" /y

# 2. Shutdown OneDrive pulito
& "C:\Program Files\Microsoft OneDrive\OneDrive.exe" /shutdown
Start-Sleep -Seconds 3

# 3. Rimuovi account Personal + Business residui
Remove-Item -Path "HKCU:\Software\Microsoft\OneDrive\Accounts\Personal" `
  -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "HKCU:\Software\Microsoft\OneDrive\Accounts\Business1" `
  -Recurse -Force -ErrorAction SilentlyContinue

# 4. Rimuovi autostart
Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" `
  -Name "OneDrive" -ErrorAction SilentlyContinue
Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" `
  -Name "OneDriveSetup" -ErrorAction SilentlyContinue

# 5. Disabilita tutti i task OneDrive
Get-ScheduledTask -TaskName "*OneDrive*" | Disable-ScheduledTask

# 6. Policy anti-sync
New-Item -Path "HKCU:\Software\Policies\Microsoft\OneDrive" -Force
Set-ItemProperty -Path "HKCU:\Software\Policies\Microsoft\OneDrive" `
  -Name "DisableFileSyncNGSC" -Value 1 -Type DWord
Set-ItemProperty -Path "HKCU:\Software\Policies\Microsoft\OneDrive" `
  -Name "DisablePersonalSync" -Value 1 -Type DWord

# 7. Verifica
Get-Process -Name "OneDrive" -ErrorAction SilentlyContinue
# Deve ritornare nulla
```

### Verifica finale
- Nessun processo OneDrive attivo
- Nessun autostart registry HKCU Run
- 3 task scheduler disabilitati
- Account Personal + Business1 rimossi
- Policy DisableFileSyncNGSC + DisablePersonalSync attive

### Lezione appresa
**OneDrive non va disinstallato, va disconnesso pulitamente**. Uninstall
aggressivo rompe catene dipendenze Windows (BitLocker key sync, credenziali
Microsoft Account). Disconnect conserva l'eseguibile ma lo rende inerte.

## Fase 3: Upgrade driver NVIDIA 581→595 (05:20-06:10)

### Stato iniziale
- NVIDIA driver 581.32 (09/09/2025) pre-installato da Euronics
- CUDA 13.0
- Bug cosmetico: Windows WMI leggeva solo 4.29GB VRAM invece di 8GB
  (hardware sano, problema solo di lettura WMI)

### Processo upgrade

**1. System Restore Point**:
```powershell
Enable-ComputerRestore -Drive "C:\"
Checkpoint-Computer -Description "Pre-NVIDIA-driver-update-595.79"
```

**2. Download Studio Driver da nvidia.com**:
- Categoria: GeForce RTX 5060
- Windows 11 64-bit
- **Studio Driver** (più stabile di Game Ready per dev)
- Versione 595.79 (16/04/2026)
- Download: ~700 MB

**3. Install custom "advanced"**:
- Extract path: temporaneo (%TEMP%)
- **NOT** NVIDIA App (bloatware)
- Componenti installati: SOLO Graphics Driver + HD Audio
- Flag: **Clean Installation** spuntato (rimuove config precedente)

Durata install: ~12 min + reboot richiesto.

**4. Reboot**:
```powershell
Restart-Computer -Force
```

**5. Post-reboot verifica**:
```powershell
nvidia-smi
```

Output:
```
+-----------------------------------------------------------------------+
| NVIDIA-SMI 595.79       Driver Version: 595.79     CUDA Version: 13.2 |
|-----------------------------------------------------------------------|
| GPU  Name        TCC/WDDM  | Bus-Id        Disp.A | Volatile Uncorr.  |
| Fan  Temp   Perf Pwr:Usage | Memory-Usage         | GPU-Util Compute  |
|=======================================================================|
|   0  NVIDIA GeForce RTX 5060   WDDM  | 00000000:01:00.0 On |  Default |
|  N/A   28C    P8    10W / 145W |  1134MiB / 8151MiB |      0%    Default |
+-----------------------------------------------------------------------+
```

Verifica chiave:
- **Driver 595.79** ✓
- **CUDA 13.2** ✓ (upgrade da 13.0)
- **RTX 5060 8GB riconosciuta** ✓ (bug WMI risolto)
- **28°C idle** ✓ (hardware sano)
- **10W/145W** ✓ (idle power realistico)
- **VRAM 1134/8151 MiB** ✓

### Lezione appresa
**NVIDIA Studio Driver > NVIDIA App** per dev. L'App NVIDIA è bloatware
con telemetria invasiva, updater aggressivo, pop-up game-centric. Studio
Driver standalone è più pulito e stabile per workflow professionale.

## Fase 4: Installazione Git (06:10-06:25)

### Via winget
```powershell
winget install --id Git.Git --accept-package-agreements --accept-source-agreements
```

Versione installata: **Git 2.53.0.windows.3**.

### Configurazione globale
```powershell
git config --global user.name "Eduardo Scarpelli"
git config --global user.email "eduscarpelli@gmail.com"
git config --global init.defaultBranch main
git config --global core.autocrlf input
git config --global pull.rebase false
git config --global credential.helper manager
```

### Verifica
```powershell
git --version
# git version 2.53.0.windows.3

git config --list --global
```

### Scelte importanti
- **init.defaultBranch main**: no more master
- **core.autocrlf input**: evita conversioni CRLF/LF su clone
- **pull.rebase false**: merge commit espliciti (semplice per solo-dev)
- **credential.helper manager**: Windows Credential Manager (standard)

## Fase 5: Claude Code install + OAuth (06:25-07:10)

### Prerequisito: Execution Policy

PowerShell richiede abilitazione script:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Install via script ufficiale
```powershell
irm https://claude.ai/install.ps1 | iex
```

Installa in: `C:\Users\edusc\.local\bin\claude.exe`.
Aggiunge path a User PATH automaticamente.

Dimensione: ~80 MB.

### Verifica
```powershell
# Riaprendo PowerShell per PATH refresh
claude --version
# 2.1.114
```

### OAuth login a Claude Max

```powershell
claude
```

Prima esecuzione apre wizard setup:
1. Theme: **Dark** (scelto)
2. Security notes: lette e accettate
3. OAuth flow: apre browser, login con eduscarpelli@gmail.com
4. Conferma Claude Max attivo (Opus 4.7 con 1M context)
5. Organizzazione: eduscarpelli@gmail.com (personal)
6. Trust folder: `C:\dev\lenovo-ai-station` (da creare)

### Lezione appresa
**Claude Code 2.1.114 native Windows** è maturo. Setup 5 minuti, zero friction.
Supporto Claude Max = accesso diretto a Opus 4.7 con 1M token context.

## Fase 6: Cleanup bloatware (07:10-08:30)

### Inventory

Prima di rimuovere ho fatto audit completo:
```powershell
winget list > bloatware-audit-pre.txt
Get-AppxPackage | Select Name, PackageFullName > appx-audit-pre.txt
```

### Rimozione classici (winget)

```powershell
$classicBloatware = @(
    "Lenovo.SmartConnectReadyFor",
    "Microsoft.365.Apps.en-us",
    "Microsoft.365.Apps.it-it",
    "Microsoft.OneNote.en-us",
    "Microsoft.OneNote.it-it",
    "McAfee.McAfeeSecurity",
    "Lenovo.LegionSpace",
    "Lenovo.LenovoNow",
    "Lenovo.SmartStorage",
    "Lenovo.SENetFilter"
)

foreach ($pkg in $classicBloatware) {
    winget uninstall --id $pkg --silent
}
```

Alcuni (Lenovo Now, SmartStorage) non esistevano come ARP IDs —
probabilmente dipendenze rimosse a cascata.

### Rimozione MSIX (Appx)

```powershell
$appxBloatware = @(
    # Xbox gaming
    "Microsoft.XboxApp",
    "Microsoft.Xbox.TCUI",
    "Microsoft.XboxGameOverlay",
    "Microsoft.XboxGamingOverlay",
    "Microsoft.XboxIdentityProvider",
    "Microsoft.XboxSpeechToTextOverlay",
    "Microsoft.MicrosoftSolitaireCollection",

    # Bing & News
    "Microsoft.BingNews",
    "Microsoft.BingSearch",
    "Microsoft.BingWeather",

    # Office trial
    "Microsoft.MicrosoftOfficeHub",
    "Microsoft.OutlookForWindows",

    # Miscellanea
    "Microsoft.Clipchamp",
    "Microsoft.Whiteboard",
    "MicrosoftCorporationII.MicrosoftJournal",
    "Microsoft.MicrosoftStickyNotes",
    "Microsoft.GetHelp",
    "Microsoft.Todos",
    "Microsoft.Copilot",
    "MicrosoftCorporationII.MicrosoftFamily",
    "Microsoft.QuickAssist",
    "Microsoft.PowerAutomateDesktop",
    "Microsoft.OneDriveSync"
)

foreach ($pkg in $appxBloatware) {
    Get-AppxPackage -Name "*$pkg*" -AllUsers | Remove-AppxPackage -AllUsers
}
```

### Shortcut cleanup

```powershell
# Start Menu entries residue
$startMenu = "$env:ProgramData\Microsoft\Windows\Start Menu\Programs"
Remove-Item -Path "$startMenu\Garanzia.lnk" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$startMenu\Lenovo Now Discovery.lnk" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$startMenu\Richiedi supporto.lnk" -Force -ErrorAction SilentlyContinue
```

### Totale rimosso
- Classici winget: 5-11 pacchetti (alcuni non trovati ARP)
- Appx: 22 pacchetti
- Shortcut: 3 file .lnk

### Verifica finale spazio liberato
```powershell
Get-PSDrive C
# Prima: 830 GB liberi
# Dopo: 869.46 GB liberi
# Liberati: ~39 GB
```

### Lezione appresa
**Laptop/desktop nuovi hanno 30-50 GB di bloatware**. Vale 1-2 ore di
cleanup iniziale, risparmia GB spazio + ore RAM/CPU nel tempo.

## Bilancio sessione notturna

### Tempo per fase
- Triplo blocco BitLocker: 47 min
- OneDrive disconnect: 50 min
- NVIDIA driver: 50 min
- Git install + config: 15 min
- Claude Code install + OAuth: 45 min
- Cleanup bloatware: 80 min
- **Totale**: ~5h15min di lavoro attivo (+ 45 min pause)

### Metriche qualità
- **Errori**: 0
- **Rework**: 0
- **Rollback**: 0
- **Commit atomici**: non ancora, prima sessione era pre-git

### Rate lavoro
~50 righe di procedure documentate all'ora. Non velocità massima,
ma **zero debito tecnico**.

### Stato finale sistema
- BitLocker neutralizzato (3 livelli)
- OneDrive disconnesso pulito
- Driver NVIDIA aggiornato (595.79)
- CUDA 13.2 funzionante
- Git installato e configurato
- Claude Code 2.1.114 con Claude Max
- Bloatware rimosso (~40GB liberati)
- Sistema pronto per git init (mattina dopo)

## Meta-learning personale

### Cosa ho imparato in questa sessione

**1. La paranoia post-trauma è utile**
Il disastro Victus mi ha reso iper-cauto. Invece di essere ostacolo, questa
cautela è diventata **metodo**. "Un comando alla volta" non era scelta
intellettuale astratta, era **esigenza emotiva** trasformata in pratica dev.

**2. Chatbot AI come partner di thinking, non come oracolo**
Durante questa sessione Claude è stato mio ***rubber duck*** tecnico.
Non "mi ha fatto il lavoro", ma mi ha aiutato a **articolare decisioni**
prima di eseguirle. Questo è il valore reale degli AI tool.

**3. L'installazione non è la configurazione**
Il 90% del tempo è andato in config (policy, registry, backup, verifica)
non install. Troppe guide online fermano a `winget install X`. La vera
robustezza è nelle impostazioni fini.

**4. Backup PRIMA di ogni modifica "importante"**
Ho fatto backup registry prima di toccarlo. Sembra ovvio ma quanti
lo fanno davvero? Il costo è 2 secondi, il beneficio è **poter tornare indietro**.

**5. La documentazione scritta durante, non dopo**
Mentre facevo, scrivevo note. Mai "lo documento dopo". Perché dopo = mai.
Ogni sessione futura di `grep` su questo file sarà più veloce perché **me stesso
del passato è stato gentile con me stesso del futuro**.

### Cosa cambia nel mio approccio post-Victus

**Prima del Victus** (old me):
- Batch install multi-software "veloce"
- "Lo provo e vedo"
- Copy-paste da Stack Overflow senza leggere
- Reboot senza verifica stato
- "Farò backup poi"

**Dopo il Victus** (new me):
- Un comando alla volta
- Spiegazione PRIMA del comando
- Verifica output ogni step
- Backup sempre prima di modifiche
- Journal delle sessioni scritto in tempo reale
- Approvazione esplicita su operazioni non reversibili

**Non sono diventato un dev migliore**. Sono diventato un dev **più
disciplinato**. Che è la stessa cosa in modo più onesto.

### Emozione dominante durante la sessione

**Prima delle 05:00**: ansia e vigilanza iper-attenta
**05:00-07:00**: fiducia crescente man mano che ogni step funzionava
**Dopo 07:00**: calma operativa, flow stato

**Il trauma si cura nel fare bene le cose successive**, non evitandole.

## Riferimenti

- Codice Consumo italiano artt. 128-135 (garanzia)
- Bug Microsoft KB5083769 (14 aprile 2026 Patch Tuesday)
- NVIDIA Driver 595.79 Release Notes (16 aprile 2026)
- PowerShell Execution Policy: RemoteSigned scope CurrentUser
- Git for Windows 2.53.0: https://git-scm.com/downloads

## Output tangibili

Alla fine di questa sessione esistevano fisicamente:
- `C:\dev\backup-20260419-0518\*.reg` (registry backup pre-operazioni)
- `C:\dev\backup-20260419-0518\disconnect-onedrive.ps1` (script riutilizzabile)
- `C:\dev\lenovo-ai-station\` (directory trust Claude Code)
- Sistema Lenovo pronto per dev moderno

Assenti ancora ma pianificati:
- Git repo inizializzato (mattina)
- Node/Python/VSCode install (domenica sera)
- Ollama + modelli locali (domenica sera, bonus)
