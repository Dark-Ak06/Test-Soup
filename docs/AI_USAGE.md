# AI usage and mistakes

Session recorded 2026-11-16T18:29:12.664121+00:00. AI generated package, workflows, experiment harness,
documentation and note. User requested autonomous completion. Claims are limited
to tool observations; no claim is made that the user independently verified them.
The source PDF explicitly permits AI assistance and requires disclosure.

| Stage | Mistake / limitation | Detection | Correction |
|---|---|---|---|
| PDF extraction | Assumed pymupdf installed in default Python | ModuleNotFoundError | Used bundled pypdf |
| PDF text output | Default Windows encoding could not print a mathematical symbol | UnicodeEncodeError | Explicit UTF-8 stdout |
| Tool bootstrap | Assumed requests in bundled Python | ModuleNotFoundError | Used standard-library urllib |
| Tool bootstrap | Initially installed latest dev packages | Review of reproducibility | Reinstalled API-verified exact versions |
| Generated lock | Literal plus signs leaked into continuation lines | Inspected generated lock | Removed plus signs before execution |
| Lint | Initial long lines and unused imports | Ruff diagnostics | Fixed/formatted code; rules unchanged |
| Workflow validation | actionlint run before git init could not locate project | Tool error | Initialized local git then reran |
| Matrix | macos-latest is ARM; 3.10 native availability differs | Official runner docs and Python manifest | Selected macos-15-intel and recorded per-platform availability |
| Evidence collection | Initial Python availability extraction only examined newest release platform set | Incomplete Windows/macOS result | Resolved newest matching release separately per OS/architecture |
| Remote work | gh has no authenticated hosts | gh auth status exit 1 | Did not push or invent hosted evidence; supplied setup guide |

Local experiment logs contain real command output, including expected failures.
Do not confuse designed attack failures with implementation mistakes. Other
unintended failures, if any, are retained in evidence/ and reported in STATUS.md.
The candidate's personal reflection remains blank because AI cannot truthfully
claim the candidate's own observations, emotions or independent work.

2026-11-16: combined-incident harness incorrectly predicted tomllib would fail
first. Its assertion failed after the real install failed on packaging, because
mutation order placed that import first. Preserved the original log, corrected
the expected diagnostic and parsed existing output; no rerun to manufacture
success. Six independent defect results were unaffected. A PowerShell inline
correction then failed with SyntaxError due to quoting; replaced it with a file.

2026-11-16: review found POSIX temporary directories default to mode 0700,
which would prevent a non-root Linux container reading its mounted inputs.
Set explicit 0755 directory / 0644 input-file permissions before Docker runs.
Windows local success alone would not expose this POSIX host permission issue.

2026-11-17: resumed authenticated cloud work. Fixed incidental import ordering on bug branches without removing intentional defects. Enabled explicit dispatch. Push triggers now also created runs; cancelled only redundant queued/pending dispatches and retained cancellation evidence. Earlier assumption that the lack of runs was solely due to multi-branch push was not established. TestPyPI account page still reports 2FA not enabled despite recovery codes being present.

2026-11-17: completed both owner-confirmed Trusted Publisher registrations,
published incident 0.9.3, reproduced exact-version installation failures, and
triggered fixed v0.9.4. Collected and verified all six intended hosted defect errors.
No claim is made that the candidate personally executed or reviewed these steps.
