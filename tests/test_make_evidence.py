import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_default_run_preserves_hosted_evidence():
    evidence = ROOT / "docs/EVIDENCE.md"
    before = evidence.read_bytes()
    assert b"https://github.com/" in before
    assert b"/actions/runs/" in before

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/make_evidence.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "PRESERVED hosted evidence" in result.stdout
    assert evidence.read_bytes() == before


def test_force_reset_overwrites_hosted_evidence_in_isolation(tmp_path):
    target = tmp_path / "EVIDENCE.md"
    mock_hosted_content = (
        "# Evidence\nhttps://github.com/Dark-Ak06/Test-Soup/actions/runs/12345678901\n"
    )
    target.write_text(mock_hosted_content, encoding="utf-8")

    # Run without --force-reset: should preserve
    result_preserved = subprocess.run(
        [sys.executable, str(ROOT / "scripts/make_evidence.py"), "--target", str(target)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "PRESERVED hosted evidence" in result_preserved.stdout
    assert target.read_text(encoding="utf-8") == mock_hosted_content

    # Run with --force-reset: should overwrite with local placeholders
    result_reset = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/make_evidence.py"),
            "--force-reset",
            "--target",
            str(target),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "WROTE local-only evidence" in result_reset.stdout
    new_content = target.read_text(encoding="utf-8")
    assert "NOT RUN" in new_content
    assert "NOT DONE" in new_content
    assert "12345678901" not in new_content
