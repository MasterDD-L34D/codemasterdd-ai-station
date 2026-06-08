# Runbook — ADR STATUS-CHECK (status-lifecycle owner)

> Process-fix da retrospettiva B1 2026-05-18 (Decisione 009). Malattia
> diagnosticata: **assenza owner del status-lifecycle** — ADR Proposed /
> Accepted-early scritti con una check-date che nessuno rilegge → 6
> STALE-STATUS rotting. Fix: check-date **machine-greppable** + audit
> ricorrente. NO script bespoke (gold-plating): un grep + scheduler basta.

## Schema STATUS-CHECK

Ogni ADR non-finale (Proposed / Accepted-early) porta UNA riga, subito
dopo la riga `Status`, in formato fisso:

```
STATUS-CHECK: YYYY-MM-DD | trigger: <condizione> | default-if-elapsed: <Accept|Reject|Escalate>
```

Quando l'ADR diventa finale (Accepted pieno / Superseded / Rejected):
rimuovere la riga STATUS-CHECK (non ha piu' senso tracciarlo).

## Audit one-liner (PowerShell, no script-file)

Esegui dalla root repo. Stampa gli ADR con check-date <= oggi:

```powershell
$t=Get-Date; Get-ChildItem docs/adr/*.md | Select-String 'STATUS-CHECK:\s*(\d{4}-\d{2}-\d{2})\s*\|\s*trigger:\s*(.+?)\s*\|\s*default-if-elapsed:\s*(\w+)' | ForEach-Object { foreach($m in $_.Matches){ $d=[datetime]$m.Groups[1].Value; if($d -le $t){ "{0} DUE {1} ({2}gg) -> {3} | {4}" -f $_.Filename,$m.Groups[1].Value,[int]($t-$d).TotalDays,$m.Groups[3].Value,$m.Groups[2].Value } } }
```

Exit-on-due (per cron alerting): wrappa con
`...; if($LASTEXITCODE){exit 1}` o controlla output non-vuoto.

## Scheduling (settimanale, Task Scheduler — pattern ADR-0019)

Registrazione one-shot (Eduardo, una tantum). Lunedi 09:00:

```powershell
$a = New-ScheduledTaskAction -Execute 'pwsh' -Argument '-NoProfile -Command "cd C:\dev\codemasterdd-ai-station; <one-liner sopra>"'
$tr = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 9am
Register-ScheduledTask -TaskName 'adr-status-check' -Action $a -Trigger $tr -Description 'ADR STATUS-CHECK weekly (Decisione 009)'
```

Alternativa low-tech: aggiungi l'one-liner al rituale mensile
`compass-check` (B2 programma) — un solo posto dove guardi la direzione.

## Stato annotazioni (applicate 2026-05-18)

| ADR | STATUS-CHECK | default-if-elapsed |
|-----|--------------|--------------------|
| 0016 constraint-count routing | 2026-06-09 | Escalate |
| 0021 multi-client (early) | 2026-06-07 | Accept |
| 0022 OpenCode tier (early) | 2026-06-09 | Accept |
| 0024 Vue3 archive timeline | RETIRED 2026-06-08 (reconciled) | -- |
| 0029 OpenRouter declined | 2026-06-13 | Accept |
| 0031 ChatGPT recovery | 2026-06-14 | Escalate |

ADR finali (0023 Superseded, 0030 Accepted, ecc.) = NO STATUS-CHECK.

## Procedura quando un ADR e' DUE

1. Verifica il `trigger`: condizione avvenuta? (es. n>=3 data point, >$5/mese x2).
2. Applica `default-if-elapsed`:
   - **Accept** → flip Status a Accepted, rimuovi STATUS-CHECK
   - **Reject** → flip a Rejected/Superseded, rimuovi STATUS-CHECK
   - **Escalate** → decisione cosciente Eduardo (no default automatico)
3. Aggiorna DECISIONS_LOG index + entry se cambia status.
4. Re-run audit → 0 due.

## Razionale anti-over-engineering

Un parser .ps1 dedicato sarebbe gold-plating (e TDD-guard lo blocca giustamente
senza test). La malattia non e' "manca un tool", e' "nessuno guarda". Un grep
+ trigger schedulato risolve al 100% le 6 STALE-STATUS senza nuovo codice da
mantenere/testare. Rif: Decisione 009, retrospettiva B1.
