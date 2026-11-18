# Cloud setup and verified release state

## Current verified state

The public repository is https://github.com/Dark-Ak06/Test-Soup. Hosted CI,
incident publication and the fixed release have been completed; exact run links,
commit SHAs and diagnostics are retained in `docs/EVIDENCE.md`.

- Tag `v0.9.3` preserves the intentionally broken incident. The `naive.yml`
  Trusted Publisher uploaded it to TestPyPI through OIDC in
  https://github.com/Dark-Ak06/Test-Soup/actions/runs/44132055388.
- Tag `v0.9.4` is the fixed release. The `release.yml` Trusted Publisher uploaded
  it through OIDC, and all 37 release, matrix and post-publish jobs passed in
  https://github.com/Dark-Ak06/Test-Soup/actions/runs/44142793862.
- The fixed 33-job baseline is
  https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130869957. The current
  `main` commit also passed robust CI in
  https://github.com/Dark-Ak06/Test-Soup/actions/runs/44143511509.
- The GitHub `testpypi` environment is restricted to version tags. Both
  `naive.yml` and `release.yml` are registered as TestPyPI Trusted Publishers
  for project `soup-release-demo-darkak06-20261116` and environment `testpypi`.
- No long-lived TestPyPI API token is used. Only the two publication jobs have
  `id-token: write`; all other jobs retain read-only repository permissions.

The published exercise project is:
https://test.pypi.org/project/soup-release-demo-darkak06-20261116/

## Owner checks for a future release

1. Authenticate to GitHub as the intended repository owner and verify write
   access. Authentication, passwords, 2FA codes and recovery codes must never
   be stored in source, chat transcripts, workflow logs or artifacts.
2. Confirm repository environment `testpypi` still allows only the intended
   version-tag pattern and that both Trusted Publisher registrations still name
   the exact repository, workflow file and environment.
3. Review the candidate commit on protected `main`, run robust CI, and create an
   immutable version tag whose value matches project and runtime metadata.
4. Inspect every release job. Do not rerun or delete a failure to manufacture a
   green record; fix forward with a new commit and version when publication may
   already have occurred.
5. Record the run URL, exact commit SHA, artifact hashes and post-publish install
   results in `docs/EVIDENCE.md`.

Real PyPI publication is not configured or authorized by this exercise. Before
adding it, protect release-tag creation, hash-lock the transitive build/test
toolchain, and prevent the OIDC publication job from executing repository code.

Sources, retrieved 2026-11-16:

- https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/
- https://docs.pypi.org/trusted-publishers/adding-a-publisher/
- https://docs.github.com/en/actions/reference/runners/github-hosted-runners
