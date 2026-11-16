# Status and submission gap

## DONE LOCALLY
- Minimal CLI, six independently reproduced bugs plus combined incident.
- Naive Linux/Python 3.12 succeeds for all variants; clean installs reject all defects.
- Fixed artifact passes local Windows/Python 3.12 and Linux/Python 3.10 Docker.
- Clean build, strict twine check, expected wheel manifest, sdist round-trip.
- Three real supply-chain attack rejections with exact diagnostics.
- Workflows prepared with SHA pins, matrix, OIDC and artifact reuse.
- Two-page note and GPU design, runbooks, setup instructions, email draft.

## NOT DONE / NOT VERIFIED
- No push, remote branch or tag creation; gh is unauthenticated.
- No hosted Actions run, including the 15-combination matrix; no run URLs.
- No TestPyPI account configuration, OIDC publish or post-publish installation.
- No fork-PR demo, semantic-escape demo, GPU execution or full hermetic toolchain.
- Personal reflection not written on behalf of the candidate; email not sent.
- Python 3.15+ is allowed by package metadata but is outside the specified CI matrix.
- GPU AWS rate is an UNVERIFIED ESTIMATE, not a confirmed quote.
- Local defect branches preserve the exact experimental mutations; B1/B2/B4 also
  have lint-style issues. A future cloud lint failure must NOT count as proof of
  the runtime defect. Read the installed verification/matrix job's actual error.

## UNINTENDED FAILURES
PDF/tool-bootstrap errors, initial lint issues and a mistaken combined-incident
diagnostic prediction are disclosed in AI_USAGE.md. The incident actually failed
on missing packaging; its original log remains intact. No cloud failures exist
because no cloud runs were started. Missing authentication is a blocker, not success.

The project is not ready to submit as a fully completed hosted exercise.

## FINAL AUDIT LIMITATIONS
All workflow syntax/lint checks passed on main, as did Python compilation and
artifact digest verification. Executable source/workflows contain zero forbidden
failure-masking patterns. All 24 third-party Action uses are full-SHA pinned.
The HTTP audit returned 200 for five cited endpoints and 403 for five others.
Those 403 pages were readable through the web tool, but the strict claim that
every URL returns 200 is NOT satisfied. See evidence/url-audit.json.
Poppler emitted missing fallback-font warnings; both rendered PDF pages were
visually inspected and contain no missing glyphs, clipping or overlaps.
