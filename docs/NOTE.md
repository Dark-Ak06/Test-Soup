# Release engineering note

## Release confidence starts after installation

SOUP / DEVOPS EXERCISE / 16 NOVEMBER 2026

## Verdict: not ready for unattended production publication

The local release candidate passes the implemented checks, but the hosted matrix, OIDC publication and TestPyPI smoke tests have not run. GitHub CLI has no authenticated account. This is a tested local implementation with an explicit remote-execution gap, not a completed cloud release.

## 1. Incident and measured defects

A Linux/Python 3.12 editable-install pipeline ran pytest and built distributions successfully for all six independent defects and their combined 0.9.3 incident. Real clean installations failed as follows; the fixed 0.9.4 package passed on local Windows/Python 3.12 and non-root Linux/Python 3.10.

| Defect | Why naive checks pass | Installed failure / guard |
|---|---|---|
| 3.11-only import | Tests use Python 3.12 | 3.10: missing tomllib |
| POSIX-only import | Tests use Linux | Windows: missing pwd |
| Missing packaged data | Editable tree has data | FileNotFoundError |
| Undeclared dependency | Dev tools bring packaging | Missing packaging |
| Entry-point typo | Tests call function directly | Cannot import mian |
| Version drift | Version never asserted | Runtime version mismatch |

The combined incident first fails on the undeclared dependency. An initial harness assertion predicted the wrong first failure; its error is recorded, and the existing output was reinterpreted without rerunning to hide it. Independent defects establish each failure separately. See docs/EVIDENCE.md and timestamped evidence/local-*.txt.

## 2. Pipeline design

The robust workflow specifies lint and 15 OS/Python combinations: Linux, Windows and Intel macOS across 3.10-3.14. A fresh job builds the release once, checks metadata and wheel contents, rebuilds from sdist to compare payloads, and records SHA256. Verification consumes the same run-specific artifact.

Linux verification runs non-root Docker with only distributions, a runtime lock and independent test probe. Windows/macOS use fresh virtual environments outside the checkout. No dev tools enter these environments. The probe invokes the installed command, reads data and compares runtime/metadata/expected versions. Publication depends on every CI job, verifies hashes again and uses TestPyPI OIDC only. Post-publish checks detect damage after upload; they cannot prevent it.

## Boundaries, cost and next steps

## 3. Silent failures and remaining exposure

Three real local attacks were rejected with the intended errors: tampered dependency hashes by pip, modified wheel bytes by the SHA256 guard, and v0.9.5 against 0.9.4 metadata by the version guard. Exact runtime pins/hashes, unique artifact names and full Action commit pins reduce substitution and release mistakes at low runtime cost. Hashes prove identity, not trustworthiness.

The implementation does not prove semantic correctness beyond its small tests, safety of approved dependencies, or integrity of a compromised build runner. Dev/build transitive dependencies are not fully locked; Docker tags and runner images can drift. Python metadata permits newer versions beyond the tested 3.14 ceiling. ARM, macOS execution and fork-PR isolation are unverified. Repository/environment protections still need account setup. No claim of a demonstrated semantic escape or full hermetic build is made.

## 4. GPU CI: designed, not run

Compare managed GitHub Linux GPU at $3.12/hour (eligible Team/Enterprise organizations), disposable Runpod A40 at listed $0.59/hour, and AWS G4dn at an UNVERIFIED planning estimate of $0.526/hour. Prices and limitations are sourced in docs/GPU_CI.md (retrieved 2026-11-16). No GPU was rented.

Base model: (4 release + 30 nightly runs) x 20 minutes / 60 x 1.10 failure allowance = 12.47 GPU-hours/month. Compute: $38.90 GitHub, $7.36 Runpod, $6.56 AWS estimate; add a $10 planning reserve. Low/high compute ranges are $6.55-$98.80, $1.24-$18.68 and $1.10-$16.66 respectively. Taxes, subscription, storage and transfer are excluded from compute.

Gate allocation on green CPU jobs; detect missing GPU in about 60 seconds; set job timeout, one retry, allocation TTL and independent idle watchdog. Avoid nightly allocation without new commits. Budget alerts require an allocation cutoff to enforce a cap. Use ephemeral runners; never reuse a privileged GPU runner for untrusted fork code.

## 5. What to fix first

First complete GitHub authentication and TestPyPI account/environment/Trusted Publisher setup, then collect real naive-green, intended robust-red and fixed-green hosted runs and exact-version installs. Next lock the build toolchain and enforce reviewed release/tag creation. Only after those results should unattended TestPyPI release be trusted within the tested boundary. Real PyPI publishing is neither configured nor authorized by this implementation.

## AI disclosure and personal reflection

AI generated code, workflows, documentation and this note and executed local checks. Suggestions were checked with real command output, official documentation and API-derived pins; mistakes and corrections are listed in docs/AI_USAGE.md. No independent candidate verification is claimed.

[Candidate to write: what surprised me, what I verified myself, and what still concerns me. This paragraph is intentionally not invented by AI.]
