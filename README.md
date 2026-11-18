# Soup release engineering exercise

Status: hosted defect demonstrations and TestPyPI release. See docs/EVIDENCE.md for exact run links, diagnostics and limitations.
Only authorized remote: https://github.com/Dark-Ak06/Test-Soup.git

Python CLI prints a greeting from packaged data. Supported Python: >=3.10.

```sh
python -m venv .venv
# Activate the venv using your platform's activation command.
python -m pip install -e '.[dev]'
python -m pytest
python scripts/build_release.py
python scripts/verify_install.py dist --expected 0.9.4
docker build --build-arg EXPECTED_VERSION=0.9.4 -t soupdemo-wheel-check .
```

`verify_install.py` creates a disposable venv OUTSIDE the checkout, installs the wheel
without development tools, then tests the installed console command and resources.
`--docker 3.10` uses a non-root Linux container with no source checkout mounted.
The checked-in `Dockerfile` provides the same non-root, no-cache wheel verification
against an explicit Python 3.10.22 base image; build the distributions first.

Read docs/SETUP.md for cloud setup, docs/EXPERIMENTS.md for defect branches,
docs/SUPPLY_CHAIN.md for attack demonstrations, and docs/GPU_CI.md for design only.
The exercise deliberately includes bad branches; do not publish them to real PyPI.
No email is sent by these tools.
