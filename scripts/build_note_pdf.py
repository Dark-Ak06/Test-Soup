"""Render docs/NOTE.md as the two-page A4 submission note."""

from __future__ import annotations

import html
import pathlib

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/NOTE.md"
OUTPUT = ROOT / "docs/NOTE.pdf"


def markdown_blocks(text: str):
    """Yield headings, paragraphs and tables from the deliberately small note format."""
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("|"):
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
                if not all(set(cell) <= {"-", ":"} for cell in cells):
                    rows.append(cells)
                index += 1
            yield "table", rows
            continue
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            yield "heading", (level, line[level:].strip())
            index += 1
            continue
        paragraph = [line]
        index += 1
        while index < len(lines):
            following = lines[index].strip()
            if not following or following.startswith("#") or following.startswith("|"):
                break
            paragraph.append(following)
            index += 1
        yield "paragraph", " ".join(paragraph)


def escaped(text: str) -> str:
    return html.escape(text, quote=False)


def footer(canvas, document):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#4f7390"))
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(18 * mm, 11 * mm, "HOSTED EVIDENCE / TESTPYPI RELEASE EXERCISE")
    canvas.drawRightString(A4[0] - 18 * mm, 11 * mm, str(document.page))
    canvas.restoreState()


def build():
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=23,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#17344b"),
        spaceAfter=7 * mm,
    )
    section = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=13.5,
        textColor=colors.HexColor("#17344b"),
        spaceBefore=2.6 * mm,
        spaceAfter=1.5 * mm,
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.6,
        leading=10.7,
        textColor=colors.HexColor("#111111"),
        spaceAfter=2.3 * mm,
    )
    meta = ParagraphStyle(
        "Meta",
        parent=body,
        fontSize=7.5,
        leading=9,
        textColor=colors.HexColor("#4f7390"),
        spaceAfter=5 * mm,
    )
    cell = ParagraphStyle("Cell", parent=body, fontSize=7.2, leading=8.6, spaceAfter=0)
    header = ParagraphStyle(
        "CellHeader", parent=cell, fontName="Helvetica-Bold", textColor=colors.HexColor("#17344b")
    )

    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=17 * mm,
        bottomMargin=19 * mm,
        title="Release confidence starts after installation",
        author="Soup exercise contributor",
    )
    story = []
    first_heading = True
    for kind, value in markdown_blocks(SOURCE.read_text(encoding="utf-8")):
        if kind == "heading":
            level, heading = value
            if level == 1:
                continue
            if heading == "Boundaries, cost and next steps":
                story.extend([PageBreak(), Paragraph(escaped(heading), title)])
            elif first_heading:
                story.append(Paragraph(escaped(heading), title))
                first_heading = False
            else:
                story.append(Paragraph(escaped(heading), section))
        elif kind == "paragraph":
            paragraph_style = meta if value.startswith("SOUP / DEVOPS EXERCISE") else body
            story.append(Paragraph(escaped(value), paragraph_style))
        elif kind == "table":
            table_data = []
            for row_index, row in enumerate(value):
                row_style = header if row_index == 0 else cell
                table_data.append([Paragraph(escaped(item), row_style) for item in row])
            table = Table(table_data, colWidths=[34 * mm, 51 * mm, 74 * mm], repeatRows=1)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5eef4")),
                        ("LINEBELOW", (0, 0), (-1, -1), 0.35, colors.HexColor("#aec3d2")),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 4),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                        ("TOPPADDING", (0, 0), (-1, -1), 4),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ]
                )
            )
            story.extend([table, Spacer(1, 2.2 * mm)])

    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
