# Disconnect OneDrive cleanly (disconnect > uninstall pattern)
#
# Perché "disconnect" e non "uninstall": disconnect preserva catene di dipendenze
# Windows (es. BitLocker key sync su Microsoft Account), evitando lock-out come
# nel disastro Victus pre-2026. Pattern documentato in JOURNAL 2026-04-19.
#
# Source: estratto da materiale research 2026-04-21 (affidabilità sessione
# claude.ai web, eseguito empiricamente su CodeMasterDD 2026-04-19).
#
# Usage (PowerShell admin):
#   .\scripts\disconnect-onedrive.ps1

# 1. Backup registry PRIMA di operazioni
$backupDir = "C:\dev\backup-$(Get-Date -Format 'yyyyMMdd-HHmm')"
New-Item -Path $backupDir -ItemType Directory -Force
reg export HKCU "$backupDir\HKCU-before.reg" /y
reg export "HKCU\Software\Microsoft\OneDrive" "$backupDir\OneDrive-registry-backup.reg" /y

# 2. Shutdown pulito
& "C:\Program Files\Microsoft OneDrive\OneDrive.exe" /shutdown
Start-Sleep -Seconds 3

# 3. Rimuovi account Personal + Business (rimuove auth, preserva binary)
Remove-Item -Path "HKCU:\Software\Microsoft\OneDrive\Accounts\Personal" `
  -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "HKCU:\Software\Microsoft\OneDrive\Accounts\Business1" `
  -Recurse -Force -ErrorAction SilentlyContinue

# 4. Rimuovi autostart
Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" `
  -Name "OneDrive" -ErrorAction SilentlyContinue

# 5. Disabilita tutti task OneDrive
Get-ScheduledTask -TaskName "*OneDrive*" | Disable-ScheduledTask

# 6. Policy anti-sync
New-Item -Path "HKCU:\Software\Policies\Microsoft\OneDrive" -Force
Set-ItemProperty -Path "HKCU:\Software\Policies\Microsoft\OneDrive" `
  -Name "DisableFileSyncNGSC" -Value 1 -Type DWord
Set-ItemProperty -Path "HKCU:\Software\Policies\Microsoft\OneDrive" `
  -Name "DisablePersonalSync" -Value 1 -Type DWord

# 7. Verifica
Get-Process -Name "OneDrive" -ErrorAction SilentlyContinue
