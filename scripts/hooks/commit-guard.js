#!/usr/bin/env node

/**
 * PreToolUse hook: valida Conventional Commits per git commit -m "..."
 * Adapted for Claude Code 2.1+ stdin JSON format.
 * Original source: rohitg00/awesome-claude-code-toolkit/hooks/scripts/commit-guard.js
 */

let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
  let data;
  try {
    data = JSON.parse(input || '{}');
  } catch {
    process.exit(0); // invalid input, don't block
  }

  const toolName = data.tool_name || '';
  const command = data.tool_input?.command || '';

  if (toolName !== 'Bash') process.exit(0);
  if (!/(^|[;&|]\s*)git\s+commit/.test(command)) process.exit(0);

  // ADR-0011 Addendum 2026-05-17 (policy-C, Eduardo-decided): ban GitHub
  // "Co-Authored-By:" trailer. ALWAYS-ON -- applies even to HEREDOC commits
  // (orthogonal to the Conventional format-check which stays HEREDOC-skip).
  // Cheap content check on full command, zero false-positive.
  if (/co-authored-by\s*:/i.test(command)) {
    process.stderr.write(
      'commit-guard.js block -- ADR-0011 policy-C: "Co-Authored-By:" trailer VIETATO.\n' +
      '  Usa trailer metadata: "Coding-Agent: <agent-id>" + "Trace-Id: <uuidv7>".\n' +
      '  Rif: codemasterdd docs/adr/0011 Addendum 2026-05-17.\n'
    );
    process.exit(2);
  }

  // ADR-0011-C (warn-only, policy-C): nudge missing required trailers. This is a
  // PreToolUse hook -- it fires ONLY for Claude Code agent commits, so it never
  // nags human hand-commits (those go through the global commit-msg hook, which
  // deliberately does NOT require the trailers). Non-blocking: warn + continue.
  if (!/coding-agent\s*:/i.test(command) || !/trace-id\s*:/i.test(command)) {
    process.stderr.write(
      'commit-guard.js note (ADR-0011-C, warn-only): agent commit missing ' +
      '"Coding-Agent:" and/or "Trace-Id:" trailer -- add them (not blocked).\n'
    );
  }

  // Check for HEREDOC opener
  if (command.includes('<<')) {
    console.error('HEREDOC detected, skipping validation');
    process.exit(0);
  }

  // Match -m "msg" or -m 'msg' only. HEREDOC multi-line skipped (controlled case).
  const msgMatch = command.match(/-m\s+["']([^"']+)["']/);
  if (!msgMatch) process.exit(0);

  const msg = msgMatch[1];
  const errors = [];

  /**
   * Regex per il pattern dei messaggi di commit Conventional Commits.
   */
  const conventionalPattern = /^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(\(.+\))?!?:\s.+/;
  if (!conventionalPattern.test(msg)) {
    errors.push('Message does not follow conventional commit format: type(scope): description');
  }

  /**
   * Verifica che la lunghezza del messaggio non superi i 72 caratteri.
   */
  if (msg.length > 72) {
    errors.push(`Subject line is ${msg.length} chars (max 72)`);
  }

  /**
   * Verifica che il messaggio non termini con un punto.
   */
  if (msg.endsWith('.')) {
    errors.push('Subject line should not end with a period');
  }

  /**
   * Verifica che la prima lettera del descrittore sia in minuscolo.
   */
  const firstChar = msg.replace(/^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(\(.+\))?!?:\s/, '')[0];
  if (firstChar && firstChar === firstChar.toUpperCase()) {
    errors.push('Description should start with lowercase letter');
  }

  if (errors.length > 0) {
    process.stderr.write(
      'commit-guard.js block — commit message issues:\n' +
      errors.map(e => '  - ' + e).join('\n') + '\n'
    );
    process.exit(2);
  }

  process.exit(0);
});
