# Observation Methods

Pick method at the BOUNDARY where you think bug lives.

| Method | When |
|--------|------|
| `print` / `console.log` / `tracing::debug!` | Trace paths, inspect data at decision points |
| `curl` / fetch direct | Hit endpoint, see raw response vs assumption |
| Browser DevTools | Rendered DOM, CSS computed, React/Vue state |
| Network tab / SSE stream | What server actually sent |
| Log files on disk | What was written vs should be |
| Screenshot / recording | What user actually sees |

Rules:
1. One boundary at a time, minimal logs
2. Reproduce reliably before concluding
3. Save exact command that reproduced — goes to handoff Working Commands
4. Same method for verify-after-fix as for diagnosis
