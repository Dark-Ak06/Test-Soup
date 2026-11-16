"""Clean build, inspect archive contents, round-trip sdist and validate versions."""

import email
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]


def run(*args):
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def inspect(wheel):
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        package_files = sorted(n for n in names if n.startswith("soupdemo/"))
        expected = (ROOT / "expected-manifest.txt").read_text().splitlines()
        assert package_files == expected, f"wheel manifest mismatch: {package_files}"
        metadata = email.message_from_bytes(
            archive.read(next(n for n in names if n.endswith("/METADATA")))
        )
        version = metadata["Version"]
        project = re.search(r'^version = "([^"]+)"', (ROOT / "pyproject.toml").read_text(), re.M)[1]
        runtime = re.search(
            r'__version__ = "([^"]+)"', archive.read("soupdemo/__init__.py").decode()
        )[1]
        tag = os.environ.get("GITHUB_REF", "")
        if tag.startswith("refs/tags/"):
            assert tag == "refs/tags/v" + project, f"tag/version mismatch: {tag} != v{project}"
        assert project == runtime == version, f"version mismatch: {project}, {runtime}, {version}"
        return {n: archive.read(n) for n in package_files}


def main():
    for path in [ROOT / "dist", ROOT / "build", *ROOT.glob("src/*.egg-info")]:
        if path.exists():
            shutil.rmtree(path)
    run("-m", "build")
    distributions = sorted((ROOT / "dist").iterdir())
    run("-m", "twine", "check", "--strict", *map(str, distributions))
    wheel = next(p for p in distributions if p.suffix == ".whl")
    original = inspect(wheel)
    sdist = next(p for p in distributions if p.name.endswith(".tar.gz"))
    with tempfile.TemporaryDirectory() as temp:
        run("-m", "pip", "wheel", "--no-deps", "--wheel-dir", temp, str(sdist))
        rebuilt = inspect(next(pathlib.Path(temp).glob("*.whl")))
        assert original == rebuilt, "sdist round-trip changed package payload"
    manifest = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in distributions}
    (ROOT / "dist/SHA256.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("PASS build and version guard", json.dumps(manifest))


if __name__ == "__main__":
    main()
