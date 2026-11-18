# Current status: 2026-11-18

Six independent defect branches have real hosted naive-green and intended
robust-red runs. Exact errors and shared fixed-green baseline are in EVIDENCE.md.
The initial baseline passed 33 jobs. The main candidate also passed hosted CI.
Both naive.yml and release.yml Trusted Publishers are configured in TestPyPI;
environment testpypi restricts deployments to tags v*.
Incident 0.9.3 was published via OIDC and its installed failures reproduced.
Fixed 0.9.4 release: SUCCESS, including OIDC publication and Linux 3.10/3.13 plus Windows 3.13 post-publish installs. Full metadata: evidence/cloud/44142793862.json.

NOT DONE / NOT VERIFIED: fork PR with a second account, GPU execution (design
only), fully hashed build/dev transitive toolchain, semantic escape demonstration,
and sending the submission email. The personal reflection and AI disclosure were
completed and reviewed on 2026-11-18.
`gitleaks` was not installed in the final local audit environment, so the retained
9-commit history scan is historical and is not claimed as proof for the current
29-commit history. A fresh all-history scan remains required before submission.
No failed run, branch or published tag was deleted or rewritten. Duplicate queued
manual dispatches were cancelled when identical push runs appeared; records retained.
Earlier local-stage notes/status are historical. This file and EVIDENCE supersede them.
