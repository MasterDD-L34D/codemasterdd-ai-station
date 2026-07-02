# autoresearch -- setup fleet + WSL2 runbook

> Setup e lezioni operative per [karpathy/autoresearch](https://github.com/karpathy/autoresearch)
> ("autonomous pretraining research swarm": un agent modifica `train.py`, addestra 5 min su
> GPU singola, tiene/scarta in base a `val_bpb`). Sessione 2026-07-02, Claude Code su Ryzen.

## Perche ci interessa

- Bench locale per esperimenti LLM-training agent-driven (pattern keep/discard = Quality Gate).
- Ha validato la pipeline **WSL2 + CUDA + torch** sul Ryzen: infrastruttura riusabile per
  futuri finetune/LoRA (es. `ferrospora-lora-dataset` sul Lenovo) e per generazione contenuti
  Evo-Tactics (flavor text, nomi creature, art prompt) con modelli addestrati in casa.
- Ha misurato (non stimato) il tetto VRAM utile del 4070S sotto WSL.

## Stato installazione fleet (2026-07-02)

| Cosa | Ryzen | Lenovo |
|---|---|---|
| Clone Windows `C:\dev\autoresearch` | reference-only (deps+data ok, train NON gira) | reference-only (idem) |
| `uv sync` (torch 2.9.1+cu128, CUDA verificato) | fatto | fatto |
| `prepare.py` (data + tokenizer vocab 8192) | fatto | fatto (29.4s) |
| Ambiente train funzionante | **WSL2 Ubuntu 26.04, repo in `/root/autoresearch`** | assente (WSL da fare se serve) |

## Blocker HARD su Windows nativo (non aggirabili senza fork)

1. `flash-attn3` (kernels-community): nessuna build variant Windows
   (`torch29-cu128-x86_64-windows` inesistente). `train.py:24` lo importa hard.
2. `uv.lock` pinna triton a `sys_platform == 'linux'`; `train.py` usa
   `torch.compile(fullgraph=True)` che richiede triton -> InductorError su Windows.

Conclusione: il repo e' Linux-only by design (target H100). Via corretta = WSL2.

## Setup WSL2 (Ryzen, replicabile su Lenovo)

```powershell
wsl --install -d Ubuntu --no-launch   # WSL feature gia' attiva se c'e' docker-desktop
```

```bash
# dentro WSL (root ok)
apt-get update && apt-get install -y gcc g++        # triton compila moduli C a runtime
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone --depth 1 https://github.com/karpathy/autoresearch.git ~/autoresearch
cd ~/autoresearch && uv sync                        # wheels Linux: torch cu128 + triton + fa3
uv run prepare.py                                   # one-time: data + tokenizer
uv run train.py                                     # smoke 5-min
```

Regole:
- Clone DENTRO il filesystem WSL (`~/`), MAI su `/mnt/c` (NTFS = venv/IO lenti).
- GPU passthrough: basta il driver NVIDIA host (nessun driver dentro WSL).

## Gotcha fleet (validi oltre autoresearch)

- **hermes python shim rotto su ENTRAMBE le macchine**: `...\hermes\hermes-agent\venv\Scripts\python.exe`
  primo nel PATH, fallisce con os error 448 ("punto di montaggio non attendibile") e manda in
  errore `uv` bare su Windows. Workaround: `uv sync --python <path-python-reale>` e run via
  venv python diretto (`.venv\Scripts\python.exe`). Python reali: Ryzen
  `%LOCALAPPDATA%\Programs\Python\Python313`, Lenovo `...\Python312`.
- **`DEVICE_BATCH_SIZE` vincolato**: `assert TOTAL_BATCH_SIZE % (batch*seq) == 0` con
  TOTAL=2^19 e seq=2048 -> batch validi = divisori di 256 (16/32/64...). Niente 24.
- **Tetto VRAM utile ~10GB su 4070S/WSL**: oltre, il driver WSL spilla su RAM condivisa
  SENZA errore OOM -> throughput dimezzato silenziosamente. Sintomo: MFU crolla, `peak_vram`
  vicino al nominale. Vale per qualunque training locale sotto WSL.

## Risultati sweep batch (5-min budget, depth 8, 50.3M param)

| Batch | val_bpb | MFU | peak VRAM | Esito |
|---|---|---|---|---|
| 16 | **1.2735** | 4.88% | 6.15GB | ottimo confermato (config attiva) |
| 32 | 1.6548 | 1.92% | 11.70GB | spill RAM condivisa, -55% token |
| 24 | -- | -- | -- | invalido (vincolo grad-accum) |

Margine inesplorato: 6.15GB usati su ~10 utili -> leve future = DEPTH 10-12, WINDOW_PATTERN, LR.
Log completi: vault `Extras/ollama-runs/2026-07-02-autoresearch-train-*-wsl.log`.

## Prossimi passi possibili

1. Agent-mode: puntare un agent su `~/autoresearch/program.md` (sandbox dedicata,
   permessi disattivati SOLO li' -- vedi README upstream) e lasciarlo iterare overnight.
2. Lenovo: replicare setup WSL se serve secondo banco (8GB VRAM -> batch 8, non 16;
   nota vincolo divisori: 8 valido).
3. Riusare la pipeline WSL2+CUDA per LoRA su dataset propri (ferrospora).

## Riferimenti

- Upstream: https://github.com/karpathy/autoresearch (README + tweet linkati li')
- Memoria sessione Claude: `~/.claude/projects/C--Users-VGit/memory/fleet_thirdparty_skill_tools.md` (Ryzen)
- SSH fleet: `docs/runbook/ssh-inbound-fleet-setup.md`
