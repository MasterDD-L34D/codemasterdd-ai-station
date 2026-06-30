# Evo-Swarm weekly digest — pending Game issue draft (2026-04-27)

> Body draft per issue su `MasterDD-L34D/Game`. Estratto automaticamente dal weekly digest evo-swarm
> (window 2026-04-20 → 2026-04-27, 432 cicli swarm, 5 proposte tracked).
> Source: `docs/exports/EXPORT-FOR-GAME-REPO-2026-04-27.md`.

## Top match diretti (2 entry)

Specie su cui lo swarm ha lavorato e che esistono già nel canonical Game (`legacy_slug`):
output swarm direttamente integrabile.

1. **`polpo_araldo_sinaptico`** ↔ canonical `polpo_araldo_sinaptico`
   (IT: *Polpo Araldo Sinaptico* / EN: *Synaptic Herald Octopus*) — cicli swarm #11, #1, #29
2. **`dune_stalker`** ↔ canonical `dune_stalker`
   (IT: *Dune Stalker* / EN: *Dune Stalker*) — cicli swarm #2, #119, #2, #1, #12

> Solo 2 match diretti questa settimana (target era top 3): la pipeline conferma che lo swarm
> sta producendo lore/biome ma con basso overlap con `legacy_slug` canonical. Coverage gap sotto.

## Top coverage gap (top 5 di 50)

Entry canonical Game (`species_expansion.yaml`) che lo swarm **non ha mai discusso**.
Candidati input per prossimi cicli swarm.

1. `arenavolux-sagittalis` — *Saettatore delle Dune* / *Dune Skiver*
2. `ferriscroba-detrita` — *Spazzino Ferroso* / *Rust Scavenger*
3. `sonapteryx-resonans` — *Ala Risonante* / *Echo Wing*
4. `lithoraptor-acutornis` — *Cacciatore di Schegge* / *Shard Prowler*
5. `salifossa-tenebris` — *Scavatore Salino* / *Salt Burrower*

(altre 45 entry nel file digest, sezione "Coverage gap").

## Riferimenti

- Digest completo: `docs/exports/EXPORT-FOR-GAME-REPO-2026-04-27.md`
- Game HEAD analizzato: `5f42757a` (CAP-15 phase merge)
- Pipeline: `scripts/swarm-to-game-export.py --since 2026-04-20 --game-repo C:/dev/Game`

---

Issue body pronto. Eduardo: copia-incolla in `gh issue create --repo MasterDD-L34D/Game` se vuoi farlo lunedì.
