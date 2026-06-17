# Postmortem: Il trauma Victus (17/04/2026)

**Data evento**: 17 aprile 2026
**Data postmortem**: 20 aprile 2026 (3 giorni dopo)
**Scopo**: lezioni apprese per evitare ricorrenza
**Tono**: onesto, analitico, zero blame self o esterno per il gusto del blame

## Executive summary

Il 17 aprile 2026 ho acquistato un HP Victus 15L da Euronics Nola per €1003.
Al primo riavvio dopo setup completo, BitLocker Recovery Screen bloccava
l'accesso. Chiave non recuperabile via Microsoft Account (bug KB5083769 +
aggressiva disinstallazione OneDrive). Dati persi. PC effettivamente
inutilizzabile.

**Impatto**:
- Perdita PC (€1003) — poi recuperato via negoziazione Euronics
- Perdita ~6 ore di setup
- Perdita dati di setup (pochi file, nessun lavoro critico)
- Stress psicologico significativo
- Lezioni apprese che hanno ristrutturato il mio approccio dev

**Cosa è andato storto** (primary causes):
1. Bug KB5083769 Microsoft (non mio controllo)
2. OneDrive disinstallazione aggressiva (mia scelta)
3. Batch install di 14 tool senza pause di verifica (mia scelta)
4. Nessun backup/snapshot pre-primo-riavvio (mia scelta)

**Cosa non era evitabile**:
- Il bug Microsoft (pubblico dopo il 14 aprile)

**Cosa era evitabile**:
- L'impatto del bug, se avessi avuto disciplina di backup + setup progressivo.

## Timeline dettagliata

### 16 aprile 2026 (pre-acquisto)

Cercavo nuovo PC per dev AI workstation. Budget €800-1200.
Trovai HP Victus 15L a €1003 Euronics Nola:
- Core i7-14700F
- RTX 4060 8GB
- 16GB DDR4
- 512GB SSD

**Non sapevo**: che il 14 aprile Microsoft aveva rilasciato KB5083769,
un Patch Tuesday con bug noto legato a BitLocker + OneDrive.

### 17 aprile 2026 mattino — Acquisto

Acquistato a Euronics Tufano, Nola. Pagamento carta. PC ricevuto in box.

**Red flag che non ho notato**:
- Il PC era Windows 11 Home preinstallato già dalla fabbrica
- Sapevo che Windows 11 Home ha BitLocker Device Encryption abilitato di default
- Sapevo di bug KB5083769 in circolo (avevo letto notizie)

### 17 aprile 2026 pomeriggio — Primo setup

Portato a casa. Avviato. Setup wizard:
- Microsoft Account login (mia email)
- Acceptance tutti i Microsoft defaults
- NO custom partitioning
- NO disabling BitLocker

**Errore critico 1**: ho accettato BitLocker auto-encryption senza pensarci.

### 17 aprile 2026 serata — Software install

Installato in batch, senza riavvi intermedi, circa 14 tool:
- Git, Node, Python
- VS Code
- Claude Code
- Discord, Chrome, Steam
- Docker Desktop
- Altri utility

**Durante install**: ho notato OneDrive "aggressivo" (popup, notifiche).
Ho tentato "debloat script" PowerShell trovato online.

**Errore critico 2**: eseguito script non compreso:
```powershell
# Hypothetical debloat script (sostanzialmente)
Get-AppxPackage -AllUsers "*OneDrive*" | Remove-AppxPackage -AllUsers
# ...altri tweaks aggressivi
```

Effetto collaterale nascosto: **OneDrive è dipendenza per BitLocker
recovery key sync** su Windows 11 Home. Rompendo OneDrive ho rotto anche
questa sync.

**Errore critico 3**: nessun checkpoint/snapshot Windows System Restore
prima di queste modifiche.

### 17 aprile 2026 notte — Primo riavvio

Installer finito. Riavvio richiesto da Windows Update + alcuni tool.

**Click Restart**.

**Post-reboot**:
```
BitLocker Recovery Screen
Enter the recovery key to unlock this drive
```

### 17 aprile 2026 tarda notte — Tentativi recovery

