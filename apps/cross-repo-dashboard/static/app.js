// Cross-repo Dashboard v0.2 — client-side actions

function openCoordModal() {
  document.getElementById('coord-modal').style.display = 'flex';
  document.getElementById('coord-notes').focus();
  document.getElementById('coord-result').textContent = '';
}
function closeCoordModal() {
  document.getElementById('coord-modal').style.display = 'none';
}
async function submitCoord() {
  const notes = document.getElementById('coord-notes').value.trim();
  if (!notes) { alert('Notes required'); return; }
  const r = document.getElementById('coord-result');
  r.textContent = 'Logging...';
  try {
    const res = await fetch('/api/coord-event', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({notes}),
    });
    const data = await res.json();
    if (data.ok) {
      r.textContent = '✓ Logged. ' + (data.stdout_tail || '');
      setTimeout(closeCoordModal, 1200);
    } else {
      r.textContent = '✗ Error: ' + (data.error || data.stderr_tail || 'unknown');
    }
  } catch (e) {
    r.textContent = '✗ Network error: ' + e;
  }
}

function openPrModal() {
  document.getElementById('pr-modal').style.display = 'flex';
  document.getElementById('pr-files').focus();
  document.getElementById('pr-result').textContent = '';
}
function closePrModal() {
  document.getElementById('pr-modal').style.display = 'none';
}
async function submitPr() {
  const repo_target = document.getElementById('pr-target').value;
  const type = document.getElementById('pr-type').value;
  const preview_files = document.getElementById('pr-files').value.trim();
  const summary = document.getElementById('pr-summary').value.trim();
  if (!preview_files || !summary) { alert('Files + summary required'); return; }
  const r = document.getElementById('pr-result');
  r.textContent = 'Running dry-run...';
  try {
    const res = await fetch('/api/draft-pr', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({repo_target, type, preview_files, summary}),
    });
    const data = await res.json();
    if (data.ok) {
      r.textContent = data.draft;
    } else {
      r.textContent = '✗ Error: ' + (data.error || data.stderr_tail || 'unknown');
    }
  } catch (e) {
    r.textContent = '✗ Network error: ' + e;
  }
}

async function openVSCode(path) {
  try {
    const res = await fetch('/api/open-vscode?path=' + encodeURIComponent(path));
    const data = await res.json();
    if (!data.ok) alert('VS Code launch failed: ' + (data.error || 'unknown'));
  } catch (e) {
    alert('Network error: ' + e);
  }
}

// Auto-refresh every 5 minutes (matches cache TTL)
setTimeout(() => location.reload(), 5 * 60 * 1000);

// Close modals on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeCoordModal();
    closePrModal();
  }
});
