<#
.SYNOPSIS
  Idempotent setup of inbound OpenSSH Server on a fleet Windows PC.

.DESCRIPTION
  Prepares this machine to ACCEPT ssh connections (e.g. Ryzen -> Lenovo).
  Installs OpenSSH.Server, enables + starts sshd (Automatic), opens the
  firewall, and authorizes a peer public key.

  IMPORTANT (Windows OpenSSH gotcha): for accounts in the local
  Administrators group, sshd ONLY reads
  C:\ProgramData\ssh\administrators_authorized_keys (with strict ACL:
  SYSTEM + Administrators only). The per-user ~/.ssh/authorized_keys is
  IGNORED for admin accounts. This script writes the admin file with the
  correct ACL, matching the fleet pattern already used on the Ryzen side.

.PARAMETER AuthorizedPubKey
  The full single-line public key of the connecting peer (Ryzen), e.g.
  "ssh-ed25519 AAAA... vgit@DESKTOP-T77TMKT".

.PARAMETER AdminTarget
  $true (default) -> write administrators_authorized_keys (connecting
  Windows user is a local admin, e.g. edusc). $false -> write the target
  user's ~/.ssh/authorized_keys instead.

.EXAMPLE
  # Run in an ELEVATED PowerShell on the machine that must accept SSH:
  .\setup-ssh-inbound.ps1 -AuthorizedPubKey "ssh-ed25519 AAAA...== vgit@DESKTOP-T77TMKT"

.NOTES
  Reusable across the fleet (Ryzen, wife PCs flagged "SSH pending" in
  CLAUDE.md). Idempotent: safe to re-run; appends the key only if absent.
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [string]$AuthorizedPubKey,

  [bool]$AdminTarget = $true
)

$ErrorActionPreference = 'Stop'

# --- 0. Elevation guard -----------------------------------------------------
$isAdmin = ([Security.Principal.WindowsPrincipal] `
  [Security.Principal.WindowsIdentity]::GetCurrent()
).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
  throw "Must run ELEVATED (Administrator PowerShell). Right-click > Run as administrator."
}

# --- 1. Validate the key shape ---------------------------------------------
$AuthorizedPubKey = $AuthorizedPubKey.Trim()
if ($AuthorizedPubKey -notmatch '^(ssh-ed25519|ssh-rsa|ecdsa-sha2-nistp256|ssh-dss) ') {
  throw "AuthorizedPubKey does not look like an OpenSSH public key (expected 'ssh-ed25519 AAAA...' or similar). Got: $($AuthorizedPubKey.Substring(0,[Math]::Min(40,$AuthorizedPubKey.Length)))..."
}

# --- 2. Install OpenSSH Server capability ----------------------------------
$cap = Get-WindowsCapability -Online -Name 'OpenSSH.Server*'
if ($cap.State -ne 'Installed') {
  Write-Output "[*] Installing OpenSSH.Server capability..."
  Add-WindowsCapability -Online -Name 'OpenSSH.Server~~~~0.0.1.0' | Out-Null
} else {
  Write-Output "[=] OpenSSH.Server already installed."
}

# --- 3. sshd service: Automatic + started ----------------------------------
Set-Service -Name sshd -StartupType Automatic
if ((Get-Service sshd).Status -ne 'Running') {
  Start-Service sshd            # first start generates host keys + default config
  Write-Output "[*] sshd started."
} else {
  Write-Output "[=] sshd already running."
}
# ssh-agent optional but handy; leave as-is if disabled by policy.

# --- 4. Firewall: allow inbound TCP 22 -------------------------------------
$fw = Get-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -ErrorAction SilentlyContinue
if ($fw) {
  Enable-NetFirewallRule -Name 'OpenSSH-Server-In-TCP'
  Write-Output "[=] Firewall rule OpenSSH-Server-In-TCP enabled."
} else {
  New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' `
    -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound `
    -Protocol TCP -Action Allow -LocalPort 22 -Profile Private | Out-Null
  Write-Output "[*] Firewall rule created (TCP 22, Private profile)."
}

# --- 5. Authorize the peer key ---------------------------------------------
if ($AdminTarget) {
  $keyFile = 'C:\ProgramData\ssh\administrators_authorized_keys'
} else {
  $keyFile = Join-Path $env:USERPROFILE '.ssh\authorized_keys'
  $dir = Split-Path $keyFile
  if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
}

$existing = ''
if (Test-Path $keyFile) { $existing = Get-Content $keyFile -Raw -ErrorAction SilentlyContinue }
if ($existing -and $existing.Contains($AuthorizedPubKey)) {
  Write-Output "[=] Key already authorized in $keyFile (no change)."
} else {
  Add-Content -Path $keyFile -Value $AuthorizedPubKey -Encoding ascii
  Write-Output "[*] Key appended to $keyFile."
}

# --- 6. Strict ACL (MANDATORY for administrators_authorized_keys) ----------
if ($AdminTarget) {
  # sshd refuses the file unless writable ONLY by SYSTEM + Administrators.
  icacls $keyFile /inheritance:r | Out-Null
  icacls $keyFile /grant 'SYSTEM:(F)' | Out-Null
  icacls $keyFile /grant 'BUILTIN\Administrators:(F)' | Out-Null
  Write-Output "[*] ACL hardened on $keyFile (SYSTEM + Administrators only)."
}

# --- 7. Restart sshd to pick up the key ------------------------------------
Restart-Service sshd
Write-Output ""
Write-Output "DONE. This machine now accepts inbound SSH."
$ip = (Get-NetIPAddress -AddressFamily IPv4 |
  Where-Object { $_.IPAddress -like '192.168.*' }).IPAddress
Write-Output "  Connect from the peer with:  ssh $env:USERNAME@$ip"
Write-Output "  (host keys fingerprint will be asked once, accept it)"
