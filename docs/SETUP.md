# Remaining account setup and cloud execution

No GitHub host is authenticated in gh. No TestPyPI publishing identity is
configured by this project. Passwords, 2FA codes and access tokens do not belong
in chat, source files or logs. These identity steps require the account owner.

1. Run `gh auth login --hostname github.com --web` in your terminal. Select HTTPS,
   open the browser flow and sign into the intended account. Check `gh auth status`.
2. Open https://github.com/Dark-Ak06/Test-Soup and confirm ownership/write access.
   Public visibility is recommended so reviewers can see the code and standard
   hosted runner usage is free. Visibility has NOT been changed here.
3. Repository Settings > Environments > New environment > `testpypi`.
   Deployment branches and tags > Selected branches and tags > add TAG pattern `v*`.
   Do not add a branch pattern. If the account cannot configure it, an owner must.
4. Sign into TestPyPI, complete account verification and 2FA. Open account
   Publishing and add a pending GitHub publisher with project `soup-release-demo-darkak06-20261116`,
   owner `Dark-Ak06`, repository `Test-Soup`, workflow `naive.yml`, environment
   `testpypi`. Name returned HTTP 404 at preflight; this does not reserve it.
5. After the first incident publication creates the project, use project Manage
   > Publishing to add `release.yml` with the same repository/environment.
   Sequential registration avoids assuming two pending publishers for one new name.
6. Push main and the six bug branches; inspect actual naive and robust runs.
   Publish incident tag v0.9.3 only after its naive run is verified. Record the
   expected failures from exact 0.9.3 installs using scripts/post_publish.py.
7. Create v0.9.4 on the final main commit and push it. Inspect all checks, OIDC
   publication and post-publish smoke. Do not claim completion until they succeed.
8. Use the gh run list/view commands in EVIDENCE.md to collect real URLs and logs.
   Preserve failed runs. Correct faults in new commits and use a new version if
   a version was already uploaded. Do not force-push or move published tags.

This repository currently has local branches but no publication tags. The full
remote execution is NOT DONE. The release jobs target TestPyPI only.

Sources, retrieved 2026-11-16:
- https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/
- https://docs.pypi.org/trusted-publishers/adding-a-publisher/
- https://docs.github.com/en/actions/reference/runners/github-hosted-runners
