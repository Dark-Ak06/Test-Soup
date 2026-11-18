# syntax=docker/dockerfile:1.7
FROM python:3.10.22-slim-bookworm

ARG EXPECTED_VERSION=0.9.4
ENV HOME=/home/verifier \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN useradd --create-home --uid 10001 verifier \
    && mkdir -p /input /work \
    && chown verifier:verifier /input /work

COPY --chown=verifier:verifier requirements-runtime.lock /input/requirements-runtime.lock
COPY --chown=verifier:verifier scripts/installed_probe.py /input/installed_probe.py
COPY --chown=verifier:verifier dist/*.whl /input/

USER verifier
WORKDIR /work
RUN python -m venv /work/env \
    && /work/env/bin/python -m pip install --no-cache-dir --require-hashes \
        -r /input/requirements-runtime.lock \
    && /work/env/bin/python -m pip install --no-cache-dir --no-deps /input/*.whl \
    && /work/env/bin/python -m pip check \
    && /work/env/bin/python /input/installed_probe.py \
        "${EXPECTED_VERSION}" /work/env/bin/soupdemo

CMD ["/work/env/bin/soupdemo", "--version"]
