# Ponytail LOC-claim falsification (2026-06-30)

Status: **RATIFICATO N=40** (20 task x 2 sample, 10 micro + 10 medium). Supersede il
direction-probe N=10 iniziale (riportato in fondo).

## Verdetto ratificato (N=40)

| | baseline | ponytail |
|---|---|---|
| osservazioni | 40 | 40 |
| mean LOC | 8.55 | 6.08 |
| correttezza | 40/40 (100%) | 39/40 (98%) |
| delta LOC paired (20 task) | -- | **-25.4%** |

- Effetto REALE ma **~-25%**, NON il -54% vendor. Il claim 54% e' cherry-picked su task
  golfabili.
- **Magnitudo dipende dalla golfabilita' del task**: micro golfabili enormi (is_ipv4 -71%,
  merge_sorted -62%, fizzbuzz -50%); medium a logica irriducibile = 0% (normalize_config,
  dict_diff, paginate, expand_template, top_k_words). Su task reali medi il guadagno e' piccolo.
- **"100% safety" FALSIFICATA**: ponytail ha rotto 1/40 (`calc`, one-liner che raise) -> 98%.
  L'one-lining aggressivo introduce un rischio-correttezza reale, anche se piccolo.
- Conferma la SDMG-skepticism: i numeri vendor self-reported erano ottimistici. Aspettativa
  realistica = ~25% meno LOC con piccolo rischio regressione su logica complessa.

## Implicazione adozione

ADOPT confermato (beneficio reale), MA: always-on su lavoro tier-0/strategico = attenzione
all'over-simplification su logica complessa (dove il guadagno e' ~0 e il rischio correttezza
e' non-zero). Opt-in per-task resta l'uso piu' sicuro; default mode `full` (non `ultra`).

---

## (storico) direction-probe N=10

Status: direction-probe (N=10). Indipendente, controllato.

## Claim sotto test

DietrichGebert/ponytail (skill AI "lazy senior dev") dichiara ~-54% codice
(self-reported, nessun bench indipendente -> SDMG vendor da falsificare).

## Metodo

- 10 micro-task Python a firma fissa (fizzbuzz, parse_kv, flatten1, balanced,
  group_first, dedupe_consecutive, roman_to_int, top_k_words, is_ipv4, merge_sorted).
- 2 arm via subagent (workflow fan-out, stesso modello Opus):
  - baseline: "implementa, solo codice funzione".
  - ponytail: stesso prompt + ruleset ponytail (la ladder + rules) iniettato.
- Entrambi vincolati "solo codice, no test/comment/prose" -> isola LOC della soluzione.
- Correttezza: test NASCOSTI (non visti dagli agent), eseguiti dal grader post-hoc.
- LOC = righe non-vuote non-comment.

## Risultato

| | baseline | ponytail | delta |
|---|---|---|---|
| LOC totali | 84 | 49 | **-41.7%** |
| Correttezza | 10/10 | 10/10 | +0 |

10/10 task: ponytail LOC <= baseline. Vincite nette: fizzbuzz 12->2, is_ipv4 12->3,
roman_to_int 12->3, dedupe 6->3. Pareggi dove gia' minimale: merge_sorted 3=3,
balanced 10=10, parse_kv 10=10, top_k_words 4=4.

## Verdetto

DIREZIONALMENTE CONFERMATO. Effetto reale, ~-42% LOC, zero costo correttezza
("100% safety" regge su questo sample). Vendor 54% vs mio 42% = stessa direzione,
magnitudo sotto headline.

## Caveat (onesti)

1. N=10 = direction-probe, NON N=40 ratify. Signal forte/consistente ma non ratificato.
2. Micro-task a firma fissa = bassa superficie di over-engineering. Il valore "vero"
   di ponytail (saltare intere astrazioni/file) NON emerge qui -> -42% e' su task dove
   la leva e' solo terseness. Su task grandi il delta potrebbe allargarsi (verso 54%)
   o assottigliarsi: ignoto senza task piu' grandi.
3. Stesso modello entrambi gli arm: misura l'effetto puro del prompt-injection. Pulito.
4. Correttezza giudicata da test indipendenti dalla generazione. OK.

## Azione

ADOPT giustificato (gia' installato opt-in `~/.claude/skills/ponytail/`). Escalation a
hook always-on (come caveman) = ragionevole vista l'evidenza, ma decisione Eduardo.
Per ratifica completa: N=40 + includere task medi (multi-funzione, con tentazione di
astrazione) dove il claim 54% probabilmente vive.

Harness riproducibile: scratchpad `ponytail_grader.py` + workflow `ponytail-loc-falsification`.
