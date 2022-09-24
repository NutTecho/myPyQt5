from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, PageTemplate
from reportlab.platypus.frames import Frame
from reportlab.lib import pagesizes
from reportlab.platypus.paragraph import Paragraph
from functools import partial
import os

def header(canvas, doc, content):
    canvas.saveState()
    w, h = content.wrap(doc.width, doc.topMargin)
    content.drawOn(canvas, doc.leftMargin, doc.height + doc.bottomMargin + doc.topMargin - h)
    canvas.restoreState()

def footer(canvas, doc, content):
    canvas.saveState()
    w, h = content.wrap(doc.width, doc.bottomMargin)
    content.drawOn(canvas, doc.leftMargin, h)
    canvas.restoreState()

def header_and_footer(canvas, doc, header_content, footer_content):
    header(canvas, doc, header_content)
    footer(canvas, doc, footer_content)

styles = getSampleStyleSheet()

filename =  os.path.join('.\\template.pdf')

PAGESIZE = pagesizes.portrait(pagesizes.A4)

pdf = SimpleDocTemplate(filename, pagesize=PAGESIZE, 
        leftMargin = 2.2 * cm, 
        rightMargin = 2.2 * cm,
        topMargin = 1.5 * cm, 
        bottomMargin = 2.5 * cm)

frame = Frame(pdf.leftMargin, pdf.bottomMargin, pdf.width, pdf.height, id='normal')

header_content = Paragraph("This is a header. testing testing testing  ", styles['Normal'])
footer_content = Paragraph("This is a footer. It goes on every page.  ", styles['Normal'])

template = PageTemplate(id='test', frames=frame, onPage=partial(header_and_footer, header_content=header_content, footer_content=footer_content))

pdf.addPageTemplates([template])
pdf.build([Paragraph("This is content")])