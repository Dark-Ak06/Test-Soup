# Supply-chain controls

## Implemented and attacked locally

| Risk | Control | Attack evidence | Prevention/detection and residual risk |
|---|---|---|---|
| Swapped runtime dependency | Exact runtime lock with SHA256; require-hashes install | `local-attacks.txt`: replace approved digest with zeros; pip refuses download | Prevents unapproved bytes entering runtime verification; an already-malicious approved wheel remains possible |
| Stale/tampered artifact | Unique run-id+commit artifact; exact file set and SHA256 before test/publish | Append bytes to wheel; SHA256 guard rejects | Detects substituted bytes relative to manifest; compromised build job can replace both |
| Version/tag disagreement | Project/runtime/wheel agreement and tag guard | v0.9.5 environment against 0.9.4 metadata is rejected | Prevents accidental mislabel; a malicious maintainer can change all values |

Run `python scripts/attack_checks.py` after `python scripts/build_release.py`.
The script prints the failing subprocess output, requires nonzero exits and
checks the intended diagnostics. It does not suppress a pipeline failure.

These are common low-cost protections against operational mistakes and dependency
replacement. Hashing two tiny runtime wheels and archives costs little. Their
value is bounded: hashes establish identity, not safety. Action SHAs were resolved
from GitHub's API, recorded in evidence/pins.json, and pinned in all workflows.

## Additional boundaries

Top-level contents:read; checkout does not persist credentials. Only publication
jobs have id-token:write, use testpypi environment and TestPyPI OIDC, and run on
tags. No pull_request_target workflow exists. PR code gets no publishing job.
Fork-PR credential isolation was NOT demonstrated with a second account.
Environment tag rules are setup instructions, NOT a configured remote control.

Runtime verification uses locked dependencies, `--no-cache-dir`, and installs the
package without dependency resolution before running pip check. General users do
not inherit this lock from wheel metadata. Build/dev transitive dependencies are
still resolved online; the environment is NOT fully hermetic. No Actions or pip
cache is restored in clean artifact verification, but resolver behavior, runner
images and Docker base-image changes remain open risks.

Next priorities: fully hashed build/test locks per supported interpreter,
trusted tag creation/protected main, artifact attestations, dependency scanning,
and a scheduled cold resolver without cache. These are NOT claimed implemented.

Post-publication installation first downloads only the exact project wheel from
TestPyPI using --no-deps, then uses PyPI for approved runtime dependencies.
It avoids --extra-index-url: pip does not treat that as a safe fallback priority,
and competing names can cause dependency confusion. Post-publication checks
DETECT a broken release; they cannot undo its publication.

Source, retrieved 2026-11-16:
https://pip.pypa.io/en/stable/cli/pip_install/
