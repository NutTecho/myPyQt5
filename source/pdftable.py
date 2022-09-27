import os
import time
import pymssql
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER,TA_LEFT,TA_RIGHT
from reportlab.lib import colors
from reportlab.pdfgen.canvas import Canvas 
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Spacer,Image,Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

filename =  os.path.join('.\\pdftable.pdf')
pdf = SimpleDocTemplate(filename,pagesize=A4,
                        rightMargin=25,leftMargin=25,
                        topMargin=25,bottomMargin=25)

class PageNumCanvas(canvas.Canvas):
    """
    http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    """
    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas. __init__(self, *args, **kwargs)
        self.pages = []
        
    #----------------------------------------------------------------------
    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()
        
    #----------------------------------------------------------------------
    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)
        
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)

        canvas.Canvas.save(self)
        
    #----------------------------------------------------------------------
    def draw_page_number(self, page_count):
        """
        Add the page number
        """
        page = "Page %s of %s" % (self._pageNumber, page_count)
        self.setFont("Helvetica", 9)
        self.setFillColor('red')
        self.drawRightString(195*mm, 272*mm, page)


def GetDB(server,user,password,database):
    listdata = []
    with pymssql.connect(server,user,password,database) as conn:
        with conn.cursor(as_dict = False) as cursor:
            cursor.execute('SELECT CustomerID, CompanyName, ContactName, ContactTitle, Address,City,Country FROM dbo.Customers')
            listdata.append(col[0] for col in cursor.description)
            for row in cursor:
                listdata.append(row)
    return listdata

def addPageNumber(canvas,doc):
    pageno = canvas.getPageNumber() # get page number
    print(pageno)
    width,height = A4
    x1 = width * 92 /100            # set position to head  
    y1 = height * 98 /100

    x2 = width * 10 /100            # set position to head  
    y2 = height * 98 /100
    canvas.setFillColor('red')     # set color to white
    printtime = '%s' % time.ctime()
    canvas.drawString(x1, y1,f'Page {pageno}')
    canvas.drawString(x2, y2,printtime)

    canvas.drawString( width * 10 /100 , height * 3 /100,"this is footer on page")

    # canvas.showPage()   # this is page break
    

def ReportGen(pdf,size):

    elems = []

    detail_head = [
        ([Paragraph(cell) for cell in ("50T7XX","LOT : 100","SEQ : 12","QTY : 20")]),
        ([Paragraph(cell) for cell in ("PUHT-EP500","","CAR","")]),
   ]

    width,height = size
    widthtList = [
        width * 20/100,
        width * 20/100,
        width * 20/100,
        width * 20/100,
        ]

    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    # styleN.wordWrap = 'CJK'
    styleN.wordWrap = 'LTR'

    data = GetDB("localhost","client1","admin","Northwind")
    data2 = [[Paragraph(cell, styleN) for cell in row] for row in data]
    # print(list(data[0]))

    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '%s' % time.ctime()

    # header
    # data3 = [[Paragraph(cell, styleN) for cell in row] for row in detail_head]
    
    tablehead = Table(detail_head,repeatRows=1,colWidths=[100,100,100,100],hAlign='LEFT')
    style_head = TableStyle([
        # ('BACKGROUND',(0,0),(-1,-1),colors.green),
        # ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        # ('ALIGN',(0,0),(-1,-1),'CENTER'),
        # ('FONTNAME',(0,0),(-1,0),'Courier-Bold'),
        ('FONTSIZE',(0,0),(-1,-1),12),
        ('SPAN',(0,1),(1,1)),
        ('LEFTPADDING',(0,0),(-1,-1),12),
        ('BACKGROUND',(0,0),(-1,-1),colors.white),
        # ('BOX',(0,0),(-1,0),2,colors.black),
        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ])
    tablehead.setStyle(style_head)
    
    elems.append(tablehead)


    # elems.append(Paragraph(ptext, styles["Normal"]))
    elems.append(Spacer(1, 12))

    # body table
    table = Table(data2,repeatRows=1,hAlign=True,vAlign=True)

    style = TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.green),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        # ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME',(0,0),(-1,0),'Courier-Bold'),
        ('FONTSIZE',(0,0),(-1,0),12),

        # ('BOTTOMPADDING',(0,0),(-1,0),12),
        ('BACKGROUND',(0,1),(-1,-1),colors.beige),
        # ('BOX',(0,0),(-1,0),2,colors.black),
        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ])
    table.setStyle(style)
    

    # ALTERNATE BACKGROUND
    # rownumb = len(data)
    # for i in range(1,rownumb):
    #     if i % 2 == 0:
    #         bc = colors.burlywood
    #     else:
    #         bc = colors.beige

    #     tx = TableStyle([('BACKGROUND',(0,i),(-1,i),bc)])
    #     table.setStyle(tx)
   
    elems.append(table)
    
    # add all element to pdf
    # pdf.build(elems)

     #add footer
    footertext = "only last page use this footer"
    elems.append(Paragraph(footertext, styles["Normal"]))
    # elems.append(Spacer(1, 12))


    pdf.build(elems, onFirstPage=addPageNumber, onLaterPages=addPageNumber)
    # pdf.build(elems, canvasmaker=PageNumCanvas)
    
    # print(filename)

   
if __name__ == "__main__":
    ReportGen(pdf,size=A4)



