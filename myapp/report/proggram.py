from reportlab.platypus import Table
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pdfencrypt import StandardEncryption
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from header import genHeaderReport
from body import genBodyReport
from footer import genFooterReport


# ====== register font and family==========
# pdfmetrics.registerFont(
#     TTFont('arabic',r'resource\xx.ttf')
# )

# pdfmetrics.registerFont(
#     TTFont('newBold',r'resource\xx.ttf')
# )

# pdfmetrics.registerFont(
#     TTFont('newItalic',r'resource\xx.ttf')
# )

# pdfmetrics.registerFontFamily(
#     'newNoemal',
#     normal='newNormal',
#     bold='newBold',
#     italic='newItalic',
#     boldItalic=''
# )

# ========================================


sec = StandardEncryption('1234','12345',canPrint=0)  #lock with user password
pdf = Canvas('report.pdf',pagesize=A4,encrypt = sec)
pdf.setTitle('MyReport')

def pdfReportGen(pdf,size):
   
    width,height = size
    heightList = [
        height * 20 /100,
        height * 77/100,
        height * 3/100,
    ]

    mainTable = Table([
        [genHeaderReport(width,heightList[0])],     #header
        [genBodyReport(width,heightList[1])],       #body
        [genFooterReport(width,heightList[2])],     #footer
    ],
    colWidths=width,
    rowHeights= heightList)

    mainTable.setStyle([
        # ('GRID',(0,0),(-1,-1),1,'red'),
        ('LEFTPADDING',(0,0),(0,2),0),
        ('BOTTOMPADDIG',(0,0),(-1,-1),0) 
    ])


    pageno = pdf.getPageNumber() # get page number
    print(pageno)
    x = width * 92 /100            # set position to head  
    y = height * 98 /100
    pdf.setFillColor('white')     # set color to white

    mainTable.wrapOn(pdf,0,0)
    mainTable.drawOn(pdf,0,0)
    pdf.drawString(x,y,f'Page {pageno}')
    pdf.showPage()   # this is page break

# add book mark and outline
pdf.bookmarkPage('p1')
pdf.addOutlineEntry('Page 1','p1')
pdf.setPageSize(size=A4)
pdfReportGen(pdf,size=A4)

pdf.bookmarkPage('p2')
pdf.addOutlineEntry('Page 2','p2')
pdf.setPageSize(size=landscape(A4))
pdfReportGen(pdf,size=landscape(A4))


pdf.save()
