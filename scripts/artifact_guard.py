"""Reject stale/tampered distributions before install or publish."""

import hashlib
import json
import pathlib
import sys


def verify(folder):
    root = pathlib.Path(folder)
    manifest = json.loads((root / "SHA256.json").read_text())
    actual_names = {
        p.name for p in root.iterdir() if p.suffix == ".whl" or p.name.endswith(".tar.gz")
    }
    assert actual_names == set(manifest), "artifact set mismatch"
    for name, expected in manifest.items():
        actual = hashlib.sha256((root / name).read_bytes()).hexdigest()
        assert actual == expected, f"SHA256 mismatch: {name}"
    print("PASS artifact digests", json.dumps(manifest, sort_keys=True))


if __name__ == "__main__":
    verify(sys.argv[1])
