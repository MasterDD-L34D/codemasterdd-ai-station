// load-problems.js — carica problems.json per promptfoo.config.yaml
// Ogni problem diventa un test case con assertion python-subprocess.
//
// Docs: https://www.promptfoo.dev/docs/configuration/test-cases#test-file-formats

const fs = require('fs');
const path = require('path');

const PROBLEMS_FILE = process.env.PROMPTFOO_PROBLEMS || 'problems.json';
const raw = fs.readFileSync(path.join(__dirname, PROBLEMS_FILE), 'utf8');
const problems = JSON.parse(raw);

module.exports = problems.map((p) => ({
  description: `${p.id}: solve ${p.prompt.slice(0, 60).replace(/\n/g, ' ')}...`,
  vars: {
    problem: p.prompt,
  },
  assert: [
    {
      // Custom python-subprocess assertion: compile + run tests in sandbox
      // LLM output (function definition) + test suite → must exit 0
      type: 'python',
      value: buildAssertionScript(p),
    },
  ],
  metadata: {
    problem_id: p.id,
    num_tests: p.tests.length,
  },
}));

function buildAssertionScript(problem) {
  // Python script ricevuto da promptfoo:
  //   output = LLM response (function code)
  //   context = promptfoo metadata
  // Deve returnare True se tutti i test passano, altrimenti False
  const testsEscaped = problem.tests.map((t) => t.replace(/'/g, "\\'")).join('\n    ');
  return `
import subprocess
import tempfile
import os
import re

code = output.strip()

# Strip markdown fences if LLM didn't follow instructions
code = re.sub(r'^\\s*\`\`\`(?:python|py)?\\s*\\n?', '', code, flags=re.MULTILINE)
code = re.sub(r'\\n?\\s*\`\`\`\\s*$', '', code, flags=re.MULTILINE)
# Strip thinking mode tags (DeepSeek-R1)
code = re.sub(r'<think>.*?</think>', '', code, flags=re.DOTALL)
code = re.sub(r'<thinking>.*?</thinking>', '', code, flags=re.DOTALL)
code = code.strip()

# Build sandbox script
script = code + '\\n\\n'
tests = '''
    ${testsEscaped}
'''
script += tests + "\\nprint('ALL_PASS')\\n"

with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(script)
    tmp = f.name

try:
    result = subprocess.run(['python', tmp], capture_output=True, text=True, timeout=10)
    passed = result.returncode == 0 and 'ALL_PASS' in result.stdout
    if passed:
        return True
    # Richiesto da promptfoo: return dict for rich diagnostics
    reason = 'pass' if passed else (
        'assert_fail' if 'AssertionError' in result.stderr else
        'syntax_error' if 'SyntaxError' in result.stderr or 'IndentationError' in result.stderr else
        'name_error' if 'NameError' in result.stderr else
        'type_error' if 'TypeError' in result.stderr else
        'runtime_error'
    )
    return {
        'pass': False,
        'score': 0.0,
        'reason': f'{reason}: {result.stderr.strip()[:300]}',
    }
finally:
    try:
        os.unlink(tmp)
    except OSError:
        pass
`;
}
