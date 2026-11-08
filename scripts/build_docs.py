"""Typeset the two English research notes from Markdown."""

from pathlib import Path
import html
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent
PAGE_WIDTH, PAGE_HEIGHT = A4
WIDTH = PAGE_WIDTH - 108
styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        "BodyTextEnglish",
        fontName="Times-Roman",
        fontSize=11,
        leading=15,
        spaceAfter=8,
        alignment=TA_LEFT,
        allowWidows=0,
        allowOrphans=0,
    )
)
styles.add(
    ParagraphStyle(
        "NoteTitle", fontName="Times-Bold", fontSize=23, leading=27, spaceAfter=14
    )
)
styles.add(
    ParagraphStyle(
        "NoteHeading",
        fontName="Times-Bold",
        fontSize=13,
        leading=17,
        spaceBefore=13,
        spaceAfter=7,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        "Cell", fontName="Times-Roman", fontSize=8.7, leading=11, spaceAfter=0
    )
)
styles.add(
    ParagraphStyle(
        "SmallNote",
        fontName="Times-Italic",
        fontSize=9,
        leading=12,
        spaceAfter=13,
        textColor=colors.HexColor("#555555"),
    )
)


def inline(text):
    value = html.escape(text)
    value = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" color="#244d67">\1</a>', value
    )
    value = re.sub(r"`([^`]+)`", r'<font name="Courier" size="8.5">\1</font>', value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)
    return re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", value)


def table(lines):
    rows = [[c.strip() for c in line.strip().strip("|").split("|")] for line in lines]
    rows = [row for row in rows if not all(re.fullmatch(r"[:\- ]+", c) for c in row)]
    count = len(rows[0])
    first = WIDTH * (0.49 if count <= 3 else 0.39)
    widths = [first] + [(WIDTH - first) / (count - 1)] * (count - 1)
    cells = [[Paragraph(inline(c), styles["Cell"]) for c in row] for row in rows]
    out = Table(cells, colWidths=widths, repeatRows=1, hAlign="LEFT")
    out.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef1f2")),
                ("LINEABOVE", (0, 0), (-1, 0), 0.6, colors.HexColor("#555555")),
                ("LINEBELOW", (0, 0), (-1, 0), 0.4, colors.HexColor("#777777")),
                ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.HexColor("#777777")),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return [KeepTogether([out, Spacer(1, 11)])]


def contents(source):
    lines = source.read_text(encoding="utf-8").splitlines()
    story = []
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("# "):
            story.append(Paragraph(inline(line[2:]), styles["NoteTitle"]))
            story.append(
                Paragraph(
                    "The ABC of Communism<br/>Research and replication notes | November 2026",
                    styles["SmallNote"],
                )
            )
            story.append(
                HRFlowable(
                    width="100%", thickness=0.6, color=colors.HexColor("#777777")
                )
            )
            story.append(Spacer(1, 13))
        elif line.startswith("## "):
            story.append(Paragraph(inline(line[3:]), styles["NoteHeading"]))
        elif line.startswith("|"):
            block = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                block.append(lines[index])
                index += 1
            story.extend(table(block))
            continue
        elif line.startswith("- "):
            story.append(
                Paragraph("&#8226; " + inline(line[2:]), styles["BodyTextEnglish"])
            )
        else:
            block = [line]
            while (
                index + 1 < len(lines)
                and lines[index + 1].strip()
                and not lines[index + 1].startswith(("#", "|", "- "))
            ):
                index += 1
                block.append(lines[index].strip())
            story.append(Paragraph(inline(" ".join(block)), styles["BodyTextEnglish"]))
        index += 1
    return story


def page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#cccccc"))
    canvas.line(54, 42, PAGE_WIDTH - 54, 42)
    canvas.setFont("Times-Roman", 8.5)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawString(54, 29, "The ABC of Communism")
    canvas.drawRightString(PAGE_WIDTH - 54, 29, str(doc.page))
    canvas.restoreState()


def build(source, name):
    target = ROOT / "docs" / name
    doc = SimpleDocTemplate(
        str(target),
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=49,
        bottomMargin=56,
        title=source.read_text(encoding="utf-8").splitlines()[0][2:],
        author="Mark Kreshchuk",
    )
    doc.build(contents(source), onFirstPage=page, onLaterPages=page)
    print(target)


if __name__ == "__main__":
    build(ROOT / "docs/METHODS.md", "Data_and_methods.pdf")
    build(ROOT / "docs/SUPPLEMENTARY_EVIDENCE.md", "Supplementary_evidence.pdf")
