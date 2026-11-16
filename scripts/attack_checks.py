"""Run attacks against real guards; assert nonzero and the intended diagnostic."""

import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]


def reject(args, expected, **kwargs):
    result = subprocess.run(args, text=True, capture_output=True, **kwargs)
    print("+", " ".join(map(str, args)))
    print(result.stdout, result.stderr)
    assert result.returncode != 0, "attack unexpectedly accepted"
    assert expected in result.stdout + result.stderr, "failure was not the intended rejection"
    return {"exit_code": result.returncode, "expected_diagnostic": expected}


def main():
    results = {}
    with tempfile.TemporaryDirectory() as temp:
        root = pathlib.Path(temp)
        lock = (ROOT / "requirements-runtime.lock").read_text()
        import re

        lock = re.sub(r"sha256:[a-f0-9]{64}", "sha256:" + "0" * 64, lock)
        (root / "tampered.lock").write_text(lock)
        results["tampered-dependency"] = reject(
            [
                sys.executable,
                "-m",
                "pip",
                "download",
                "--no-cache-dir",
                "--require-hashes",
                "-r",
                str(root / "tampered.lock"),
                "-d",
                str(root / "download"),
            ],
            "DO NOT MATCH THE HASHES",
        )
        shutil.copytree(ROOT / "dist", root / "dist")
        wheel = next((root / "dist").glob("*.whl"))
        with wheel.open("ab") as stream:
            stream.write(b"tampered")
        results["stale-artifact"] = reject(
            [sys.executable, str(ROOT / "scripts/artifact_guard.py"), str(root / "dist")],
            "SHA256 mismatch",
        )
        env = dict(os.environ, GITHUB_REF="refs/tags/v0.9.5")
        results["tag-mismatch"] = reject(
            [sys.executable, str(ROOT / "scripts/expected_version.py")],
            "tag/version mismatch",
            cwd=ROOT,
            env=env,
        )
    print("ATTACK_RESULTS=" + json.dumps(results, sort_keys=True))


if __name__ == "__main__":
    main()
