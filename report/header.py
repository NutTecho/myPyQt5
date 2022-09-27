from reportlab.platypus import Table,Image
from reportlab.lib import colors


def genHeaderReport(width,height):
    widthList = [
        width * 55 / 100,  #col1 left image 
        width * 45 /100,   #col2 right image
    ]

    leftImagePath = '.\\report\\a1.jpg'
    leftImageWidth = widthList[0]
    leftImage = Image(leftImagePath,leftImageWidth,height)

    rightImagePath = '.\\report\\a2.jpg'
    rightImageWidth = widthList[1]
    rightImage = Image(rightImagePath,rightImageWidth,height)


    res = Table([
        [leftImage, rightImage]
    ],
    colWidths=widthList,
    rowHeights=height)

    res.setStyle([
        ('GRID',(0,0),(0,-1),1,'red')
    ])


    return res