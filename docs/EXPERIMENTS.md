# Experiments and interpretation

The baseline is 0.9.4. Each `bug/01-*` through `bug/06-*` starts from the same
working baseline and changes one defect. `incident/0.9.3` combines all six.
The combined incident fails first on the undeclared packaging import; that is NOT proof of
the remaining defects. Independent branches provide that proof.

| Defect | Why naive CI misses it | User failure | Robust control |
|---|---|---|---|
| B1 `tomllib` import | Only Python 3.12 | Import fails on 3.10 | Python 3.10 installed probe |
| B2 `pwd` import | Only Linux | Windows startup fails | Windows installed probe |
| B3 package-data removed | Editable source contains file | Installed resource is missing | Manifest and installed data read |
| B4 undeclared `packaging` import | Build tools bring packaging | Clean runtime cannot import it | Venv with runtime dependencies only |
| B5 `mian` entry point | Tests call main directly | Console script cannot start | Invoke installed executable |
| B6 runtime version 0.9.2 | Tests never ask version | CLI lies about version | Metadata/runtime/tag agreement |

Reproduction requires Docker, Python >=3.10, build and test tools. From the repo:

```sh
python scripts/reproduce.py /absolute/path/to/new-scratch-directory
python scripts/make_evidence.py
```

Use a NEW scratch directory. Command logs are stored under evidence/.
The naive sequence really runs in Linux Python 3.12: editable install, pytest,
then build. The installed probe uses a fresh external Windows venv for B2-B6,
and a non-root Linux Python 3.10 container for B1 and the incident.
The parent harness asserts an actual nonzero exit AND the expected diagnostic.
Its own success means the experiment behaved as predicted, not that the broken
package passed. These are local experiments, not hosted Actions runs.

Naive publication is a separate job to confine OIDC permission to publishing.
This intentionally deviates from the pasted specification's single-job naive
workflow while retaining its inadequate test/build checks. The PDF does not
require a single job. Only tag v0.9.3 can invoke naive publication.

Cloud sequence after setup: push baseline/main and defect branches, inspect
every run, push incident tag v0.9.3, reproduce from TestPyPI, then push v0.9.4.
Do not replay failed jobs to disguise a failure: preserve results and fix forward.
The fixed baseline is shared across defects; one complete successful release
run can be referenced as the shared fix only after its exact commit is verified.
