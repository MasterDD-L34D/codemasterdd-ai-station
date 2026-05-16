#!/usr/bin/env node
'use strict';

// scrape-custom-gpts.js -- Playwright Option B per Custom GPTs config recovery
//
// Gap filler: brianjlacy/export-chatgpt esplicitamente esclude Custom GPTs
// (gizmo_type != 'snorlax'). Questo script scrapa via DOM la Configure panel
// di ogni GPT owned dall'utente, salvando name/description/instructions/
// conversation_starters/capabilities/knowledge_files.
//
// Auth: persistent browser context (riusa sessione login Chrome esistente).
// Resume: skip GPT gia' scrapati basandosi su output dir.
// Rate-limit: configurable delay tra azioni (default 2000ms).
//
// Run modes:
//   --auth-mode initial   : opens browser, user logs in manualmente, saves state
//   (default)             : usa state salvato, scrape headless
//
// Selectors DOM testati 2026-05. Possibili rotture se OpenAI cambia UI.

import { chromium } from 'playwright';
import { program } from 'commander';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const AUTH_STATE_PATH = path.join(__dirname, '.playwright-auth-state.json');

program
  .name('scrape-custom-gpts')
  .description('Scrape ChatGPT Custom GPTs config via Playwright (Option B gap filler)')
  .option('-o, --output <dir>', 'Output directory', './custom-gpts')
  .option('-d, --delay <ms>', 'Delay between actions (ms)', '2000')
  .option('--auth-mode <mode>', 'auth mode: "initial" (manual login first) or "saved" (use state)', 'saved')
  .option('--headless', 'Headless mode (only with --auth-mode saved)', false)
  .option('--gpt-url <url>', 'Scrape only a specific GPT URL (debug)')
  .option('--skip-knowledge', 'Skip downloading knowledge files (faster)', false)
  .option('--verbose', 'Verbose logging', false)
  .parse();

const opts = program.opts();
const DELAY = parseInt(opts.delay, 10);
const OUTPUT_DIR = path.resolve(opts.output);

function log(msg, ...rest) {
  console.log(`[${new Date().toISOString()}] ${msg}`, ...rest);
}

function vlog(msg, ...rest) {
  if (opts.verbose) log(`[VERBOSE] ${msg}`, ...rest);
}

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function sanitizeSlug(name) {
  if (!name) return 'untitled';
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .replace(/-{2,}/g, '-')
    .substring(0, 60) || 'untitled';
}

async function initialAuthFlow() {
  log('=== Initial auth mode: opening headed browser ===');
  log('1. A Chromium window will open');
  log('2. Login to chatgpt.com with your Business account');
  log('3. Verify workspace is "Area di lavoro di Master DD Business"');
  log('4. Close any onboarding dialogs');
  log('5. When ready, RETURN HERE and press Enter (or Ctrl+C to abort)');

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto('https://chatgpt.com/');

  // Wait for user to login + signal ready
  await new Promise((resolve) => {
    process.stdin.once('data', () => resolve());
    log('\n>>> Press Enter when login complete and ChatGPT main UI is visible...');
  });

  // Save auth state
  await context.storageState({ path: AUTH_STATE_PATH });
  log(`Auth state saved to ${AUTH_STATE_PATH}`);

  await browser.close();
  log('=== Auth setup complete. Re-run without --auth-mode initial to start scraping ===');
}

async function listOwnedGPTs(page) {
  log('Navigating to /gpts/mine ...');
  await page.goto('https://chatgpt.com/gpts/mine', { waitUntil: 'networkidle', timeout: 60000 });
  await sleep(DELAY);

  // Multiple selector strategies (UI variations 2026-04-05)
  const gptCardSelectors = [
    'a[href*="/g/g-"]',           // direct GPT URL links
    '[data-testid="gpt-card"] a', // testid-based
    'div[role="link"][href*="/g/"]'
  ];

  let gptLinks = [];
  for (const sel of gptCardSelectors) {
    gptLinks = await page.$$eval(sel, els => {
      return [...new Set(els.map(e => e.href).filter(h => h && h.includes('/g/g-')))];
    });
    if (gptLinks.length > 0) {
      vlog(`Selector ${sel} matched ${gptLinks.length} GPTs`);
      break;
    }
  }

  if (gptLinks.length === 0) {
    log('WARNING: zero GPTs detected. UI may have changed or you have no owned GPTs.');
    log('Manual fallback: open https://chatgpt.com/gpts/mine in browser, copy URLs of your GPTs, pass via --gpt-url one at a time.');
    return [];
  }

  log(`Found ${gptLinks.length} owned GPTs`);
  return gptLinks;
}

