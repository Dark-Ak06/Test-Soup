Subject: DevOps internship exercise - release pipeline and evidence
To: team@trysoup.dev

DRAFT - NOT SENT

Hello Soup team,

Repository: https://github.com/Dark-Ak06/Test-Soup
Evidence and six naive-green / robust-red pairs:
https://github.com/Dark-Ak06/Test-Soup/blob/main/docs/EVIDENCE.md
Fixed release: https://github.com/Dark-Ak06/Test-Soup/actions/runs/44142793862
Test package: https://test.pypi.org/project/soup-release-demo-darkak06-20261116/

The project demonstrates six packaging/platform defects, a clean installed-artifact
matrix, three supply-chain attack rejections, OIDC publication and GPU CI design.
The two-page note is docs/NOTE.pdf. AI assistance is disclosed in docs/AI_USAGE.md.
Remaining limits are recorded in docs/STATUS.md.

I was surprised by how easily a naive Ubuntu/Python 3.12 CI using an editable install stayed completely green across six different user-facing defects, including failures specific to Windows and Python 3.10, and by how many small issues only appeared in real GitHub Actions runs, including harness mistakes and cache-related assumptions. I am still concerned that even a green robust pipeline cannot make a compromised but approved dependency safe because hashes prove identity rather than trustworthiness, that the transitive build/test toolchain is not fully hash-locked, and that the publish job with id-token: write still checks out and executes repository code.
