from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle
from reportlab.lib.pagesizes import A4

filename = 'pdftable.pdf'
data = [
    ["Tom",12,"Gun",100],
    ["Jack",13,"Car",150],
    ["Will",14,"Book",200],
    ["Bill",13,"Ball",250]
]
table = Table(data)
pdf = SimpleDocTemplate(filename,pagesize=A4)
style = TableStyle([
    ('BACKGROUND',(0,0),(3,0),colors.green),
    ('TEXTCOLOR',(0,0),(3,0),colors.whitesmoke),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('FONTNAME',(0,0),(-1,0),'Courier-Bold'),
    ('FONTSIZE',(0,0),(-1,0),12),

    ('BOTTOMPADDING',(0,0),(-1,0),12),
    ('BACKGROUND',(0,1),(-1,-1),colors.beige),
    ('BOX',(0,0),(-1,0),2,colors.black),
    ('GRID',(0,0),(-1,-1),1,colors.black)
])
table.setStyle(style)

# ALTERNATE BACKGROUND
rownumb = len(data)
for i in range(1,rownumb):
    if i % 2 == 0:
        bc = colors.burlywood
    else:
        bc = colors.beige

    tx = TableStyle([('BACKGROUND',(0,i),(-1,i),bc)])
    table.setStyle(tx)




elems = []
elems.append(table)

pdf.build(elems)

