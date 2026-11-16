# Evidence

Local results are NOT GitHub Actions runs.

| Variant | Naive local | Installed local | Intended diagnostic | Actions |
|---|---|---|---|---|
| fixed | exit 0 | exit 0 | PASS installed package | NOT RUN |
| 01-python310 | exit 0 | exit 1 | No module named 'tomllib' | NOT RUN |
| 02-windows | exit 0 | exit 1 | No module named 'pwd' | NOT RUN |
| 03-data | exit 0 | exit 1 | FileNotFoundError | NOT RUN |
| 04-dependency | exit 0 | exit 1 | No module named 'packaging' | NOT RUN |
| 05-entrypoint | exit 0 | exit 1 | cannot import name 'mian' | NOT RUN |
| 06-version | exit 0 | exit 1 | runtime version mismatch | NOT RUN |
| incident | exit 0 | exit 1 | No module named 'packaging' | NOT RUN |

Full timestamped command output: `evidence/local-*.txt`.

## Cloud evidence

NOT RUN: GitHub CLI reported no authenticated hosts. No run URLs are invented.
TestPyPI publication and post-publish installation: NOT DONE.
macOS and hosted Windows/Linux matrix: NOT RUN.
Fork PR / second-account demonstration: NOT DONE.

To collect real cloud runs after authenticated execution:

```sh
gh run list --repo Dark-Ak06/Test-Soup --json databaseId,url,conclusion,headSha,workflowName,event,headBranch
gh run view <id> --repo Dark-Ak06/Test-Soup
```

Each cloud row must link its exact commit and failing job log before claiming success.
