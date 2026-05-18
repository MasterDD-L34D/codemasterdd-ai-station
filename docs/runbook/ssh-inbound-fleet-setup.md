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
ssh edusc@192.168.1.10            # IP target stampato a fine script
# prima volta: accetta il fingerprint host (yes)
```

Verifica annidata (se hai accesso al peer via un terzo canale):
```
ssh -i <fleetkey> Vgit@<peer-ip> "ssh -i C:/Users/Vgit/.ssh/id_ed25519 -o StrictHostKeyChecking=accept-new edusc@192.168.1.10 whoami"
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
