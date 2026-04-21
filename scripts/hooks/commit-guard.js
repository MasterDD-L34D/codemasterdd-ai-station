#!/usr/bin/env node
// PreToolUse hook: valida Conventional Commits per git commit -m "..."
// Adapted for Claude Code 2.1+ stdin JSON format.
// Original source: rohitg00/awesome-claude-code-toolkit/hooks/scripts/commit-guard.js

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
  if (!command.includes('git commit')) process.exit(0);

  // Match -m "msg" or -m 'msg' only. HEREDOC multi-line skipped (controlled case).
  const msgMatch = command.match(/-m\s+["']([^"']+)["']/);
  if (!msgMatch) process.exit(0);

  const msg = msgMatch[1];
  const errors = [];

  const conventionalPattern = /^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(\(.+\))?!?:\s.+/;
  if (!conventionalPattern.test(msg)) {
    errors.push('Message does not follow conventional commit format: type(scope): description');
  }

  if (msg.length > 72) {
    errors.push(`Subject line is ${msg.length} chars (max 72)`);
  }

  if (msg.endsWith('.')) {
    errors.push('Subject line should not end with a period');
  }

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
