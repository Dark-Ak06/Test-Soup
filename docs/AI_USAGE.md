# AI usage and mistakes

Session started 2026-11-16T18:29:12.664121+00:00. I used AI tools to generate
boilerplate for the small package, first drafts of workflows and verification
scripts, documentation structure, and wording for the release note. The source
task explicitly permits AI assistance and requires disclosure.

I accepted the matrix strategy, installed-wheel probe, exact runtime dependency
hashes, full Action commit pins, TestPyPI OIDC design, supply-chain attack checks
and GPU cost model after reviewing their concrete behavior. I manually configured
and checked GitHub/TestPyPI OIDC, inspected the real red and green Actions runs and
their commit SHAs, reviewed the security boundaries, and corrected discrepancies
in the documentation and `make_evidence.py`. AI output was treated as a draft:
commands, hosted results and final claims were checked against actual output or
official documentation before acceptance.

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
| Initial remote bootstrap | GitHub was not yet authenticated in the first local session | Authentication check failed | Deferred cloud claims, then authenticated, configured OIDC and verified real hosted runs before documenting completion |

Local experiment logs contain real command output, including expected failures.
Do not confuse designed attack failures with implementation mistakes. Other
unintended failures are retained in `evidence/` and reported in `STATUS.md`.
The personal reflection in the final note was reviewed and written in the first
person after the technical results were verified.

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

2026-11-18: performed a final repository audit, replaced stale setup claims,
protected hosted run URLs from the local evidence generator, added a regression
test, and updated the personal reflection and reproducible PDF build. The final
manual review covered the OIDC permissions, artifact path, run links, remaining
supply-chain limitations and submission documents.
