from reportlab.platypus import Table
from reportlab.lib import colors


def genBodyReport(width,height):
    widthlist = [
        width * 10 / 100,
        width * 80 / 100,
        width * 10 / 100,
    ]

    heightlist = [
        height * 10 / 100,
        height * 15 / 100,
        height * 35 / 100,
        height * 30 / 100,
        height * 10 / 100,

    ]

    res = Table([
        ['',_genoffer(widthlist[1],heightlist[0]),''],
        ['',_genabout(widthlist[1],heightlist[1]),''],
        ['',_genadress(widthlist[1],heightlist[2]),''],
        ['',_geninfo(widthlist[1],heightlist[3]),''],
        ['',_genrecip(widthlist[1],heightlist[4]),''],
    ],
    widthlist,
    heightlist)

    res.setStyle([
        ('GRID',(0,0),(-1,-1),1,'red')
    ])
    return res


def _genoffer(width,height):
    return 'Offer'

def _genabout(width,heght):
    return 'About'

def _genadress(width,heght):
    return 'Address'

def _geninfo(width,heght):
    return 'Info'

def _genrecip(width,heght):
    return 'Recip'
