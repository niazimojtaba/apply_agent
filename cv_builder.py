"""
cv_builder.py — shared rendering engine for all CV scripts.

Usage in a per-role script:
    from cv_builder import CVBuilder
    cv = CVBuilder("outputs/CV_Jane_Smith_Acme_Engineer.pdf")
    cv.header("Senior Backend Engineer — Go & Kubernetes")
    cv.summary("…")
    cv.skills([("Languages", "Go, Python, C++"), ("Cloud", "AWS, Kubernetes")])
    cv.job("Acme Corp — Senior Engineer", "2022–Present | Berlin", "SaaS platform.", [...])
    cv.publications(["Smith et al., ICSE 2023."])
    cv.education([("MSc Computer Science", "TU Berlin (2018–2020)", "")])
    cv.awards(["1st place — …"])
    cv.build()
"""

import yaml
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_JUSTIFY

_PROFILE_PATH = Path(__file__).parent / "profile.yaml"


def _load_profile() -> dict:
    with open(_PROFILE_PATH) as f:
        return yaml.safe_load(f)


class CVBuilder:
    def __init__(self, output_path: str):
        self._profile = _load_profile()
        accent_hex = self._profile.get("accent_color", "1a5276")
        self.ACCENT = colors.HexColor(f"#{accent_hex}")
        self.BLACK  = colors.black
        self.GRAY   = colors.HexColor("#555555")
        self._output = output_path
        self._story  = []
        W = A4[0] - 30 * mm
        self._W = W
        self._doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            leftMargin=15*mm, rightMargin=15*mm,
            topMargin=12*mm, bottomMargin=12*mm,
        )
        self._init_styles()

    def _init_styles(self):
        A, B, G = self.ACCENT, self.BLACK, self.GRAY
        def s(name, **kw):
            return ParagraphStyle(name, **kw)
        self.S_NAME    = s("name",    fontSize=20, leading=24, textColor=B, fontName="Helvetica-Bold")
        self.S_CONTACT = s("contact", fontSize=9,  leading=13, textColor=G, fontName="Helvetica")
        self.S_TITLE   = s("title",   fontSize=11, leading=14, textColor=A, fontName="Helvetica-Bold")
        self.S_SECTION = s("section", fontSize=10, leading=13, textColor=A, fontName="Helvetica-Bold", spaceBefore=6)
        self.S_BODY    = s("body",    fontSize=9,  leading=13, textColor=B, fontName="Helvetica", alignment=TA_JUSTIFY)
        self.S_JOBTIT  = s("jobtit",  fontSize=9,  leading=13, textColor=A, fontName="Helvetica-Bold")
        self.S_GRAY    = s("gray",    fontSize=8.5,leading=12, textColor=G, fontName="Helvetica")
        self.S_BULLET  = s("bullet",  fontSize=9,  leading=13, textColor=B, fontName="Helvetica",
                            leftIndent=12, alignment=TA_JUSTIFY)

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _section(self, title: str):
        self._story += [
            Spacer(1, 3*mm),
            Paragraph(title, self.S_SECTION),
            HRFlowable(width=self._W, thickness=0.6, color=self.ACCENT, spaceAfter=2),
        ]

    def _bullets(self, items: list[str]):
        return ListFlowable(
            [ListItem(Paragraph(i, self.S_BULLET),
                      bulletColor=self.ACCENT, leftIndent=12, bulletFontSize=8)
             for i in items],
            bulletType="bullet", bulletFontName="Helvetica", leftIndent=0, spaceBefore=1
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def header(self, role_title: str):
        """Render name, contact line, and role title from profile.yaml."""
        p = self._profile
        linkedin_url = p.get("linkedin", "")
        self._story.append(Paragraph(p["name"], self.S_NAME))
        self._story.append(Paragraph(
            f'{p["email"]} &nbsp;|&nbsp; '
            f'<a href="{linkedin_url}" color="#{self._profile.get("accent_color","1a5276")}">LinkedIn</a>'
            f' &nbsp;|&nbsp; {p["location"]} &nbsp;|&nbsp; {p["phone"]}',
            self.S_CONTACT
        ))
        self._story.append(Paragraph(role_title, self.S_TITLE))
        self._story.append(Spacer(1, 2*mm))

    def summary(self, text: str):
        """Add a SUMMARY section with the given paragraph text (HTML tags supported)."""
        self._section("SUMMARY")
        self._story.append(Paragraph(text, self.S_BODY))

    def skills(self, lines: list[tuple[str, str]]):
        """
        Add a TECHNICAL SKILLS section.
        lines: list of (label, value) — e.g. [("Languages", "Go, Python"), ...]
        """
        self._section("TECHNICAL SKILLS")
        for label, value in lines:
            self._story.append(Paragraph(f"<b>{label}:</b> {value}", self.S_BODY))

    def job(self, company_role: str, period_loc: str, desc: str, bullet_items: list[str]):
        """
        Add one work-experience entry.
        Call multiple times; the first call auto-inserts the WORK EXPERIENCE header.
        """
        if not hasattr(self, "_jobs_started"):
            self._section("WORK EXPERIENCE")
            self._jobs_started = True
        self._story += [
            Paragraph(company_role, self.S_JOBTIT),
            Paragraph(period_loc,   self.S_GRAY),
            Paragraph(desc,         self.S_GRAY),
            self._bullets(bullet_items),
            Spacer(1, 2*mm),
        ]

    def publications(self, items: list[str]):
        """Add a PUBLICATIONS section. Each item is a plain/HTML string."""
        self._section("PUBLICATIONS")
        for item in items:
            self._story.append(Paragraph(item, self.S_BODY))

    def education(self, entries: list[tuple[str, str, str]]):
        """
        Add an EDUCATION section.
        entries: list of (degree_bold, institution_period, extra_lines)
        extra_lines can be a newline-separated string or empty.
        """
        self._section("EDUCATION")
        for i, (degree, inst, extra) in enumerate(entries):
            text = f"<b>{degree}</b>, {inst}"
            if extra:
                text += "<br/>" + extra
            self._story.append(Paragraph(text, self.S_BODY))
            if i < len(entries) - 1:
                self._story.append(Spacer(1, 2*mm))

    def awards(self, items: list[str]):
        """Add an AWARDS section."""
        self._section("AWARDS")
        self._story.append(self._bullets(items))

    def build(self):
        """Render the PDF to the output path given at construction."""
        self._doc.build(self._story)
        print(f"Generated: {self._output}")
