"""Build the website, publication data, and PDF CV from the same records."""
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader, select_autoescape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
TYPES = {
    "journal": "Journal", "conf_intl": "Conference", "poster_intl": "Poster / Demo",
    "conf_dom": "Domestic conference", "poster_dom": "Domestic poster / Demo", "other": "Other",
}


def load(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def safe_url(value, local=False):
    if not value:
        return ""
    parsed = urlparse(value)
    if parsed.scheme in {"https", "http"} and parsed.netloc:
        return value
    if local and not parsed.scheme and not parsed.netloc and value.startswith("files/") and ".." not in Path(value).parts:
        if not (ROOT / value).is_file():
            raise ValueError(f"Missing linked file: {value}")
        return value
    raise ValueError(f"Unsupported publication link: {value}")


def infer_type(venue):
    text = venue.casefold()
    if "poster" in text or "demo" in text:
        return "poster_intl"
    if "transactions" in text or "journal" in text:
        return "journal"
    if "conference" in text or "symposium" in text or "proceedings" in text:
        return "conf_intl"
    return "other"


def publications(snapshot, overrides, additional):
    result = []
    for article in snapshot["articles"]:
        paper = dict(article)
        extra = overrides.get(paper["id"], {})
        # Scholar owns the title, publication year, venue, abbreviated authors, and citation count.
        for key in ("type", "pdf", "publisher_url", "full_authors", "featured", "venue_label"):
            if key in extra:
                paper[key] = extra[key]
        paper["source"] = "Google Scholar"
        paper.setdefault("type", infer_type(paper["venue"]))
        result.append(paper)
    scholar_ids = {p["id"] for p in result}
    for item in additional:
        # An explicit scholar_id prevents duplicates when an additional item becomes indexed.
        if item.get("scholar_id") in scholar_ids:
            continue
        result.append(dict(item))
    for p in result:
        p["type_label"] = TYPES.get(p["type"], "Other")
        p["display_authors"] = p.get("full_authors") or p["authors"]
        p["venue_label"] = p.get("venue_label") or p["type_label"]
        p["pdf"] = safe_url(p.get("pdf", ""), local=True)
        p["publisher_url"] = safe_url(p.get("publisher_url", ""))
        p["scholar_url"] = safe_url(p.get("scholar_url", ""))
    return sorted(result, key=lambda p: (-(p.get("year") or 0), p["title"].casefold()))


def pdf_cv(profile, papers, sync_date, destination):
    pdfmetrics.registerFont(TTFont("CVSans", ROOT / "assets/fonts/DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("CVSans-Bold", ROOT / "assets/fonts/DejaVuSans-Bold.ttf"))
    pdfmetrics.registerFontFamily("CVSans", normal="CVSans", bold="CVSans-Bold", italic="CVSans", boldItalic="CVSans-Bold")
    pdfmetrics.registerFont(TTFont("Korean", ROOT / "assets/fonts/NanumGothic-Regular.ttf"))
    pdfmetrics.registerFontFamily("Korean", normal="Korean", bold="Korean", italic="Korean", boldItalic="Korean")
    stylesheet = getSampleStyleSheet()
    ink = colors.HexColor("#202032")
    accent = colors.HexColor("#5842c3")
    stylesheet.add(ParagraphStyle(name="CVName", fontName="CVSans-Bold", fontSize=27, leading=32, textColor=ink, spaceAfter=7))
    stylesheet.add(ParagraphStyle(name="CVSection", fontName="CVSans-Bold", fontSize=12, leading=17, textColor=accent, spaceBefore=16, spaceAfter=8, keepWithNext=True))
    stylesheet.add(ParagraphStyle(name="CVBody", fontName="CVSans", fontSize=9.4, leading=14, textColor=ink, spaceAfter=4))
    stylesheet.add(ParagraphStyle(name="CVSmall", fontName="CVSans", fontSize=8.4, leading=12, textColor=colors.HexColor("#666477"), spaceAfter=5))
    def clean(value):
        # Embed Korean glyphs so the CV renders without fonts installed on the reader's device.
        value = html.escape(str(value).replace("–", "-").replace("—", "-").replace("…", "..."))
        return re.sub(r"([\u3000-\u318f\uac00-\ud7af]+)", r'<font name="Korean">\1</font>', value)
    def para(value, style="CVBody"):
        return Paragraph(value, stylesheet[style])
    story = [para(clean(profile["name"]), "CVName"),
             para(clean(profile["role"] + " | " + profile["affiliation"])),
             para(f'{clean(profile["email"])} · <link href="{profile["site_url"]}" color="#5842c3">{clean(profile["site_url"])}</link>', "CVSmall"),
             para(f'<link href="{html.escape(profile["scholar_url"], quote=True)}" color="#5842c3">Google Scholar</link> · Publication data checked {sync_date}', "CVSmall"),
             para("Research interests", "CVSection"),
             para(clean(" · ".join(item["name"] for item in profile["research"]))) ]
    def section(title):
        story.append(para(title, "CVSection"))
    section("Education")
    for e in profile["education"]:
        story.append(KeepTogether([para(f'<b>{clean(e["institution"])}</b>'), para(clean(e["degree"])), para(clean(e["period"]), "CVSmall")]))
    section("Research experience")
    for e in profile["experience"]:
        story.append(KeepTogether([para(f'<b>{clean(e["role"])} · {clean(e["institution"])}</b>'), para(clean(e["period"]), "CVSmall"), para(clean(e["description"]))]))
    section("Awards")
    for a in profile["awards"]:
        story.append(para(f'<b>{a["year"]} · {clean(a["title"])}</b><br/>{clean(a["venue"])}'))
    section("Publications indexed in Google Scholar")
    story.append(para("Titles and years follow the Google Scholar profile. Complete author names and existing PDF links are retained where available.", "CVSmall"))
    indexed = [p for p in papers if p["source"] == "Google Scholar"]
    additional = [p for p in papers if p["source"] != "Google Scholar"]
    def pub(p, index):
        label = f'{index}. {clean(p["title"])}'
        link = p["publisher_url"] or p["scholar_url"]
        title = f'<b>{label}</b>'
        if link:
            title = f'<link href="{html.escape(link,quote=True)}" color="#202032">{title}</link>'
        return KeepTogether([para(title), para(clean(p["display_authors"]), "CVSmall"),
                             para(clean(f'{p["venue"]} · {p.get("year") or "Year not listed"}'), "CVSmall"), Spacer(1, 5)])
    for i, p in enumerate(indexed, 1):
        story.append(pub(p, i))
    if additional:
        section("Additional presentations and posters")
        story.append(para("Preserved from the existing website; not part of the current Scholar publication list.", "CVSmall"))
        for i, p in enumerate(additional, 1):
            story.append(pub(p, i))
    section("Funded projects")
    for p in profile["projects"]:
        story.append(KeepTogether([para(f'<b>{clean(p["name"])}</b>'), para(clean(p["period"]), "CVSmall"), para(clean(p["description"])), Spacer(1, 4)]))
    section("Technical skills")
    for name, skills in profile["skills"].items():
        story.append(para(f'<b>{clean(name)}</b>: {clean(", ".join(skills))}'))
    section("Languages")
    story.append(para(clean(" · ".join(profile["languages"]))))
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#e4e1ed"))
        canvas.line(19*mm, 15*mm, 191*mm, 15*mm)
        canvas.setFont("CVSans", 8)
        canvas.setFillColor(colors.HexColor("#6b687c"))
        canvas.drawString(19*mm, 10*mm, "Dong-Geun Kim | Curriculum Vitae")
        canvas.drawRightString(191*mm, 10*mm, str(doc.page))
        canvas.restoreState()
    destination.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(destination), pagesize=A4, rightMargin=19*mm, leftMargin=19*mm,
                                 topMargin=18*mm, bottomMargin=22*mm,
                                 title="Dong-Geun Kim - Curriculum Vitae", author=profile["name"])
    document.build(story, onFirstPage=footer, onLaterPages=footer)


def main():
    profile, snapshot = load("profile.json"), load("scholar.json")
    papers = publications(snapshot, load("publication-overrides.json"), load("additional-publications.json"))
    date = snapshot["last_successful_sync"][:10]
    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=select_autoescape(["html"]))
    indexed = [p for p in papers if p["source"] == "Google Scholar"]
    context = dict(profile=profile, papers=papers, indexed=indexed,
                   additional=[p for p in papers if p["source"] != "Google Scholar"],
                   featured=[p for p in indexed if p.get("featured")][:3],
                   years=sorted({p["year"] for p in indexed if p.get("year")}, reverse=True),
                   metrics=snapshot["metrics"], sync_date=date, types=TYPES)
    (ROOT / "index.html").write_text(env.get_template("index.html").render(**context), encoding="utf-8")
    (ROOT / "data/publications.json").write_text(json.dumps(papers, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    pdf_cv(profile, papers, date, ROOT / "files/DongGeunKim_CV.pdf")
    # Explicit allowlist: never publish repository archives, temporary Word files, or build scripts.
    output = ROOT / "_site"
    output.mkdir(exist_ok=True)
    for name in ("index.html", "style.css", "script.js", "favicon.svg", ".nojekyll"):
        shutil.copy2(ROOT / name, output / name)
    (output / "images").mkdir(exist_ok=True)
    shutil.copy2(ROOT / "images/dgkim.jpg", output / "images/dgkim.jpg")
    (output / "assets/fonts").mkdir(parents=True, exist_ok=True)
    for name in ("NanumGothic-Regular.ttf", "NanumGothic-OFL.txt"):
        shutil.copy2(ROOT / "assets/fonts" / name, output / "assets/fonts" / name)
    (output / "files").mkdir(exist_ok=True)
    files = {p["pdf"] for p in papers if p["pdf"]} | {"files/DongGeunKim_CV.pdf"}
    for name in files:
        shutil.copy2(ROOT / name, output / name)
    (output / "data").mkdir(exist_ok=True)
    shutil.copy2(ROOT / "data/publications.json", output / "data/publications.json")
    print(f"Built website + PDF CV: {len(indexed)} Scholar publications, {len(papers)-len(indexed)} additional records.")


if __name__ == "__main__":
    main()
