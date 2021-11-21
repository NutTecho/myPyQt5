from reportlab.platypus import Table
from reportlab.lib import colors

def genFooterReport(width,height):
    text = 'contact Mr.Nut Techosakondee 0876154740 nutert321@gmail.com'
    color = colors.HexColor('#003363')
    res = Table([[text]],width,height)
    
    res.setStyle([
        ('GRID',(0,0),(-1,-1),1,'red'),
        ('LEFTPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDIG',(0,0),(-1,-1),0), 
        ('BACKGROUND',(0,0),(0,-1),color),
        ('TEXTCOLOR',(0,0),(-1,-1),'white'),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  
    ])
    return res