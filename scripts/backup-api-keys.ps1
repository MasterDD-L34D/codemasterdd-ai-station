# backup-api-keys.ps1 -- Daily rotation backup di ~/.config/api-keys/keys.env
#
# BACKLOG M7 (deferred SPRINT_02): mitigation V4 disaster recovery.
# Daily snapshot di keys.env in backup/api-keys/ (gitignored), rotation N giorni,
# encryption at rest opzionale via DPAPI (user+machine bound).
#
# Pattern safety:
#   - Source: $env:USERPROFILE/.config/api-keys/keys.env (ACL solo edusc:F gia' enforced)
#   - Target: backup/api-keys/api-keys-YYYY-MM-DD.env (gitignored via backup/*, ACL preservata)
#   - Encryption opt-in (-Encrypt): DPAPI ConvertFrom-SecureString, decrypt solo da stesso user/machine
#   - Idempotent: overwrite di backup di oggi (no duplicati intra-giorno)
#   - Retention: rimozione file >RetentionDays (default 30)
#
# Privacy:
#   - Plain mode: contenuto leggibile ma ACL identica al source + path gitignored
#   - Encrypt mode: contenuto unreadable senza user+machine context (DPAPI)
#   - MAI commit (gitignored), MAI in cloud, MAI in registry
#
# Usage:
#   .\scripts\backup-api-keys.ps1                          # daily plain backup, retention 30gg
#   .\scripts\backup-api-keys.ps1 -Encrypt                 # DPAPI encryption
#   .\scripts\backup-api-keys.ps1 -RetentionDays 7         # keep last 7 days
#   .\scripts\backup-api-keys.ps1 -Quiet                   # silent (CI/scheduled task)
#
# Schedule daily via Windows Task Scheduler:
#   schtasks /Create /SC DAILY /TN "ApiKeysBackup" /TR "powershell -File C:\dev\codemasterdd-ai-station\scripts\backup-api-keys.ps1 -Quiet" /ST 03:00
#
# Recovery (decrypt encrypted backup):
#   $enc = Get-Content backup/api-keys/api-keys-2026-05-09.env -Raw
#   $sec = ConvertTo-SecureString $enc
#   $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)
#   $plain = [Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
#   Set-Content $env:USERPROFILE/.config/api-keys/keys.env -Value $plain -NoNewline

[CmdletBinding()]
param(
    [string]$Source = "$env:USERPROFILE\.config\api-keys\keys.env",
    [string]$BackupDir = "$PSScriptRoot\..\backup\api-keys",
    [int]$RetentionDays = 30,
    [switch]$Encrypt,
    [switch]$Quiet
)

function Write-Info {
    param([string]$Msg, [string]$Color = "Cyan")
    if (-not $Quiet) { Write-Host $Msg -ForegroundColor $Color }
}

function Write-Err {
    param([string]$Msg)
    Write-Host $Msg -ForegroundColor Red
}

# ---- Validate source ----
if (-not (Test-Path $Source)) {
    Write-Err "ERROR: source non trovato: $Source"
    exit 1
}

$sourceItem = Get-Item $Source
$sourceSize = $sourceItem.Length

if ($sourceSize -eq 0) {
    Write-Err "ERROR: source e' vuoto: $Source"
    exit 1
}

# ---- Resolve backup dir (assoluto, normalizza) ----
if (-not (Test-Path $BackupDir)) {
    Write-Info "Backup dir non esiste, creo: $BackupDir" "DarkGray"
    New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
}
$BackupDir = (Resolve-Path $BackupDir).Path

# ---- Compute target path ----
$dateStr = Get-Date -Format 'yyyy-MM-dd'
$encryptedSuffix = if ($Encrypt) { ".enc" } else { "" }
$targetName = "api-keys-${dateStr}.env${encryptedSuffix}"
$target = Join-Path $BackupDir $targetName

Write-Info "backup-api-keys -- daily rotation"
Write-Info "  Source: $Source ($sourceSize bytes)" "DarkGray"
Write-Info "  Target: $target" "DarkGray"
Write-Info "  Mode:   $(if ($Encrypt) { 'DPAPI encrypted' } else { 'plain (ACL-protected)' })" "DarkGray"
Write-Info "  Retention: $RetentionDays days" "DarkGray"

