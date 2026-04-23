# TEMPLATE_MODEL_ROUTING_PROMPT

```text
Voglio definire il model routing reale di questo progetto.

Agisci come AI Workflow Architect.

Contesto progetto:
[incolla brief o compact]

Strumenti disponibili:
[es: ChatGPT, Claude Code, NotebookLM, OpenCode, Ollama, API provider esterni]

Vincoli:
- privacy:
- costo:
- hardware:
- velocità:
- integrazione col repo:

Voglio che tu mi costruisca un piano di routing pratico.

Per favore:
1. separa le fasi del lavoro: comprensione fonti, sintesi, planning, repo audit, coding, review, compact
2. per ogni fase scegli uno strumento e un modello principali
3. indica un fallback solo se davvero serve
4. spiegami perché quella scelta è corretta rispetto ai vincoli
5. dimmi cosa deve restare locale e cosa può andare in cloud
6. proponi una policy semplice: locale prima / cloud dopo, oppure altro, ma motivato
7. chiudi con una tabella finale pronta da copiare dentro MODEL_ROUTING.md

Non voglio una lista generica di modelli.
Voglio poche scelte, ruoli chiari, passaggi espliciti e anti-pattern da evitare.
```
