"""Generate a table from measured local experiments and verified gh run metadata."""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "evidence/local-results.json").read_text())
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
        f"| {row['name']} | exit {naive} | exit {robust} | {row.get('diagnostic', '')} | NOT RUN |"
    )
lines += [
    "",
    "Full timestamped command output: `evidence/local-*.txt`.",
    "",
    "## Cloud evidence",
    "",
    "NOT RUN: GitHub CLI reported no authenticated hosts. No run URLs are invented.",
    "TestPyPI publication and post-publish installation: NOT DONE.",
    "macOS and hosted Windows/Linux matrix: NOT RUN.",
    "Fork PR / second-account demonstration: NOT DONE.",
    "",
    "To collect real cloud runs after authenticated execution:",
    "",
    "```sh",
    "gh run list --repo Dark-Ak06/Test-Soup --json "
    "databaseId,url,conclusion,headSha,workflowName,event,headBranch",
    "gh run view <id> --repo Dark-Ak06/Test-Soup",
    "```",
    "",
    "Each cloud row must link its exact commit and failing job log before claiming success.",
]
(ROOT / "docs").mkdir(exist_ok=True)
(ROOT / "docs/EVIDENCE.md").write_text("\n".join(lines) + "\n")
