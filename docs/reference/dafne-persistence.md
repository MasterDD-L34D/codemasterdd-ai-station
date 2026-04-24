# Dafne swarm persistence — opzioni operative

> Il server Dafne (`START-SWARM.ps1`) è un Python foreground process. Se la
> PowerShell parent chiude, il processo muore. Questo documento elenca 3
> opzioni per mantenere Dafne up quando serve.

## Problema osservato 2026-04-24

Sessione auto-mode ha restartato Dafne 2× via `Start-Process -WindowStyle Minimized`,
ma entrambe le volte il processo è morto dopo ~10-30 min senza intervento utente.
Probabile causa: quando la PowerShell figlio esce dopo aver lanciato Python (o crash
senza traceback visibile), il process Python continua ma senza stdout/stderr catturato
e senza restart. L'integration dogfood-ui `/dafne` panel mostra `reachable: false`.

## Opzione 1 — Wrapper auto-restart (consigliata per use saltuario)

File: `C:/Users/edusc/Dafne/workspace/swarm/START-DAFNE-PERSISTENT.ps1`

Usage:
```powershell
cd C:\Users\edusc\Dafne\workspace\swarm
.\START-DAFNE-PERSISTENT.ps1
# Lascia la finestra aperta (o minimized). Ctrl+C per stop.
```

Features:
- Auto-restart su qualsiasi exit code
- Safety circuit breaker: se >20 restart/ora, stop per evitare bootloop
- Log rotation giornaliera in `logs/dafne-YYYY-MM-DD.log`
- Exit clean dopo >5min chiede conferma (evita restart accidentale)

**Limite**: la finestra PowerShell deve restare aperta. Se chiudi la shell, Dafne muore.

## Opzione 2 — Windows Task Scheduler (consigliata per always-on)

Registra Dafne come Scheduled Task triggered `At log on` con auto-restart-on-fail.
Richiede PowerShell admin.

```powershell
# Esegui come Administrator
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File C:\Users\edusc\Dafne\workspace\swarm\START-DAFNE-PERSISTENT.ps1"

$trigger = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERNAME"

$principal = New-ScheduledTaskPrincipal `
    -UserId "$env:USERNAME" `
    -LogonType Interactive `
    -RunLevel Limited

$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -DontStopOnIdleEnd `
    -ExecutionTimeLimit ([TimeSpan]::Zero) `
    -RestartOnFailure `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -RestartCount 3

Register-ScheduledTask `
    -TaskName "Dafne-Swarm-Persistent" `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings `
    -Force

# Verifica
Get-ScheduledTask -TaskName "Dafne-Swarm-Persistent"

# Avvio immediato senza aspettare next logon
Start-ScheduledTask -TaskName "Dafne-Swarm-Persistent"
```

Rimozione (se vuoi togliere):
```powershell
Unregister-ScheduledTask -TaskName "Dafne-Swarm-Persistent" -Confirm:$false
```

**Limite**: modifica sistema globale. Task visibile in Task Scheduler UI.

## Opzione 3 — Dockerize (long-term, non urgente)

Dafne swarm potrebbe essere containerizzato (Python 3.12 + Flask + Ollama client
via host.docker.internal:11434). Avrebbe `restart: unless-stopped` policy e si
integrerebbe con il stack infra/ ADR-0017.

**Pro**: consistency con LiteLLM/Langfuse, no process hygiene issue
**Contro**: richiede Dockerfile nel repo `evo-swarm` + writing to `C:/dev/Game/`
  che dal container necessita bind-mount (complessità).
**Status**: deferred, non trigger concreto (Opzione 1 o 2 coprono 90% use case).

## Raccomandazione

- **Sviluppo attivo sessione Dafne** (es. day-5, triage proposals): Opzione 1
  (launcha quando serve, vedi log nella shell)
- **Always-on background** (monitor 24/7): Opzione 2 (task scheduler)
- **Build containerized ecosystem**: Opzione 3 (post Fase 7 transition)

## Verifica persistence

Dopo setup, verifica:
```bash
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:5000/api/status
# Atteso: HTTP 200
```

Se dogfood-ui up, panel `/dafne` mostra live data anche post-system-idle.

## Riferimenti

- `START-DAFNE-PERSISTENT.ps1` — wrapper custom (Opzione 1)
- `STATUS_MULTI_REPO.md` — tracking operativo Dafne state
- `apps/dogfood-ui/dafne_client.py` — client con ping_timeout=2s, timeout=5s
- Microsoft docs: [Register-ScheduledTask](https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/register-scheduledtask)
