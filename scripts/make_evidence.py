"""Generate local evidence without erasing verified hosted run links."""

import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def contains_hosted_run_urls(path: pathlib.Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return "https://github.com/" in text and "/actions/runs/" in text


def local_only_document(root: pathlib.Path) -> str:
    data = json.loads((root / "evidence/local-results.json").read_text(encoding="utf-8"))
    lines = [
        "# Evidence",
        "",
        "Local results are NOT GitHub Actions runs.",
        "",
        "| Variant | Naive local | Installed local | Intended diagnostic | Actions |",
        "|---|---|---|---|---|",
    ]
    for row in data:
        naive = row.get("naive_exit")
        robust = row.get("verify_exit")
        lines.append(
            f"| {row['name']} | exit {naive} | exit {robust} | "
            f"{row.get('diagnostic', '')} | NOT RUN |"
        )
    lines += [
        "",
        "Full timestamped command output: `evidence/local-*.txt`.",
        "",
        "## Cloud evidence",
        "",
        "NOT RUN: hosted evidence has not been collected for this reset document.",
        "TestPyPI publication and post-publish installation: NOT DONE.",
        "macOS and hosted Windows/Linux matrix: NOT RUN.",
        "Fork PR / second-account demonstration: NOT DONE.",
        "",
        "Collect and verify real run URLs before replacing these local-only statements.",
    ]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force-reset",
        action="store_true",
        help="replace docs/EVIDENCE.md with local-only placeholders even if hosted URLs exist",
    )
    parser.add_argument(
        "--target",
        type=pathlib.Path,
        default=ROOT / "docs/EVIDENCE.md",
        help="target evidence file to update (defaults to docs/EVIDENCE.md)",
    )
    args = parser.parse_args(argv)
    target = args.target
    if contains_hosted_run_urls(target) and not args.force_reset:
        print(f"PRESERVED hosted evidence: {target}")
        return 0
    target.parent.mkdir(exist_ok=True)
    target.write_text(local_only_document(ROOT), encoding="utf-8")
    print(f"WROTE local-only evidence: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