# ---- Read source ----
try {
    $plain = [System.IO.File]::ReadAllText($Source)
} catch {
    Write-Err "ERROR: lettura source fallita: $_"
    exit 1
}

# ---- Write target ----
try {
    if ($Encrypt) {
        $secure = ConvertTo-SecureString $plain -AsPlainText -Force
        $encrypted = ConvertFrom-SecureString $secure
        # ConvertFrom-SecureString DPAPI: la stringa ritornata e' Base64 hex, user+machine bound.
        Set-Content -Path $target -Value $encrypted -NoNewline -Encoding ASCII
    } else {
        # Plain copy: bytes identici al source, no transcoding
        [System.IO.File]::WriteAllText($target, $plain, [System.Text.UTF8Encoding]::new($false))
    }
} catch {
    Write-Err "ERROR: scrittura target fallita: $_"
    exit 1
}

# ---- Set ACL solo edusc:F (best effort: SetAccessRuleProtection richiede SeSecurityPrivilege/admin) ----
try {
    $acl = Get-Acl $target
    $acl.SetAccessRuleProtection($true, $false)  # disable inheritance, no copy
    $acl.Access | ForEach-Object { $acl.RemoveAccessRule($_) | Out-Null }
    $rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
        "$env:USERDOMAIN\$env:USERNAME",
        "FullControl",
        "Allow"
    )
    $acl.AddAccessRule($rule)
    Set-Acl -Path $target -AclObject $acl -ErrorAction Stop
    Write-Info "  ACL: strict ($env:USERDOMAIN\$env:USERNAME only, no inheritance)" "DarkGray"
} catch [System.Security.AccessControl.PrivilegeNotHeldException] {
    Write-Info "  ACL: ereditate da $BackupDir (strict ACL richiede run as admin)" "DarkGray"
} catch {
    Write-Info "  WARN: set ACL fallito non-fatale (continuo, file gia' scritto): $($_.Exception.Message)" "Yellow"
}

# ---- Verify integrity (read-back) ----
try {
    if ($Encrypt) {
        $encReadBack = Get-Content $target -Raw
        $secReadBack = ConvertTo-SecureString $encReadBack
        $bstrPtr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secReadBack)
        $plainReadBack = [Runtime.InteropServices.Marshal]::PtrToStringAuto($bstrPtr)
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstrPtr)

        if ($plainReadBack -ne $plain) {
            Write-Err "ERROR: integrity check FAIL (decrypt mismatch)"
            exit 1
        }
        Write-Info "  Integrity check: PASS (DPAPI decrypt round-trip OK)" "Green"
    } else {
        $plainReadBack = [System.IO.File]::ReadAllText($target)
        if ($plainReadBack -ne $plain) {
            Write-Err "ERROR: integrity check FAIL (plain content mismatch)"
            exit 1
        }
        Write-Info "  Integrity check: PASS (plain content match)" "Green"
    }
} catch {
    Write-Err "ERROR: integrity check exception: $_"
    exit 1
}

# ---- Rotation: cleanup file > RetentionDays ----
$cutoff = (Get-Date).AddDays(-$RetentionDays)
$removed = 0
Get-ChildItem -Path $BackupDir -Filter "api-keys-*.env*" -File -ErrorAction SilentlyContinue | ForEach-Object {
    if ($_.LastWriteTime -lt $cutoff) {
        try {
            Remove-Item $_.FullName -Force
            Write-Info "  Rotated out: $($_.Name) (LastWrite $($_.LastWriteTime.ToString('yyyy-MM-dd')))" "DarkGray"
            $removed++
        } catch {
            Write-Info "  WARN: cleanup fallito per $($_.Name): $_" "Yellow"
        }
    }
}

# ---- Final report ----
$totalBackups = (Get-ChildItem -Path $BackupDir -Filter "api-keys-*.env*" -File -ErrorAction SilentlyContinue).Count
Write-Info ""
Write-Info "==> Backup OK: $targetName ($sourceSize bytes)" "Green"
Write-Info "    Total backups: $totalBackups (rotated out: $removed)" "DarkGray"

exit 0
