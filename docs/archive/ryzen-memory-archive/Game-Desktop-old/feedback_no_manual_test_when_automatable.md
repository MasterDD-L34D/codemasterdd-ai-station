---
name: No manual test when automatable
description: User dice "inutile perdere tempo nei test umani" se Claude/agent può testare programmatic. Switch automatic test harness via subagent.
type: feedback
originSessionId: 43af369a-a1ea-416b-87cb-0cbe6f22509e
---
User feedback 2026-05-06 phone smoke loop: "senti è inutile che perdiam o tempo nei test umani! qui manca ancora un sacco di cose abbiam o detto che la scelta così non è adatta.. ed è inutile testare a mano queste cose se puoi testarle tu o i tuoi agenti!"

**Why**: phone smoke loop iterativo con master-dd phone retest dopo ogni fix sprecato tempo umano quando:
1. WS flow è programmatic-testable via Node `ws` client
2. Architectural design gap (canonical vs shipped) NON si risolvono retesting, solo speccando upfront
3. Subagent (coop-phase-validator + narrative-design-illuminator) fanno audit + spec parallel mentre Claude continua

**How to apply**:
- Default automatic prima di proporre human test loop: scrivi script harness Node/Python ws/HTTP per coprire happy path + failure modes
- Spawn parallel subagent per gap audit / spec design upfront PRIMA di shipping fix iterativo
- Manual human test SOLO quando: (a) UX/visual judgment needed, (b) hardware-specific (phone touch, gyro, audio), (c) subagent harness ha already PASSED + want final smell test
- NO manual retest dopo ogni backend patch — batch fix multipli, run harness, ship singolo PR
- Se trova architectural drift (canonical vs shipped), STOP iterative fix, spawn spec agent first
