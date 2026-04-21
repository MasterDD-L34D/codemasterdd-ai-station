# BitLocker triplo blocco (procedura completa)
#
# 3-layer disable per impedire encryption auto su Windows 11. Usato su
# CodeMasterDD 2026-04-19 per prevenire lock-out pattern Victus (dove
# BitLocker auto-encryption + Microsoft Account key sync ha reso unbootable
# una macchina dopo reset OneDrive).
#
# Source: estratto da materiale research 2026-04-21 (eseguito empiricamente
# su CodeMasterDD 2026-04-19). Vedi JOURNAL 2026-04-19.
#
# Usage (PowerShell admin):
#   .\scripts\bitlocker-hard-disable.ps1

# Livello 1 — Decrittazione disco
manage-bde -off C:  # wait until "Fully Decrypted" in manage-bde -status

# Livello 2 — Registry anti-encryption-auto
New-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Control\BitLocker" -Force
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\BitLocker" `
  -Name "PreventDeviceEncryption" -Value 1 -Type DWord

# Livello 3 — Servizio BDESVC disabilitato
Stop-Service -Name BDESVC
Set-Service -Name BDESVC -StartupType Disabled

# Verifica finale
manage-bde -status  # "Fully Decrypted", "No Key Protectors"
Get-Service BDESVC  # Status Stopped, StartType Disabled
