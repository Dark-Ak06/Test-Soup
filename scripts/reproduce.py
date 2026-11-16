"""Run real local defect experiments. Requires Docker and build tools in this Python."""

import argparse
import datetime
import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFECTS = {
    "01-python310": "No module named 'tomllib'",
    "02-windows": "No module named 'pwd'",
    "03-data": "FileNotFoundError",
    "04-dependency": "No module named 'packaging'",
    "05-entrypoint": "cannot import name 'mian'",
    "06-version": "runtime version mismatch",
}


def mutate(root, name):
    cli = root / "src/soupdemo/cli.py"
    project = root / "pyproject.toml"
    if name == "01-python310":
        cli.write_text(
            cli.read_text().replace(
                "import click", "import click\nimport tomllib\n\ntomllib.loads('')"
            )
        )
    elif name == "02-windows":
        cli.write_text(
            cli.read_text().replace("import click", "import click\nimport pwd\n\npwd.getpwuid(0)")
        )
    elif name == "03-data":
        project.write_text(
            project.read_text().replace('soupdemo = ["data/*.txt"]', "soupdemo = []")
        )
    elif name == "04-dependency":
        cli.write_text(
            cli.read_text().replace(
                "import click",
                "import click\nfrom packaging.version import Version\n\nVersion('1.0')",
            )
        )
    elif name == "05-entrypoint":
        project.write_text(project.read_text().replace("soupdemo.cli:main", "soupdemo.cli:mian"))
    elif name == "06-version":
        (root / "src/soupdemo/__init__.py").write_text('__version__ = "0.9.2"\n')
    else:
        raise ValueError(name)


def logged(name, command, cwd=ROOT, env=None):
    evidence = ROOT / "evidence" / f"local-{name}.txt"
    with evidence.open("w", encoding="utf-8") as stream:
        stream.write(datetime.datetime.now(datetime.timezone.utc).isoformat() + "\n")
        stream.write("COMMAND: " + json.dumps(list(map(str, command))) + "\n")
        stream.flush()
        result = subprocess.run(command, cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT)
        stream.write(f"\nEXIT_CODE={result.returncode}\n")
    print(f"{name}: exit={result.returncode} log={evidence.name}", flush=True)
    return result.returncode, evidence.read_text(encoding="utf-8", errors="replace")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", help="Empty/new scratch directory outside the repository")
    args = parser.parse_args()
    work = pathlib.Path(args.workspace).resolve()
    work.mkdir(parents=True, exist_ok=False)
    dockerfile = work / "Dockerfile"
    dockerfile.write_text(
        "FROM python:3.12-slim\n"
        "RUN python -m pip install pytest==8.4.2 build==1.3.0 twine==6.2.0 "
        "ruff==0.14.5 click==8.1.8 setuptools==80.9.0 wheel==0.45.1\n"
    )
    code, _ = logged("naive-image", ["docker", "build", "-t", "soup-naive-local", str(work)])
    assert code == 0
    results = []
    for name in ["fixed", *DEFECTS, "incident"]:
        case = work / name
        shutil.copytree(
            ROOT,
            case,
            ignore=shutil.ignore_patterns(
                ".git",
                "evidence",
                "dist",
                "build",
                "*.egg-info",
                "__pycache__",
                ".ruff_cache",
                ".pytest_cache",
            ),
        )
        for defect in DEFECTS if name == "incident" else [name] if name in DEFECTS else []:
            mutate(case, defect)
        if name == "incident":
            project = case / "pyproject.toml"
            project.write_text(
                project.read_text().replace('version = "0.9.4"', 'version = "0.9.3"')
            )
        command = [
            "docker",
            "run",
            "--rm",
            "--mount",
            f"type=bind,source={case},target=/case",
            "-w",
            "/case",
            "soup-naive-local",
            "sh",
            "-ec",
            "python -m pip install -e '.[dev]' && python -m pytest -q && python -m build",
        ]
        naive, _ = logged(name + "-naive", command)
        assert naive == 0, f"naive failed unexpectedly for {name}"
        expected = "0.9.3" if name == "incident" else "0.9.4"
        command = [
            sys.executable,
            str(ROOT / "scripts/verify_install.py"),
            str(case / "dist"),
            "--expected",
            expected,
        ]
        if name in ["01-python310", "incident", "fixed"]:
            command += ["--docker", "3.10"]
        code, output = logged(name + "-installed", command)
        diagnostic = DEFECTS.get(
            name, "No module named 'packaging'" if name == "incident" else "PASS installed package"
        )
        assert (code == 0) == (name == "fixed"), f"unexpected verify result for {name}"
        assert diagnostic in output, f"wrong failure for {name}: {diagnostic}"
        results.append(
            {"name": name, "naive_exit": naive, "verify_exit": code, "diagnostic": diagnostic}
        )
        (ROOT / "evidence/local-results.json").write_text(json.dumps(results, indent=2) + "\n")
    print("PASS: all intended local outcomes observed")


if __name__ == "__main__":
    main()
