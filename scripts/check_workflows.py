"""Download an integrity-pinned actionlint release, then validate workflow syntax."""

import hashlib
import pathlib
import subprocess
import tarfile
import tempfile
import urllib.request

URL = "https://github.com/rhysd/actionlint/releases/download/v1.7.12/actionlint_1.7.12_linux_amd64.tar.gz"
SHA256 = "8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8"

with tempfile.TemporaryDirectory() as temp:
    root = pathlib.Path(temp)
    data = urllib.request.urlopen(URL, timeout=60).read()
    assert hashlib.sha256(data).hexdigest() == SHA256, "actionlint digest mismatch"
    archive = root / "actionlint.tar.gz"
    archive.write_bytes(data)
    with tarfile.open(archive) as tar:
        member = tar.getmember("actionlint")
        binary = root / "actionlint"
        binary.write_bytes(tar.extractfile(member).read())
        binary.chmod(0o755)
    subprocess.run([str(binary), "-color"], check=True)
