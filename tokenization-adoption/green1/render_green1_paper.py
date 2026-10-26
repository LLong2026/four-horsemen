#!/usr/bin/env python3
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'GREEN1_PAPER_v1.0.md')
OUT = os.path.join(HERE, 'GREEN1_PAPER_v1.0.pdf')
pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DejaVu', normal='DejaVu', bold='DejaVu-Bold', italic='DejaVu', boldItalic='DejaVu-Bold')
S = {
 'title': ParagraphStyle('title', fontName='DejaVu-Bold', fontSize=14.5, leading=20, spaceAfter=10, textColor=colors.HexColor('#142339'), alignment=TA_CENTER),
 'h1': ParagraphStyle('h1', fontName='DejaVu-Bold', fontSize=11.5, leading=16, spaceBefore=16, spaceAfter=8, textColor=colors.HexColor('#142339'), keepWithNext=True),
 'body': ParagraphStyle('body', fontName='DejaVu', fontSize=8.8, leading=14, spaceAfter=7),
 'bullet': ParagraphStyle('bullet', fontName='DejaVu', fontSize=8.8, leading=14, leftIndent=16, firstLineIndent=-12, spaceAfter=5),
}
def esc(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
story = []
lines = open(SRC).read().split('\n')
title_done = False
for ln in lines:
    t = esc(ln.strip())
    if ln.startswith('# ') and not title_done:
        story.append(Paragraph(t, S['title'])); story.append(Spacer(1, 6))
        story.append(Paragraph('Leon Calvin Long, II — SquirlOS Technologies LLC · 2026-10-26', ParagraphStyle('sub', fontName='DejaVu', fontSize=9, leading=14, alignment=TA_CENTER, textColor=colors.HexColor('#35485c'), spaceAfter=4)))
        story.append(Paragraph('v1.0, 2026-10-26 (two-key curation: vetted by the system (Gabriel), owner GO — Leon GO, chat authorization, 2026-10-26 00:34 CT)', ParagraphStyle('sub2', fontName='DejaVu', fontSize=8, leading=12, alignment=TA_CENTER, textColor=colors.HexColor('#35485c'), spaceAfter=14)))
        story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#142339'), spaceAfter=12))
        title_done = True
    elif ln.startswith('## '):
        story.append(Paragraph(t[3:], S['h1']))
    elif ln.startswith('- '):
        story.append(Paragraph('• ' + t[2:], S['bullet']))
    elif ln.strip():
        story.append(Paragraph(t, S['body']))
doc = SimpleDocTemplate(OUT, pagesize=letter, leftMargin=0.85*72, rightMargin=0.85*72, topMargin=0.75*72, bottomMargin=0.75*72, title='Trust Is the Pollutant (SQUIRL OS GREEN-1)', author='Leon Calvin Long, II')
doc.build(story)
print("built", OUT)