async function scrapeGPT(page, gptUrl, outDir) {
  log(`Scraping: ${gptUrl}`);
  await page.goto(gptUrl, { waitUntil: 'networkidle', timeout: 60000 });
  await sleep(DELAY);

  // Click "Configure" or kebab menu -> Edit
  const configureSelectors = [
    'button:has-text("Configure")',
    'a:has-text("Configure")',
    'button:has-text("Configura")',  // IT locale
    'button[aria-label*="Edit"]',
    'button[aria-label*="Configure"]'
  ];

  let configBtn = null;
  for (const sel of configureSelectors) {
    configBtn = await page.$(sel);
    if (configBtn) {
      vlog(`Configure button matched: ${sel}`);
      break;
    }
  }

  if (!configBtn) {
    log(`WARNING: Configure button not found for ${gptUrl}. UI may differ. Skipping.`);
    return null;
  }

  await configBtn.click();
  await sleep(DELAY);

  // Scrape fields (defensive: each in try/catch, fallback to '')
  const scrape = async (selector, fieldName, attr = 'innerText') => {
    try {
      const el = await page.$(selector);
      if (!el) {
        vlog(`Field "${fieldName}" not found via ${selector}`);
        return '';
      }
      if (attr === 'innerText') return (await el.innerText()).trim();
      return (await el.getAttribute(attr) || '').trim();
    } catch (e) {
      vlog(`Field "${fieldName}" scrape error:`, e.message);
      return '';
    }
  };

  // Selectors per Configure panel (best-effort, UI 2026-04)
  const name = await scrape('input[name="name"], input[placeholder*="Name"]', 'name', 'value');
  const description = await scrape('textarea[name="description"], textarea[placeholder*="Description"]', 'description', 'value');
  const instructions = await scrape('textarea[name="instructions"], textarea[placeholder*="instructions" i]', 'instructions', 'value');

  // Conversation starters (multiple inputs)
  let starters = [];
  try {
    starters = await page.$$eval('input[placeholder*="conversation starter" i], textarea[placeholder*="starter" i]',
      els => els.map(e => e.value).filter(Boolean));
  } catch (e) {
    vlog('Starters scrape error:', e.message);
  }

  // Capabilities (checkboxes for web browsing, DALL-E, code interpreter)
  let capabilities = {};
  try {
    capabilities = await page.evaluate(() => {
      const caps = {};
      document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
        const label = cb.closest('label')?.innerText?.trim() ||
                      cb.parentElement?.innerText?.trim() ||
                      cb.getAttribute('aria-label') || '';
        if (label) caps[label] = cb.checked;
      });
      return caps;
    });
  } catch (e) {
    vlog('Capabilities scrape error:', e.message);
  }

  // Knowledge files list (defensive: file names only, not download yet)
  let knowledgeFiles = [];
  try {
    knowledgeFiles = await page.$$eval(
      '[data-testid="knowledge-file"], [aria-label*="knowledge file" i], .file-attachment-name',
      els => els.map(e => e.innerText || e.getAttribute('aria-label') || '').filter(Boolean)
    );
  } catch (e) {
    vlog('Knowledge files scrape error:', e.message);
  }

  // Actions (if any) -- best-effort
  let actionsCount = 0;
  try {
    actionsCount = await page.$$eval('[data-testid*="action"], .action-item', els => els.length);
  } catch (e) {
    vlog('Actions count error:', e.message);
  }

  const config = {
    url: gptUrl,
    scraped_at: new Date().toISOString(),
    name,
    description,
    instructions,
    conversation_starters: starters,
    capabilities,
    knowledge_files: knowledgeFiles,
    actions_count: actionsCount,
  };

  const slug = sanitizeSlug(name) || `gpt-${Date.now()}`;
  const gptDir = path.join(outDir, slug);
  await fs.mkdir(gptDir, { recursive: true });
  await fs.mkdir(path.join(gptDir, 'knowledge'), { recursive: true });

  // Write config.md
  const md = [
    `# Custom GPT: ${name || 'Unknown'}`,
    '',
    '---',
    `url: ${gptUrl}`,
    `scraped_at: ${config.scraped_at}`,
    `slug: ${slug}`,
    `knowledge_files_count: ${knowledgeFiles.length}`,
    `actions_count: ${actionsCount}`,
    '---',
    '',
    `## Description`,
    description || '_(empty)_',
    '',
    `## Instructions (system prompt)`,
    '```',
    instructions || '_(empty)_',
    '```',
    '',
    `## Conversation Starters`,
    ...(starters.length ? starters.map(s => `- ${s}`) : ['_(none)_']),
    '',
    `## Capabilities`,
    ...Object.entries(capabilities).map(([k, v]) => `- ${k}: ${v ? 'ON' : 'OFF'}`),
    '',
    `## Knowledge Files (${knowledgeFiles.length})`,
    ...(knowledgeFiles.length ? knowledgeFiles.map(f => `- ${f}`) : ['_(none)_']),
    '',
    '## Actions',
    `Count: ${actionsCount}. Schema scrape NOT implemented (manual screenshot if needed).`,
  ].join('\n');

  await fs.writeFile(path.join(gptDir, 'config.md'), md, 'utf-8');
  await fs.writeFile(path.join(gptDir, 'config.json'), JSON.stringify(config, null, 2), 'utf-8');

  // Knowledge files download (best-effort, requires UI interaction)
  if (!opts.skipKnowledge && knowledgeFiles.length > 0) {
    log(`  Knowledge files: ${knowledgeFiles.length} detected. Manual download required.`);
    log(`  Note: OpenAI does NOT expose direct download endpoint for GPT knowledge files via public API.`);
    log(`  Workaround: click each file in Configure UI -> "Download" (if available) -> save to ${gptDir}/knowledge/`);
    // Future: programmatic download via signed URL extraction se OpenAI esponesse endpoint
  }

  log(`  Saved ${slug} -> ${gptDir}`);
  return slug;
}

