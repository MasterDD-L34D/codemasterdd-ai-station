# Jules lane -- operating policy

Status: ACCEPTED (Eduardo, sessione 2026-07-02 notte: "seguiamo tutte le tue
raccomandazioni operative d'ora in poi"). Questo e' il layer di POLICY sopra i
documenti operativi -- qui vivono le decisioni di cadenza/priorita'/perimetro;
i dettagli di esecuzione NON si duplicano qui.

SoT collegati (leggi quelli per il COME):
- Loop operativo: `docs/runbook/godot-doc-comment-campaign-handoff.md`
- Inventario schemi + mappa riuso: `docs/research/jules-schema-reuse-2026-07-02.md`
- Doctrine e gotcha vivi: memory `feedback_jules_loop_operational`
- Stato coda campagna: GGv2 `docs/godot-v2/doc-comment-campaign.md` (tracker = SoT)

## Decisioni

1. **Campagna doc-comment GGv2 = FILLER-ONLY.** Max 1 giro trio per sessione,
   solo in coda a sessioni con ALTRO focus e a quota Jules ferma (10-15 min).
   MAI sessioni dedicate alla campagna. Razionale: polish DX inerte, fuori dal
   critical path (baricentro = playtest).
2. **Stop definitivo al tail.** Il pool clean residuo (~12 file @ 131/280, 47%)
   si consuma a filler (~4 giri, arrivo ~51%); a pool vuoto la campagna CHIUDE
   con nota finale nel tracker. Il tail (>150L / zero-public-func / high-NA
   host-views) NON si lavora. **100% di coverage NON e' un obiettivo**: il
   valore sta nei tooltip delle API realmente usate in editor, gia' coperte.
3. **Priorita' dispatch Jules**: L3 characterization-test sui tool playtest Game
   (analyze_telemetry, dashboard pipeline) appena churn fermo >=3-5 giorni --
   valore diretto sul fronte caldo; template = task statblock 2026-06-25;
   delivery PR-to-owner con "do NOT merge". Poi L1 filler. L6 (report judgment)
   e L7 (i18n/stringhe player-facing) restano NO-GO.
4. **Perimetro auto-merge**: lane doc-comment GGv2 (batch + tracker regen) +
   lane L3 char-test gate-verdi (vedi Addendum 2026-07-06). Ogni altra lane
   parte PR-to-owner; merge esterno = Eduardo esplicito (ADR-0037). Nessuna
   estensione senza ok esplicito.
5. **Gate = necessario NON sufficiente.** Il ground-truth meccanico (dels==0,
   only-target, ASCII-add, nonDocAdds==0, adds==spec, gdformat/gdlint) resta
   obbligatorio, MA il placement richiede spot-check umano del patch (lezione
   batch-33 v1: class-## sopra la blank line = doc staccato, gate verde).
6. **Prompt rules baked** (ogni task-file): strict-prompt con fn-list esatta e
   testo ## verbatim; "NO blank line tra il blocco ## e class_name"; <=100
   char/riga (gdlint); churn-gate >=3-5gg su OGNI target prima del dispatch.
7. **Recovery standard**: delivery-miss (COMPLETED + zero outputs + activities
   `{}`) -> re-GET dopo ~2 min -> re-dispatch stesso task-file. FAILED con
   outputs vuoti -> snapshot early da activities (L-031). Mai -ForceBlind.

## Addendum 2026-07-06 -- estensione perimetro merge (autorizzazione Eduardo)

Autorizzazione esplicita Eduardo (sessione 2026-07-06 sera, AskUserQuestion
"Merge grant" -> scelta "Char-test gate-verdi + filler"): il perimetro
auto-merge si estende ai PR della lane **L3 characterization-test su Game**,
SOLO se TUTTO il gate stack e' verde:

- patch byte-identical allo spec pre-provato embedded nel task-file
  (pre-verifica di ogni assert contro il modulo reale PRIMA del dispatch);
- dels == 0; UN solo file nuovo (il test target); ASCII-only;
- full `pytest tests/` collect senza errori/collisioni di basename + test file
  verde in locale;
- CI del PR verde (python-tests + ci-gate) PRIMA del merge.

Qualsiasi segnale giallo (uno qualunque dei punti sopra, o anomalia di
placement/scope) -> fallback PR-to-owner come prima, merge = Eduardo.
Restano INVARIATI: doctrine-files = Eduardo-only-merge (ADR-0037 decisione 2),
nessuna lane nuova in auto-merge senza ok esplicito, freeze paths mai toccati.
Il grant e' ATTIVO dal merge (Eduardo) di questo addendum; revocabile con una
riga in questo doc.

## Trigger di revisione

- Pool clean esaurito -> chiusura campagna (nota nel tracker, riga in JOURNAL).
- Churn `tools/` Game fermo >=3-5gg -> attivare L3 (ricontrollo ~2026-07-05).
- Proposta di lane nuova -> parte PR-to-owner + autorizzazione esplicita.
- Contraddizione con un ADR futuro -> vince l'ADR, aggiorna questo doc.
