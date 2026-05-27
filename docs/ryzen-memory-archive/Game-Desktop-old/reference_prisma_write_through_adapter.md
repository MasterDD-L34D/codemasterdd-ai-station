---
name: Prisma write-through adapter pattern
description: Pattern ripetibile per store con cache in-memory + persistence Prisma opzionale senza breaking sync API. Stabilito M12 Phase D, riusato M13 P3.
type: reference
originSessionId: 159549ac-0389-45ef-aae1-e9f52e290596
---
Pattern canonico per store che devono supportare sia in-memory (dev/test) sia Prisma (prod) senza forzare route API async.

## Shape funzione fabbrica

```js
function createXStore({ prisma = null, logger = null } = {}) {
  const states = new Map();
  const usePrisma = prismaSupportsX(prisma);
  const log = logger || console;

  function persistAsync(key, next) {
    if (!usePrisma) return;
    prisma.xTable
      .upsert({ where: ..., create: ..., update: ... })
      .catch((err) => log.warn?.('[xStore] upsert failed:', err?.message || err));
  }

  function get(key) { /* sync Map read */ }
  function set(key, state) {
    const next = { ...state, updated_at: Date.now() };
    states.set(key, next);
    persistAsync(key, next);   // fire-and-forget
    return { ...next };
  }

  async function hydrate(scope) {
    if (!usePrisma) return 0;
    try {
      const rows = await prisma.xTable.findMany({ where: ... });
      for (const row of rows) states.set(key, fromRow(row));
      return rows.length;
    } catch (err) {
      log.warn?.('[xStore] hydrate failed:', err?.message || err);
      return 0;
    }
  }

  return { get, set, hydrate, _mode: usePrisma ? 'prisma' : 'in-memory' };
}

function prismaSupportsX(prisma) {
  return Boolean(
    prisma &&
      prisma.xTable &&
      typeof prisma.xTable.upsert === 'function' &&
      typeof prisma.xTable.findMany === 'function',
  );
}
```

## Invarianti

1. **API sync** preservata: route layer non deve cambiare.
2. **Fail-safe**: upsert/deleteMany catch → warn log, in-memory cache autoritativa.
3. **Detection**: `prismaSupportsX(prisma)` guard — stub prisma client (senza la delegate richiesta) cade gracefully a in-memory.
4. **Hydrate opt-in**: chiamare `store.hydrate(scope)` solo se serve restart recovery; tests in-memory skip.
5. **`_mode`** introspection field per debug + test.

## Test coverage richiesto

- `prismaSupports` detection (client valido + null + partial)
- `_mode` reports correctly per entrambi i path
- Write-through: seed/apply triggers upsert (mock prisma verify)
- Hydrate: pre-seed rows nel mock → findMany popola Map
- Clear scope: deleteMany invoke + in-memory cleanup
- Failure fallback: upsert reject → in-memory state resta corretto

## Esempi live

- `apps/backend/services/forms/formSessionStore.js` (M12 Phase D, `FormSessionState`, migration 0003)
- `apps/backend/services/progression/progressionStore.js` (M13 P3, `UnitProgression`, migration 0004)
- `apps/backend/services/metaProgression.js` — pattern precedente (async API, meno riusabile; nuovi store devono seguire write-through sync).

## Quando NON usare

- Se i callers già sono async (es. route handler già `async`): stile `metaProgression` pattern va bene.
- Se la persistence deve essere strongly-consistent (ack required): promise chain esplicita + error propagation.
- Se il volume writes è alto (>100/s): considerare batch flush invece di upsert-per-write.
