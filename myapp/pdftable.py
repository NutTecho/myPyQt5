import os
import time
import pymssql
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER,TA_LEFT,TA_RIGHT
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Spacer,Image,Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pdfencrypt import StandardEncryption

filename =  os.path.join('.\\pdftable.pdf')
pdf = SimpleDocTemplate(filename,pagesize=A4,
                        rightMargin=25,leftMargin=25,
                        topMargin=25,bottomMargin=25)

def GetDB(server,user,password,database):
    listdata = []
    with pymssql.connect(server,user,password,database) as conn:
        with conn.cursor(as_dict = False) as cursor:
            cursor.execute('SELECT * FROM dbo.Customers')
            listdata.append(col[0] for col in cursor.description)
            for row in cursor:
                listdata.append(row)
                # print(row)

    return listdata


def ReportGen(pdf,size):

    elems = []

    # data = [
    #     ("Tom",12,"Gun",100),
    #     ("Jack",13,"Car",150),
    #     ("Will",14,"Book",200),
    #     ("Bill",13,"Ball",250)
    # ]

    data = GetDB("localhost","client1","admin","Northwind")
    # print(data)

    width,height = A4
    widthtList = [
        width * 20 /100,
        width * 20/100,
        width * 20/100,
        width * 20/100,
        ]

    styles=getSampleStyleSheet()
    # styleN = styles["BodyText"]

    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '%s' % time.ctime()

    elems.append(Paragraph(ptext, styles["Normal"]))
    elems.append(Spacer(1, 12))

    table = Table(data,colWidths=50,repeatRows=1,hAlign=TA_CENTER,vAlign=TA_CENTER)

    style = TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.green),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME',(0,0),(-1,0),'Courier-Bold'),
        ('FONTSIZE',(0,0),(-1,0),12),

        ('BOTTOMPADDING',(0,0),(-1,0),12),
        ('BACKGROUND',(0,1),(-1,-1),colors.beige),
        ('BOX',(0,0),(-1,0),2,colors.black),
        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('ALIGN',(0,0),(-1,0),'CENTER'),
        # ('VALIGN',(0,0),(-1,0),'CENTER'),
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

    pdf.build(elems)
    # print(filename)

ReportGen(pdf,size=A4)