**Tentativo 1**: login Microsoft Account web.
- Recovery key NON presente nel mio account
- Motivo: sync rotta dal debloat OneDrive

**Tentativo 2**: USB recovery drive.
- Comando `repair-bde` non può decrittare senza chiave
- `manage-bde -protectors -get C:` inaccessibile senza unlock

**Tentativo 3**: Hiren's BootCD forensics.
- Strumenti leggono disco cifrato come garbage
- Nessun recovery possibile

**Tentativo 4**: Microsoft Support chat.
- Riconosciuto bug KB5083769 recente
- No tool magici
- Hanno suggerito: "restore da backup" (non esisteva) o "reinstallazione"

**Stato finale**: PC boot-loop BitLocker Recovery, zero recovery possibile.

## Root Cause Analysis (5 Whys)

**Problema visibile**: BitLocker Recovery Screen al primo riavvio, chiave non disponibile.

**Why 1**: Perché la chiave non era nel mio Microsoft Account?
→ Perché la sync OneDrive che uploader chiavi BitLocker era rotta.

**Why 2**: Perché la sync era rotta?
→ Perché avevo rimosso aggressivamente OneDrive con script di debloat.

**Why 3**: Perché ho rimosso OneDrive in modo aggressivo?
→ Perché ero irritato dai popup e volevo setup "pulito".

**Why 4**: Perché non sapevo che rimuovere OneDrive sarebbe stato distruttivo?
→ Perché non avevo letto/compreso lo script che stavo eseguendo.

**Why 5**: Perché ho eseguito script non compresi?
→ Perché ero in modalità "setup veloce", multi-tasking, no verifica step-by-step.

**Root cause finale**: **mancanza di disciplina procedurale durante setup critici**.

## Contributing factors

### 1. Pressione temporale auto-imposta

Volevo "finire setup velocemente" per iniziare a lavorare. Ho accorpato
14 install + modifiche sistema in poche ore.

**Mitigation**: setup critici sono **slow by design**. Aspettativa realistica:
1-2 giorni per setup completo dev workstation, non 3 ore.

### 2. Stack Overflow / blog-driven setup

Script di debloat copiato da blog post senza verifica.

**Mitigation**: **leggi sempre cosa fa uno script prima di eseguirlo**.
Se non capisci, non eseguire (o studia prima).

### 3. Microsoft Account + Windows 11 Home

La combo ha auto-enabled BitLocker + uno sync fragile.

**Mitigation**: su futuri PC:
- Considera local account initial setup
- Disable BitLocker **prima** di qualsiasi software install
- Oppure Windows 11 Pro (più controllabile)

### 4. Zero snapshot/backup

Nessun System Restore point prima di modifiche invasive.

**Mitigation**: **always create restore point** prima di:
- Tweaks registry
- Install antivirus/security
- Debloat script
- Major driver update

### 5. OneDrive assumed "optional"

Mental model: "OneDrive è optional, posso toglierlo".
Realtà: OneDrive è integrato profondamente in Windows 11 Home.

**Mitigation**: OneDrive è **disconnect**, non **uninstall**. Lascia
eseguibile in place, disconnetti account + policy + autostart (pattern
usato sul Lenovo).

## Lezioni specifiche apprese

### Lezione 1: BitLocker è arma a doppio taglio

**Pro BitLocker**:
- Protegge dati se PC rubato/perso
- Compliance scenarios

