# Verified cloud evidence

| Defect | Naive green | Robust red | Intended error and job | Fixed green |
|---|---|---|---|---|
| B1 | [green](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130396834) | [red](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130396871) | test (ubuntu-latest, 3.10): `No module named 'tomllib'` | [shared fixed baseline](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130869957) |
| B2 | [green](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130419269) | [red](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130419599) | test (windows-latest, 3.14): `No module named 'pwd'` | [shared fixed baseline](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130869957) |
| B3 | [green](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130444249) | [red](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130444283) | build: `wheel manifest mismatch` | [shared fixed baseline](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130869957) |
| B4 | [green](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130469552) | [red](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130469634) | verify-artifact (ubuntu-latest, 3.14): `No module named 'packaging'` | [shared fixed baseline](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130869957) |
| B5 | [green](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130488668) | [red](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130488701) | verify-artifact (ubuntu-latest, 3.11): `cannot import name 'mian'` | [shared fixed baseline](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130869957) |
| B6 | [green](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130512240) | [red](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130512506) | build: `version mismatch: 0.9.4, 0.9.2, 0.9.4` | [shared fixed baseline](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44130869957) |

Each listed run was rechecked with gh run view; full API metadata and failed logs are in evidence/cloud/. The fixed baseline is shared by all six independent defect branches.

## Published incident

[v0.9.3 OIDC publication](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44132055388) succeeded. Exact published version installations failed on local Windows and non-root Linux/Python 3.10; see evidence/local-published-093-*.txt. The exercise preserves the bad release and supersedes it; no release was deleted.

## Fixed release

[v0.9.4 release](https://github.com/Dark-Ak06/Test-Soup/actions/runs/44142793862): SUCCESS: all release jobs, OIDC publication and three post-publish installs passed. Post-publish checks use Linux 3.10/3.13 and Windows 3.13.

## Retained limitations

Fork PR/second account and GPU execution were not demonstrated. GPU is a design only. Build/dev transitive dependencies are not fully hashed. Personal reflection requires candidate review. Original local-stage PDF and status documents are superseded by this cloud evidence. Redundant queued manual dispatches were cancelled when push runs appeared; records were retained.
