"""Standard-library-only tests, deliberately independent of pytest/dev dependencies."""

import importlib.metadata
import pathlib
import subprocess
import sys

import soupdemo
from soupdemo.cli import greeting


def main():
    expected, command = sys.argv[1:]
    version = importlib.metadata.version("soup-release-demo-darkak06-20261116")
    assert version == expected, f"wheel version {version} != expected {expected}"
    assert soupdemo.__version__ == expected, "runtime version mismatch"
    assert greeting("Ada") == "Hello, Ada!"
    result = subprocess.run([command, "--name", "Ada"], text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "Hello, Ada!"
    result = subprocess.run([command, "--version"], text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip().endswith(" " + expected), result.stdout
    location = pathlib.Path(soupdemo.__file__).resolve()
    assert "site-packages" in str(location), location
    print(f"PASS installed package: {location}; version={version}")


if __name__ == "__main__":
    main()
