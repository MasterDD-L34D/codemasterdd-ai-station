# Offensive tooling awareness -- Noctis / ReconForge (2026-06-30)

Status: defensive awareness note (NON adottati). Prodotto durante valutazione 5-tool
(Ponytail/knip/Noctis/ReconForge/Medusa). Scope: capire COSA fanno per il lato difensivo
(owasp-security-auditor), senza integrarli nel fleet.

## Perche' questa nota (e non l'adozione)

Tu sei defensive + dev, non red-team con engagement autorizzati. Integrare tooling offensive
nel fleet = superficie di rischio (supply-chain, OPSEC, misalign posture) senza un caso d'uso
reale. Questa nota documenta le capacita' per riconoscerle/difendersi, non per usarle.

## NoctisAI -- malware-development / threat-intel MCP

- Cosa e': MCP server (Model Context Protocol) per "advanced malware development", threat-intel,
  OSINT, forensic, con generazione codice AI-assistita "OPSEC-aware" per red-team.
- Categoria: **offensive / malware-dev**. Dichiarato "authorized research & education only".
- Risk per il fleet: un MCP che genera malware con OPSEC-awareness, agganciato a un agente con
  tool-use, e' esattamente la classe di componente che NON vuoi nel tuo ambiente sovereign.
  Ecosistema "Villager AI" -> supply-chain non verificabile.
- Lato difensivo (cosa ti serve sapere): esistono MCP che weaponizzano agenti LLM per
  generare/offuscare payload. Detection angle: monitora MCP server registrati (`claude mcp list`),
  nega MCP non firmati/non auditati, tratta "OPSEC-aware code generation" come IoC.

## ReconForge (e fork same-name) -- recon bug-bounty/pentest

- Cosa e': toolkit/installer che orchestra strumenti OSS standard di reconnaissance --
  subfinder/amass (subdomain enum), httpx (live host), katana (crawl), nmap (port scan),
  nuclei (vuln templating), whatweb (fingerprint). Vari fork GitHub stesso nome.
- Categoria: **offensive recon** (dual-use). Legittimo SOLO con autorizzazione esplicita
  sull'asset target.
- Fit reale per te: marginale. Utile se un giorno fai attack-surface mapping sui TUOI asset
  (es. subdomain enum di un tuo dominio prima di esporre un servizio). In quel caso: scegli UN
  fork, pinnalo a commit, leggi lo script prima (gli installer "one-script" tirano giu' decine
  di binari -- audit obbligatorio), giralo in sandbox.
- Lato difensivo: questi sono esattamente gli strumenti che un attaccante punta contro di te.
  Difesa = riduci attack surface (subdomain inventory tuo, chiudi porte, rate-limit), e i
  template nuclei pubblici sono anche una checklist di hardening (gira nuclei sui tuoi servizi
  con autorizzazione = self-audit).

## Bottom line

- Noctis: 🔴 mai integrare. Awareness-only (riconoscere MCP-weaponization).
- ReconForge: 🟠 defer. Se mai serve self-recon autorizzato, 1 fork pinnato + audit + sandbox.
- Entrambi NON entrano nel fleet senza un caso d'uso autorizzato concreto e un audit completo.

Ref: valutazione completa in JOURNAL / chat 2026-06-30. Doctrine: build-on-existing,
audit-then-replay, dual-use = authorization-gated.
