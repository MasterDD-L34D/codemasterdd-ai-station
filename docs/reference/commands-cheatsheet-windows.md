# Reference: cheatsheet comandi Windows/PowerShell

**Data**: 2026-04-20
**Scopo**: quick reference dei comandi usati spesso durante setup Lenovo
**Target**: riferimento rapido per futuro self

## Indice

- [Winget (package manager)](#winget)
- [PowerShell basics](#powershell-basics)
- [Registry operations](#registry-operations)
- [Services management](#services-management)
- [Scheduled tasks](#scheduled-tasks)
- [File system](#file-system)
- [Environment variables](#environment-variables)
- [BitLocker](#bitlocker)
- [NVIDIA / GPU](#nvidia--gpu)
- [System Restore](#system-restore)

## Winget

### Install

```powershell
# Install con auto-accept licenze
winget install <PackageId> --accept-package-agreements --accept-source-agreements

# Esempi usati
winget install Git.Git --accept-package-agreements --accept-source-agreements
winget install GitHub.cli --accept-package-agreements --accept-source-agreements
winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements
winget install Microsoft.VisualStudioCode --accept-package-agreements --accept-source-agreements
winget install Ollama.Ollama --accept-package-agreements --accept-source-agreements

# Install versione specifica
winget install OpenJS.NodeJS --version 22.14.0 --accept-package-agreements --accept-source-agreements
```

### Search / list

```powershell
# Lista installati
winget list

# Export audit a file
winget list > C:\dev\winget-audit.txt

# Cerca package
winget search <name>

# Info su package
winget show <PackageId>
```

### Upgrade

```powershell
# Lista update disponibili
winget upgrade

# Upgrade specifico
winget upgrade <PackageId>

# Upgrade tutti (use with caution)
winget upgrade --all
```

### Uninstall

```powershell
# Uninstall silent
winget uninstall --id <PackageId> --silent

# Esempio cleanup bloatware
$bloatware = @("McAfee.McAfeeSecurity", "Lenovo.LegionSpace")
foreach ($pkg in $bloatware) {
    winget uninstall --id $pkg --silent
}
```

## PowerShell basics

### Execution policy

```powershell
# Check policy corrente
Get-ExecutionPolicy

# Set per CurrentUser (non serve admin)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Policy options:
# Restricted, AllSigned, RemoteSigned, Unrestricted, Bypass
```

### Run as admin

```powershell
# Apri PS come admin da PS normale
Start-Process powershell -Verb RunAs

# Check se sono admin
([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
```

### Output redirection

```powershell
# Output a file
Get-Process > processes.txt

# Append a file
Get-Service >> services-log.txt

# Pipe a file CSV
Get-Process | Select-Object Name, CPU | Export-Csv -Path processes.csv -NoTypeInformation
```

### Error handling

```powershell
try {
    # comando rischioso
    Remove-Item -Path "C:\some-path" -Force
} catch {
    Write-Error "Errore: $_"
} finally {
    Write-Host "Sempre eseguito"
}

# Continua anche on error
Remove-Item -Path "C:\path" -ErrorAction SilentlyContinue
```

## Registry operations

### Read

```powershell
# Leggi valore singolo
(Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run").OneDrive

# Leggi tutta una key
Get-ItemProperty -Path "HKCU:\Software\Microsoft\OneDrive"

# Lista subkey
Get-ChildItem -Path "HKLM:\SOFTWARE"
```

### Write / Modify

```powershell
# Crea nuova key
New-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Control\BitLocker" -Force

# Set valore DWord
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\BitLocker" `
  -Name "PreventDeviceEncryption" -Value 1 -Type DWord

# Altri tipi: String, ExpandString, Binary, DWord, QWord, MultiString
```

### Delete

```powershell
# Remove valore singolo
Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" `
  -Name "OneDrive" -ErrorAction SilentlyContinue

# Remove intera key ricorsiva
Remove-Item -Path "HKCU:\Software\Microsoft\OneDrive\Accounts\Personal" `
  -Recurse -Force -ErrorAction SilentlyContinue
```

### Backup / Restore

```powershell
# Export registry key a file .reg
reg export "HKCU\Software\Microsoft\OneDrive" "C:\dev\backup\onedrive.reg" /y

# Export intera hive
reg export HKCU "C:\dev\backup\HKCU-full.reg" /y

# Restore
reg import "C:\dev\backup\onedrive.reg"
```

**IMPORTANTE**: sempre backup prima di modifiche invasive.

## Services management

### Status

```powershell
# Status servizio
Get-Service -Name BDESVC

# Tutti i servizi
Get-Service

# Filter by status
Get-Service | Where-Object { $_.Status -eq "Running" }
```

### Start / Stop

```powershell
# Start
Start-Service -Name BDESVC

# Stop
Stop-Service -Name BDESVC

# Restart
Restart-Service -Name BDESVC
```

### Startup type

```powershell
# Set startup
Set-Service -Name BDESVC -StartupType Disabled
# Opzioni: Automatic, Manual, Disabled, AutomaticDelayedStart

# Verifica
Get-Service -Name BDESVC | Select-Object Name, Status, StartType
```

## Scheduled tasks

```powershell
# Lista tutti
Get-ScheduledTask

# Filter
Get-ScheduledTask -TaskName "*OneDrive*"

# Disable
Get-ScheduledTask -TaskName "*OneDrive*" | Disable-ScheduledTask

# Enable
Get-ScheduledTask -TaskName "OneDrive Standalone Update Task" | Enable-ScheduledTask

# Remove
Unregister-ScheduledTask -TaskName "<name>" -Confirm:$false
```

## File system

### Navigation

```powershell
# PWD equivalent
Get-Location
# O: pwd

# CD
Set-Location "C:\dev"
# O: cd C:\dev

# List
Get-ChildItem
# O: ls, dir
```

### Create

```powershell
# Nuova directory
New-Item -Path "C:\dev\new-dir" -ItemType Directory -Force

# Nuovo file
New-Item -Path "C:\dev\new-file.txt" -ItemType File

# File con contenuto
"Contenuto" | Out-File -FilePath "C:\dev\note.txt"
```

### Copy / Move / Delete

```powershell
# Copy
Copy-Item -Path "source.txt" -Destination "dest.txt"
Copy-Item -Path "C:\dev\*" -Destination "C:\backup\" -Recurse

# Move
Move-Item -Path "source.txt" -Destination "C:\new-location\"

# Rename
Rename-Item -Path "old-name.txt" -NewName "new-name.txt"

# Delete
Remove-Item -Path "file.txt"
Remove-Item -Path "directory" -Recurse -Force

# Delete con confirmation prompt skip
Remove-Item -Path "dir" -Recurse -Force -Confirm:$false
```

### Space / Size

```powershell
# Disk space
Get-PSDrive C

# Folder size
(Get-ChildItem "C:\dev" -Recurse | Measure-Object -Property Length -Sum).Sum / 1GB

# Top 10 largest files in folder
Get-ChildItem "C:\path" -Recurse -File | Sort-Object Length -Descending | Select-Object -First 10 Name, @{N="SizeMB"; E={$_.Length / 1MB}}
```

## Environment variables

### Read

```powershell
# Variabile specifica
$env:PATH
$env:USERPROFILE

# Tutte
Get-ChildItem Env:

# User scope
[System.Environment]::GetEnvironmentVariable("PATH", "User")

# System scope (requires admin)
[System.Environment]::GetEnvironmentVariable("PATH", "Machine")
```

### Write

```powershell
# Set temporaneo (solo session corrente)
$env:MY_VAR = "value"

# Set permanente User scope
[System.Environment]::SetEnvironmentVariable("OLLAMA_FLASH_ATTENTION", "1", "User")

# Set permanente System scope (admin required)
[System.Environment]::SetEnvironmentVariable("SOME_VAR", "value", "Machine")

# Esempio setup Ollama (usato)
[System.Environment]::SetEnvironmentVariable("OLLAMA_FLASH_ATTENTION", "1", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_KV_CACHE_TYPE", "q8_0", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_MAX_LOADED_MODELS", "1", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_KEEP_ALIVE", "30m", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_CONTEXT_LENGTH", "16384", "User")
```

### Refresh PATH senza riapertura shell

```powershell
# Force refresh PATH da Machine + User
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

## BitLocker

### Status

```powershell
# Status drive C:
manage-bde -status C:

# Shorter version
Get-BitLockerVolume -MountPoint C:
```

### Disable

```powershell
# Decrittazione drive C:
manage-bde -off C:

# Alternative PowerShell
Disable-BitLocker -MountPoint "C:"
```

### Enable (se mai servisse)

```powershell
manage-bde -on C: -recoverypassword
# o
Enable-BitLocker -MountPoint "C:" -RecoveryPasswordProtector
```

### Recovery key

```powershell
# Show protectors
manage-bde -protectors -get C:

# Backup recovery key to file
(Get-BitLockerVolume -MountPoint C:).KeyProtector | 
    Where-Object { $_.KeyProtectorType -eq "RecoveryPassword" } |
    ForEach-Object { $_.RecoveryPassword } > "C:\backup\bitlocker-key.txt"
```

## NVIDIA / GPU

### Driver info

```powershell
# GPU info via nvidia-smi
nvidia-smi

# Dettaglio compact
nvidia-smi --query-gpu=name,driver_version,memory.total,memory.used --format=csv

# Monitor real-time (aggiorna ogni 1s)
nvidia-smi -l 1
```

### CUDA

```powershell
# CUDA version
nvcc --version

# CUDA samples location (se installato)
$env:CUDA_PATH
```

### Process using GPU

```powershell
nvidia-smi --query-compute-apps=pid,name,used_memory --format=csv
```

## System Restore

### Create restore point

```powershell
# Abilita restore su C:
Enable-ComputerRestore -Drive "C:\"

# Crea checkpoint
Checkpoint-Computer -Description "Pre-NVIDIA-driver-update" -RestorePointType "MODIFY_SETTINGS"
# Types: APPLICATION_INSTALL, APPLICATION_UNINSTALL, DEVICE_DRIVER_INSTALL, MODIFY_SETTINGS, CANCELLED_OPERATION
```

### List restore points

```powershell
Get-ComputerRestorePoint
```

### Restore

```powershell
# Restore to specific point
Restore-Computer -RestorePoint <number>
# (richiede reboot automatico)
```

## Git operations comuni

```powershell
# Status
git status

# Add + commit + push
git add .
git commit -m "feat: description"
git push origin main

# View log
git log --oneline -10

# Show last commit details
git show HEAD

# Amend last commit
git commit --amend --no-edit

# Force-push safe
git push --force-with-lease=main:<OLD_SHA> origin main

# Create branch
git checkout -b feature/new-feature

# Switch branch
git checkout main
```

## GitHub CLI (gh)

```powershell
# Status auth
gh auth status

# Create repo
gh repo create <user>/<repo> --private --source=. --remote=origin --push

# Edit repo description
gh repo edit --description "description in italiano"

# List repos
gh repo list

# View repo
gh repo view <user>/<repo>
```

## Ollama

```powershell
# Version
ollama --version

# List models
ollama list

# Pull model
ollama pull qwen2.5-coder:7b

# Run model (interactive)
ollama run qwen2.5-coder:7b

# Run with verbose (benchmark)
ollama run qwen2.5-coder:7b --verbose "test prompt"

# Remove model
ollama rm <model-name>

# Show model info
ollama show qwen2.5-coder:7b

# Service status
Get-Service Ollama
Restart-Service Ollama
```

## Claude Code

```powershell
# Version
claude --version

# Launch
claude

# In Claude Code interactive:
# /compact    — compact conversation history
# /model      — switch model
# /exit       — exit
```

## Misc utilities

```powershell
# Restart computer
Restart-Computer -Force

# Shutdown
Stop-Computer -Force

# Logoff
logoff

# Check uptime
(Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime

# Check Windows version
[System.Environment]::OSVersion
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber

# Free memory
Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory, TotalVisibleMemorySize
```

## Gotchas noti

### 1. PATH stantio dopo install

Dopo `winget install <tool>`, sessioni PowerShell aperte **prima** non vedono il tool.
**Fix**: riapri PowerShell, o usa path assoluto, o refresh $env:Path manualmente.

### 2. ExecutionPolicy richiesta per script

Prima di eseguire script .ps1, imposta policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Appx uninstall può lasciare residui

Alcuni uninstall lasciano shortcut Start Menu, registry key, scheduled task.
**Fix**: pulizia manuale post-uninstall:
```powershell
# Shortcut cleanup
Remove-Item "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\<name>.lnk" -Force
```

### 4. Admin vs User scope confusion

Alcuni comandi richiedono admin (registry HKLM, services, Machine env vars).
Altri no (HKCU, file in user home, User env vars).
**Fix**: pianifica quando servi admin, evita admin di default.

### 5. Claude Code bash PATH fossilizzato

Claude Code tiene PATH snapshot all'avvio. Nuove install non visibili finché Claude Code restart.
**Fix**: chiudi e riapri Claude Code dopo install.

## Fonti

- PowerShell docs: https://learn.microsoft.com/en-us/powershell
- Winget docs: https://learn.microsoft.com/en-us/windows/package-manager/winget
- BitLocker docs: https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker
- NVIDIA SMI: https://developer.nvidia.com/nvidia-system-management-interface

## Follow-up

- [ ] Aggiungere command-by-use-case grouping
- [ ] Documentare workflow CI/CD comandi se implementati
- [ ] Cross-reference con script in `scripts/` folder del repo
