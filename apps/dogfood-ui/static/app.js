// Minimal JS — per ora solo confirm dialogs e fetch helpers.
// Espandibile in futuro per live stats polling, filter UI, etc.

(function () {
    'use strict';

    // Nothing heavy yet — Jinja templates gestiscono rendering server-side.
    // Fetch helper available globally se i template vogliono usarlo:
    window.cmdFetch = async function (url, opts = {}) {
        const defaults = {
            headers: { 'Content-Type': 'application/json' },
            credentials: 'same-origin',
        };
        const response = await fetch(url, { ...defaults, ...opts });
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return response.json();
    };
})();
