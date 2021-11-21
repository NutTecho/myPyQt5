import os
import sys
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from pdfrw.objects import pdfstring
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4

outfile = "render.pdf"
infile = os.path.join(sys.path[0],"temp4.pdf")

template = PdfReader(infile,decompress=False)
template_obj = pagexobj(template.pages[0])

pdf = Canvas(outfile,pagesize=A4)

#set output map with template
newname = makerl(pdf,template_obj)
# print(pdf.keys())
# print(pdf.Info)
# print(pdf.Root.keys())
# print(template.Root.AcroForm.Fields)


# get field name and position from pdf form 
for page in template.Root.Pages.Kids:
    for field in page.Annots:
        label =  field.T
        sides_positions = field.Rect
        left = min(sides_positions[0], sides_positions[2])
        bottom = min(sides_positions[1], sides_positions[3])

        user_data = {
            '(firstname)': 'Tom',
            '(lastname)': 'Hank',
            '(age)': '14',
        }
        value = user_data.get(str(label))
        print(value)
        
        padding = 10.0
        line_height = 15.0

        # input text to text field
        pdf.drawString(x= float(left), y = float(bottom), text=value)

pdf.save()
