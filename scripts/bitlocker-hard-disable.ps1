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

<#
.SYNOPSIS
Disabilita BitLocker in modo completo su un disco.

.DESCRIPTION
Questo script esegue una disabilitazione triplo di BitLocker per impedire l'auto-encryption su Windows 11. 
Il processo include la decrittazione del disco, la modifica del registro per prevenire l'auto-encryption e la disabilitazione del servizio BDESVC.

.NOTES
Questo script è stato sviluppato per prevenire problemi di lock-out come quello riscontrato nel pattern Victus.
Per ulteriori dettagli, vedere il JOURNAL 2026-04-19.

.EXAMPLE
.\scripts\bitlocker-hard-disable.ps1
Esegui il processo di disabilitazione di BitLocker completo.
#>

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
