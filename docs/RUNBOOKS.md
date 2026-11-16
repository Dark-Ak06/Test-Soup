# Short operational runbooks

## Leaked secret: first ten minutes
- Stop new publication/deployment. Identify which credential and systems it authorizes.
- Revoke or rotate at the issuer immediately; deleting a log is not revocation.
- Preserve restricted incident evidence and timestamps without copying the secret.
- Restrict exposed logs/artifacts, review access and use, notify the responsible owner.
- Check published packages, sessions and related credentials; restore only after containment.

## Bad release
- Pause automation; identify exact affected version, hashes and user impact.
- Yank the bad version with a clear reason; publish a corrected higher version.
- Advise affected users to upgrade or pin a known-good version; retest installed artifacts.
- Do not treat deleting files as a rollback. Existing downloads cannot be recalled,
  and pinned installs may still select a yanked version.
- The exercise assumes non-deletable releases. PyPI's real behavior is more nuanced:
  deletion exists, but is not safe replacement/reuse of an uploaded distribution.
  Use yank/supersede in this exercise, not deletion.

## Compromised dependency
- Halt release; identify exact compromised versions/hashes and exposure window.
- Replace with reviewed known-good version, regenerate locks in a clean environment.
- Inspect whether dependency code ran during builds; rotate exposed credentials if needed.
- Rebuild from trusted inputs, test, publish a new version and notify affected users.

Source, retrieved 2026-11-16:
https://docs.pypi.org/project-management/yanking/
