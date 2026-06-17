# Runbook: SSH inbound fleet setup (`setup-ssh-inbound.ps1`)

**Script**: `scripts/setup/setup-ssh-inbound.ps1`
**Scopo**: rendere una macchina Windows del fleet capace di **accettare** connessioni SSH (es. Ryzen -> Lenovo) in modo idempotente e ripetibile.
**Validato empiricamente**: 2026-05-17, sblocco sync Ryzen->Lenovo (vedi JOURNAL).

---

## Cosa fa (7 step)

1. **Elevation guard** — esce subito se non lanciato come Administrator.
2. **Valida la chiave** — controlla che `-AuthorizedPubKey` sia una pubkey OpenSSH valida.
3. **Installa OpenSSH.Server** — `Add-WindowsCapability` (skip se già installato).
4. **sshd Automatic + started** — primo start genera host key + config default.
5. **Firewall** — apre/abilita inbound TCP 22 (profilo Private).
6. **Autorizza la pubkey del peer** — append idempotente (solo se assente).
7. **ACL stretta + restart sshd** — vedi gotcha sotto.

## Gotcha load-bearing (perché serve questo script, non `ssh-keygen` a mano)

Per account nel gruppo **Administrators** locale, l'OpenSSH di Windows
legge **SOLO** `C:\ProgramData\ssh\administrators_authorized_keys` con ACL
stretta (**SYSTEM + Administrators only**, inheritance OFF). Il classico
`~/.ssh/authorized_keys` per-utente è **IGNORATO** per gli admin. Senza la
ACL corretta sshd **rifiuta** il file silenziosamente -> auth fallisce
"credenziali ignote". Lo script scrive il file admin + applica l'ACL
corretta. Questo è il motivo per cui i tentativi manuali "ovvi"
falliscono.

---

## Uso (procedura completa peer -> target)

### Passo 1 — sul PEER (la macchina che si connette, es. Ryzen): genera la coppia di chiavi

```powershell
# se non esiste gia':
ssh-keygen -t ed25519 -f $env:USERPROFILE\.ssh\id_ed25519 -N '""' -C "vgit@DESKTOP-T77TMKT"
type $env:USERPROFILE\.ssh\id_ed25519.pub   # copia questa riga
```

> Alternativa robusta usata 2026-05-17: generare la coppia su una macchina
> qualunque senza problemi di quoting, poi `scp` la **privata** sul peer e
> usare la **pubblica** al passo 2. Il keygen remoto over-SSH è fragile
> (prompt passphrase senza PTY) — preferire keygen locale + scp.

### Passo 2 — sul TARGET (la macchina che deve ACCETTARE, es. Lenovo): lancia lo script ELEVATO

PowerShell **Run as administrator**:

```powershell
cd C:\dev\codemasterdd-ai-station
.\scripts\setup\setup-ssh-inbound.ps1 -AuthorizedPubKey "ssh-ed25519 AAAA...== vgit@DESKTOP-T77TMKT"
```

Se l'utente connettente sul target NON è admin (raro nel fleet): aggiungi
`-AdminTarget $false` (scrive `~/.ssh/authorized_keys` invece del file admin).

#### Lanciarlo elevato da una sessione non-elevata (pattern 2026-05-17)

Se non hai una shell admin a portata, da PowerShell normale:

```powershell
$key='ssh-ed25519 AAAA...== vgit@DESKTOP-T77TMKT'
$log='C:\dev\codemasterdd-ai-station\logs\ssh-inbound-setup.log'
Start-Process powershell -Verb RunAs -Wait -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-Command',
  "& { & 'C:\dev\codemasterdd-ai-station\scripts\setup\setup-ssh-inbound.ps1' -AuthorizedPubKey '$key' *>&1 | Tee-Object -FilePath '$log' }")
Get-Content $log
```

-> compare **un popup UAC**: clicca **Sì** una volta. Lo script gira
elevato, logga su file, leggi l'esito dal log. (`logs/` è gitignored.)

### Passo 3 — verifica (dal peer)

```
ssh edusc@<hub-ip>            # IP target stampato a fine script
# prima volta: accetta il fingerprint host (yes)
```

Verifica annidata (se hai accesso al peer via un terzo canale):
```
ssh -i <fleetkey> Vgit@<peer-ip> "ssh -i C:/Users/Vgit/.ssh/id_ed25519 -o StrictHostKeyChecking=accept-new edusc@<hub-ip> whoami"
```

---

## Idempotenza

Safe da ri-lanciare. Capability già installata -> skip. sshd già running
-> skip. Chiave già presente -> no append. Firewall rule esistente ->
solo enable. La 2ª run è no-op verificata.

## Troubleshooting

| Sintomo | Causa | Fix |
|--------|------|-----|
| "Must run ELEVATED" | shell non-admin | Run as administrator / pattern Start-Process -Verb RunAs |
| auth fallisce, "Permission denied (publickey)" su account admin | ACL/file sbagliato | lo script SCRIVE l'admin file + ACL; verifica `icacls C:\ProgramData\ssh\administrators_authorized_keys` = solo SYSTEM+Administrators |
| connessione rifiutata (timeout) | firewall / sshd down | `Get-Service sshd`; `Get-NetFirewallRule OpenSSH-Server-In-TCP` |
| keygen remoto over-SSH si blocca | prompt passphrase senza PTY | keygen locale + scp (vedi nota Passo 1) |
| warning "post-quantum key exchange" | banner informativo OpenSSH recente | innocuo su LAN, ignora |

## Riuso fleet

Stesso script per i PC "SSH pending" in CLAUDE.md (PC moglie
DESKTOP-B9L203E / LAPTOP-D73A8DIE): Passo 1 sul peer, Passo 2 elevato sul
target con la rispettiva pubkey. Igiene: la chiave privata vive SOLO sul
peer; rimuovi eventuali copie locali post-trasferimento.

**Riferimenti**: JOURNAL 2026-05-17 (caso Ryzen->Lenovo), CLAUDE.md
§Ecosistema device (IP fleet), `scripts/setup/setup-ssh-inbound.ps1`.

---

# Appendice A -- Inventario fleet (PRIVATO)

> L'inventario fleet dettagliato (hostname, IP, MAC, HW, chiavi SSH, matrice
> connettivita) e' stato spostato nello store privato sovrano per la pubblicazione
> del repo (2026-06-17). Vedi: `<private fleet store: ~/.claude/reference/fleet-topology.md>`
> (sincato cross-fleet via scripts/fleet/sync-claude-global.ps1, NON nel repo pubblico).

# Appendice B — Sorgente completo `scripts/setup/setup-ssh-inbound.ps1`

```powershell
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
```
