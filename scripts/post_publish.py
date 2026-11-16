"""Detect post-publication damage. This cannot prevent a bad publication."""

import argparse
import pathlib
import subprocess
import sys
import tempfile
import time

from verify_install import verify


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("version")
    parser.add_argument("--docker")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as temp:
        for attempt in range(1, 7):
            command = [
                sys.executable,
                "-m",
                "pip",
                "download",
                "--no-deps",
                "--only-binary=:all:",
                "--no-cache-dir",
                "--index-url",
                "https://test.pypi.org/simple/",
                "--dest",
                temp,
                f"soup-release-demo-darkak06-20261116=={args.version}",
            ]
            result = subprocess.run(command, check=False)
            if result.returncode == 0:
                break
            if attempt == 6:
                raise SystemExit(result.returncode)
            print(f"Index fetch failed: attempt {attempt}/6; waiting 20 seconds", flush=True)
            time.sleep(20)
        assert len(list(pathlib.Path(temp).glob("*.whl"))) == 1
        # Dependencies resolve solely from PyPI; package solely from TestPyPI.
        verify(temp, args.version, args.docker)


if __name__ == "__main__":
    main()