**Contro BitLocker (dev workstation)**:
- Recovery key sync fragile
- Bug Microsoft periodici (KB5083769 non è il primo né sarà l'ultimo)
- Rimuovibile solo se acceso

**Per dev desktop casalingo** (mio caso): **BitLocker off**.
Physical security della casa > cryptographic protection.

### Lezione 2: "Debloat" è operazione seria

Script di debloat Windows **non sono innocui**. Toccano:
- Registry (può rompere features)
- Scheduled tasks (può disabilitare servizi critici)
- Appx packages (può avere cascading effects)
- Services (può impedire boot)

**Approccio giusto**:
1. Backup pre-modifica
2. Script review line-by-line
3. Test su VM prima di production machine (se stakes alti)
4. Reversibilità checklist ("come torno indietro se si rompe?")

### Lezione 3: Windows 11 Home ≠ Windows 11 Pro

**Home** ha:
- BitLocker Device Encryption default ON
- Meno group policy controllabili
- Microsoft Account forzato
- Auto-updates più aggressivi

**Pro** ha:
- BitLocker opzionale
- Group Policy Editor (gpedit.msc)
- Local account OK
- Update più controllabili

**Per dev lessons**: futuro, **considera Windows 11 Pro** se PC mio.
Differenza prezzo €100-150 vale controllo.

### Lezione 4: Primo riavvio è momento di rischio

**Fattori che si combinano al primo riavvio**:
- Tutti i driver caricano freschi
- BitLocker check key
- Windows Update può partire
- Software install post-reboot steps

**Ogni fallimento individuale è possibile, combinazioni sono catastrofiche**.

**Mitigation**: **reboot tra ogni install "grosso"**, non batch.
Verifica sistema stabile dopo ogni reboot prima del next install.

### Lezione 5: Microsoft Account centralizza rischio

Microsoft Account lega insieme:
- Windows login
- OneDrive sync
- BitLocker recovery key sync
- Office license
- Store purchases

**Un errore in una area rompe più sistemi**.

**Mitigation futura**:
- Dual account (local + MSA quando necessario)
- Recovery key backup **fuori** da MSA (chiavetta USB, printout)
- OneDrive solo per file explicit, no "backup intero desktop"

### Lezione 6: Non esistono "piccole modifiche di sistema"

In Windows, ogni modifica al registry/service/policy può avere effetti
a cascata non documentati.

**Mitigation**: tratta ogni modifica come **change management serio**.
Backup, documentation, reversibility plan.

## Cosa ha funzionato bene (positive takeaways)

### 1. Attivazione Codice Consumo

Conoscenza legale + evidence pubblica (bug noto) + articolazione chiara
hanno permesso **negoziazione sostituzione gratuita** con Lenovo desktop
(superiore) + extra.

**Lesson**: diritti consumatore valgono quando:
- Conosci la legge (artt. 128-135)
- Hai evidenza oggettiva (bug documented)
- Comunichi professionalmente (no aggressione)

### 2. Recovery emotivo 48 ore

Dopo shock iniziale, 48 ore di riflessione + azione costruttiva
(negotiate + restart) hanno portato outcome migliore di setup originale.

**Lesson**: trauma è momentaneo, reaction structure è permanente.
Agire con calma produce risultati migliori di agire in panico.

### 3. Ristrutturazione mentale

Il trauma ha **ristrutturato** approach:
- Prima: dev "veloce", install-heavy, trust defaults
- Dopo: dev "deliberato", install-minimal, verify everything

**Lesson**: alcuni errori sono **cari ma trasformativi**.
Il trauma ha risparmiato futuri disastri più gravi (potenzialmente su progetti reali).

## Cosa applico ora (procedura post-trauma)

### Setup PC nuovo — nuova procedura

**Fase 0: Pre-first-boot**
- Research bug Microsoft correnti (KB recenti)
- Plan backup strategy before turning on

**Fase 1: First boot**
- Local account initial (se possibile)
- DISABILITA BitLocker IMMEDIATAMENTE (o Home → Pro upgrade)
- Disconnect OneDrive (not uninstall)
- NON installare nulla se non necessario assoluto
- System Restore point "clean slate"

**Fase 2: Hardening**
- NVIDIA driver Studio (no App)
- Update essenziali sistema
- Disattiva telemetry/tracking
- Firewall rules basic
- System Restore point "hardened"

**Fase 3: Dev stack**
- Git + Claude Code + terminal
- Un tool alla volta con verify
- Reboot tra install grossi
- Commit infrastructure-as-code repo

**Fase 4: Personalization**
- Bloatware removal (audited)
- App-specific config
- Full backup + restore point

### Backup strategy

**Tier 1: System level**
- System Restore points prima di modifiche invasive
- Windows image backup settimanale (esterno drive)

**Tier 2: Data level**
- Git repo per tutto progetto attivo (GitHub origin)
- Syncthing plan (future) tra Lenovo + Ryzen + eventual Mac mini
- Obsidian vault in Git (conoscenza personale)

**Tier 3: Config level**
- Dotfiles in repo
- Script setup reproducibile
- Registry backup pre-tweaks

### Docs di setup

**Repo `codemasterdd-ai-station`** (meta: questo stesso repo).

Documentata ogni decisione, ogni comando, ogni scelta.

Se Lenovo si rompe, **posso ricrearlo in 1 giorno** seguendo la documentazione.

## Reflection psicologica

### Il trauma iniziale

Primo reboot BitLocker screen: panico vero.
- "Ho perso tutto."
- "Ho buttato €1000."
- "Sono incompetente."

### Il processo di recovery

**Ora 1-4**: panico, tentativi disperati recovery.
**Ora 4-12**: disperazione calma, accept data loss.
**Giorno 2**: analisi strategica: cosa posso fare?
**Giorno 2 pomeriggio**: decisione azione legale consumer.
**Giorno 3**: negoziazione Euronics successful.
**Giorno 3-5**: setup Lenovo con disciplina applicata.

### Cosa ho imparato emotivamente

**1. I disastri non definiscono**
Un errore catastrofico non mi rende "bad dev". È **un evento** da cui imparare.

**2. La paranoia post-trauma è utile**
Il stress post-Victus ha reso possibile discipline che "dev-normale" skippa.
Paranoia diventa **metodo**.

**3. Documentation as protection**
Scrivere tutto non è perfezionismo, è **insurance**. Se succede di nuovo,
ho scripts + decisioni ready da applicare.

**4. Sovereignty as healing**
Decisione "sovereign AI" non è coincidenza post-Victus. È **reaction**
a fragility experienced. Build systems you control.

**5. Support network matters**
Ho parlato con mia moglie, mia madre, amici dev durante il trauma.
Non "soluzione tecnica" ma "recalibration emotiva".

## Keep-do-stop

### Keep (cose che ho sempre fatto bene)

- Backup progetti importanti su GitHub
- Repository come source of truth (non disco locale)
- Documentazione tecnica nei readme

### Do (cose nuove, post-trauma)

- BitLocker off per default su dev machine
- OneDrive disconnect pulito (no uninstall)
- System Restore prima di tweak
- Setup progressivo (non batch)
- Reboot tra install grossi
- Journal di sessione in tempo reale
- Commit atomici con messaggi semantic
- ADR per decisioni strategiche

### Stop (cose da non fare più)

- Eseguire script non compresi
- Batch install 10+ tool senza reboot
- Affidamento cieco a Microsoft defaults
- "Lo provo e vedo"
- Rinviare backup "a dopo"
- Ignore warning/error subtili nel setup

## Fonti

- Microsoft KB5083769 bug report: https://support.microsoft.com/en-us/topic/<KB>
- Codice Consumo artt. 128-135: https://www.normattiva.it
- BitLocker recovery key documentation: Microsoft Docs

## Follow-up annuale

**Tra 1 anno (aprile 2027)**: rileggere questo postmortem. Chiedere:
- Ho mantenuto le nuove discipline?
- Nuovi eventi rilevanti da aggiungere?
- Lezioni ancora valide?

## Cosa è costato e cosa ha dato

### Costi

- Tempo: ~40 ore (setup perso + negoziazione + re-setup + postmortem)
- Stress: forte nei primi 2-3 giorni
- Denaro netto: €0 (sostituzione gratuita)

### Ricavi

- Hardware migliore (RTX 4060→5060, DDR4→DDR5, extras €100)
- Approccio dev disciplinato (vale ore nel lungo termine)
- Infrastructure-as-code repo (reproducibility)
- Questo postmortem + ADRs (institutional memory)
- Filosofia sovereign AI (avviata)

**Bilancio**: netto positivo, anche se il percorso è stato duro.

## La frase chiave

**"Il trauma si cura nel fare bene le cose successive, non evitandole."**

Non ho smesso di fare setup PC per paura.
Ho continuato, con più cura.
E ora questo setup è più solido di qualsiasi altro abbia avuto.