async function isAlreadyScraped(gptUrl, outDir) {
  // Resume: check if any config.json in subdirs has matching url
  try {
    const subdirs = await fs.readdir(outDir, { withFileTypes: true });
    for (const d of subdirs) {
      if (!d.isDirectory()) continue;
      const configPath = path.join(outDir, d.name, 'config.json');
      try {
        const json = JSON.parse(await fs.readFile(configPath, 'utf-8'));
        if (json.url === gptUrl) return true;
      } catch (e) { /* ignore */ }
    }
  } catch (e) { /* output dir missing, ok */ }
  return false;
}

async function main() {
  if (opts.authMode === 'initial') {
    await initialAuthFlow();
    return;
  }

  // Verify auth state exists
  try {
    await fs.access(AUTH_STATE_PATH);
  } catch {
    console.error(`ERROR: auth state missing at ${AUTH_STATE_PATH}`);
    console.error('Run first: node scrape-custom-gpts.js --auth-mode initial');
    process.exit(1);
  }

  await fs.mkdir(OUTPUT_DIR, { recursive: true });

  log(`Output dir: ${OUTPUT_DIR}`);
  log(`Delay: ${DELAY}ms`);
  log(`Headless: ${opts.headless}`);

  const browser = await chromium.launch({ headless: opts.headless });
  const context = await browser.newContext({ storageState: AUTH_STATE_PATH });
  const page = await context.newPage();

  // Optional: only scrape one GPT for debug
  let gptUrls = [];
  if (opts.gptUrl) {
    gptUrls = [opts.gptUrl];
    log(`Single-GPT debug mode: ${opts.gptUrl}`);
  } else {
    gptUrls = await listOwnedGPTs(page);
  }

  if (gptUrls.length === 0) {
    log('No GPTs to scrape. Exiting.');
    await browser.close();
    return;
  }

  const results = { scraped: [], skipped: [], errors: [] };

  for (let i = 0; i < gptUrls.length; i++) {
    const url = gptUrls[i];
    log(`\n--- [${i + 1}/${gptUrls.length}] ${url} ---`);

    if (await isAlreadyScraped(url, OUTPUT_DIR)) {
      log('  Already scraped (resume). Skipping.');
      results.skipped.push(url);
      continue;
    }

    try {
      const slug = await scrapeGPT(page, url, OUTPUT_DIR);
      if (slug) results.scraped.push({ url, slug });
    } catch (e) {
      log(`ERROR scraping ${url}:`, e.message);
      results.errors.push({ url, error: e.message });
    }

    // Inter-GPT delay
    await sleep(DELAY);
  }

  // Write index
  const indexPath = path.join(OUTPUT_DIR, 'INDEX.md');
  const indexLines = [
    '# Custom GPTs Scrape Index',
    '',
    `Scraped at: ${new Date().toISOString()}`,
    `Total found: ${gptUrls.length}`,
    `Scraped: ${results.scraped.length}`,
    `Skipped (resume): ${results.skipped.length}`,
    `Errors: ${results.errors.length}`,
    '',
    '## GPTs scraped',
    ...results.scraped.map(g => `- [${g.slug}](${g.slug}/config.md) -- ${g.url}`),
    '',
    '## Errors',
    ...results.errors.map(e => `- ${e.url}: ${e.error}`),
  ].join('\n');
  await fs.writeFile(indexPath, indexLines, 'utf-8');

  log(`\n=== Done ===`);
  log(`Scraped: ${results.scraped.length} | Skipped: ${results.skipped.length} | Errors: ${results.errors.length}`);
  log(`Index: ${indexPath}`);

  await browser.close();
}

main().catch(e => {
  console.error('FATAL:', e);
  process.exit(1);
});
