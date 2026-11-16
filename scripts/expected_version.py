import os
import pathlib
import re

ref = os.environ.get("GITHUB_REF", "")
version = re.search(r'^version = "([^"]+)"', pathlib.Path("pyproject.toml").read_text(), re.M)[1]
if ref.startswith("refs/tags/"):
    assert ref == "refs/tags/v" + version, "tag/version mismatch"
print("EXPECTED_VERSION=" + version)
