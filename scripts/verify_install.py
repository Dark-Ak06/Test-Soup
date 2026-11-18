"""Test distributions in an isolated venv or non-root Linux container."""

import argparse
import os
import pathlib
import shutil
import subprocess
import tempfile
import venv


def run(args, **kwargs):
    print("+", " ".join(map(str, args)), flush=True)
    subprocess.run(list(map(str, args)), check=True, **kwargs)


def verify(dist, expected, docker=None):
    wheels = list(pathlib.Path(dist).resolve().glob("*.whl"))
    assert len(wheels) == 1, "expected exactly one wheel"
    with tempfile.TemporaryDirectory(prefix="soup-installed-") as temp:
        root = pathlib.Path(temp)
        shutil.copy(wheels[0], root)
        shutil.copy(pathlib.Path(__file__).resolve().parents[1] / "requirements-runtime.lock", root)
        shutil.copy(pathlib.Path(__file__).with_name("installed_probe.py"), root)
        if docker:
            # POSIX mkdtemp defaults to 0700; the container UID needs read/traverse access.
            root.chmod(0o755)
            for item in root.iterdir():
                item.chmod(0o644)
            # Only wheel and independent probe enter the container, never the repository.
            script = (
                "python -m venv /tmp/env && "
                "/tmp/env/bin/python -m pip install --no-cache-dir --require-hashes "
                "-r /input/requirements-runtime.lock && "
                "/tmp/env/bin/python -m pip install --no-cache-dir --no-deps /input/*.whl && "
                "/tmp/env/bin/python -m pip check && "
                "/tmp/env/bin/python /input/installed_probe.py "
                + expected
                + " /tmp/env/bin/soupdemo"
            )
            run(
                [
                    "docker",
                    "run",
                    "--rm",
                    "--user",
                    "65534:65534",
                    "-e",
                    "HOME=/tmp",
                    "--mount",
                    f"type=bind,source={root},target=/input,readonly",
                    f"python:{docker}-slim",
                    "sh",
                    "-ec",
                    script,
                ]
            )
        else:
            venv.EnvBuilder(with_pip=True).create(root / "env")
            bindir = root / "env" / ("Scripts" if os.name == "nt" else "bin")
            python = bindir / ("python.exe" if os.name == "nt" else "python")
            command = bindir / ("soupdemo.exe" if os.name == "nt" else "soupdemo")
            env = dict(os.environ)
            env.pop("PYTHONPATH", None)
            run(
                [
                    python,
                    "-m",
                    "pip",
                    "install",
                    "--no-cache-dir",
                    "--require-hashes",
                    "-r",
                    root / "requirements-runtime.lock",
                ],
                cwd=root,
                env=env,
            )
            run(
                [
                    python,
                    "-m",
                    "pip",
                    "install",
                    "--no-cache-dir",
                    "--no-deps",
                    root / wheels[0].name,
                ],
                cwd=root,
                env=env,
            )
            run([python, "-m", "pip", "check"], cwd=root, env=env)
            run([python, root / "installed_probe.py", expected, command], cwd=root, env=env)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dist")
    parser.add_argument("--expected", required=True)
    parser.add_argument("--docker", choices=["3.10", "3.11", "3.12", "3.13", "3.14"])
    args = parser.parse_args()
    verify(args.dist, args.expected, args.docker)
