# Asset Workspace Evo-Tactics — reference

**Path local**: `~/Documents/evo-tactics-refs/` (184GB, gitignored by design — DMCA mitigation public repo).

**Backup meta**: https://github.com/MasterDD-L34D/evo-tactics-refs-meta (private, ~8.5MB doc+scripts+URL lists, NO asset binaries).

## Trigger phrases (auto-recall)

- "asset workflow"
- "Skiv asset"
- "Path 1 / Path 2 / Path 3"
- "crea icona / sprite / SFX / portrait / animation / portrait HUD"
- "recipe Skiv"
- "echolocation pulse / wounded perma / sand-spell"
- "/asset-workflow"

## Quick recall paths

| Doc | Path | Use |
|-----|------|-----|
| Workflow primary repo | `docs/guide/asset-creation-workflow.md` | Path 1+2+3 canonical workflow |
| Workspace HANDOFF | `~/Documents/evo-tactics-refs/HANDOFF.md` | Recipes Skiv asset class + restore guide |
| Skiv refs extracted | `~/Documents/evo-tactics-refs/SKIV_REFS_EXTRACTED.md` | Filename-level extracted assets |
| File-level index | `~/Documents/evo-tactics-refs/MANIFEST.json` | 32136 file searchable JSON |
| Catalog top picks | `~/Documents/evo-tactics-refs/CATALOG_skiv.json` | top-15 picks per HF dataset |
| Tools install | `~/Documents/evo-tactics-refs/TOOLS.md` | 10/14 installed paths |
| CC0 sources | `~/Documents/evo-tactics-refs/CC0_SOURCES.md` | 16+ verified CC0 fonti |

## Tools installed (10/14)

LibreSprite + SLADE + Noesis + AssetStudio + Pixelorama + Laigter + Audacity + WFC + gltfpack + Tracery (auto-curl).
SKIPPED: Inkscape (use Pixelorama+AI), LDtk, MagicaVoxel, glTF-Validator (manual if needed).

## Asset library map

- `pixel-art-retro/`: Kenney (6 visual + 9 audio) + DENZI (1500+ pixel) + skiv-desert-pack (Wild Animals: Fox/Wolf/Boar/Deer 36-52x52 sprite + Hermit Sand) + skiv-icon-pack (536 PNG: FX 231 + glitch + RPG inventory) + skiv-character-sprites (Dog/snake/dino)
- `creature-anatomy/`: PhyloPic 581 SVG silhouette CC0 + skiv-concept-art (175+ Surt CC0 + Creature-cub PSD layered)
- `3d-models/`: wolf-skiv-ref (8 wolf FBX/blend) + quaternius-animals (Wolf/Cat/Dog/Fox/Dragon FBX+blend+obj) + skiv-biome-3d (Africa Savanna 493 + CAVE_PACK_PRO 272 + 3D Nature 160 + Desert Arena 53)
- `textures-pbr/`: ambientCG sand 20 PBR 1K materials
- `sound-fx/`: Kenney audio + FreePD music 1237 MP3 + Sonniss (Monthly+GDC5+GDC6 6691 audio royalty-free) + skiv-audio-kit 350 file curated (sand-spell.flac ⭐⭐⭐ + DRAGON + ALIEN GROWL + Hoof Gallop + Paw Trot + 80-CC0-creature 174 OGG)
- `oga-cc0-hf/`: HuggingFace OGA-CC0 dataset raw zip 47GB (2D 22 + 3D 20 + Concept 1.8 + SFX 3.7)

## Skiv-direct gold

- **3d wolf rigged** (Quaternius FBX) — Skiv quadruped 1:1
- **Red Fox** (Quaternius) — desert canid direct
- **Africa Savanna 493 file** — biome ref
- **sand-spell.flac** — echolocation/sand magic SFX direct
- **PhyloPic 581 CC0 SVG** — taxonomic codex
- **Wild Animals Wolf_Howl 16-frame** — Skiv calling pack gesture
- **DENZI cat 12 sprite 32x32** — feline pixel
- **DENZI god-abilities breathe variants** (46 icon) — Skiv echolocation/ancestor

## Workflow recipes (full in HANDOFF.md)

- Skiv portrait HUD 64x64: Path 1 — Fox_Idle slice → Pixelorama palette swap + dorsal stripes ~10min
- Skiv run cycle 36x36: Path 1 — Fox_Run slice 10 frame ~30min
- Skiv idle vocal: Path 4 — Audacity + Deep Breather pitch -2 semi
- Skiv combat roar: Path 4 — 80-CC0 roar_01 + Punch-Elem Whoosh layer
- Skiv echolocation pulse 800ms: Path 4 — sand-spell.flac trim + EQ HP 2kHz + reverb tail
- Skiv portrait Path 2: Retro Diffusion 10 varianti + Pixelorama polish 30min
- Skiv anatomy Path 3: Wolf_1 .blend study angles + close + redraw fresh

## Restore from fresh PC

```bash
git clone https://github.com/MasterDD-L34D/evo-tactics-refs-meta.git ~/Documents/evo-tactics-refs
# Re-install tools per TOOLS.md (~30 min manual)
cd ~/Documents/evo-tactics-refs
python robust_download.py urls-hf-2d-art.txt references/oga-cc0-hf/2d-art
# Repeat for each urls-*.txt → ~2h bandwidth + 184GB disk
python gen_manifest.py  # regen MANIFEST.json
```

## Cross-ref

- Workflow shipping: `Game/docs/guide/asset-creation-workflow.md`
- Policy canonical: `Game/docs/core/43-ASSET-SOURCING.md`
- ADR zero-cost: `Game/docs/adr/ADR-2026-04-18-zero-cost-asset-policy.md`
- Skill on-demand: `Game/.claude/skills/asset-workflow.md`
- CREDITS provenance: `Game/CREDITS.md`
