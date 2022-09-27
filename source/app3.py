from PyQt5 import uic ,QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QListView, QMainWindow, QTableView, QVBoxLayout, QWidget, QTabWidget,QLineEdit
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt,QAbstractListModel, QObject, QRunnable, QThreadPool, QTimer, Qt,QTimer,QUrl,pyqtSignal, pyqtSlot
import sys
import os
import time
import pymssql
# import pdb

from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER,TA_LEFT,TA_RIGHT
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Spacer,Image,Table,PageTemplate,Frame, doctemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm,inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pdfencrypt import StandardEncryption
from functools import partial

from reportlab.platypus.flowables import PageBreak

class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
    file_save_as = pyqtSignal(str)

class GetDB():
    def __init__(self,server,user,password,database,*args, **kwargs):
        super(GetDB, self).__init__(*args, **kwargs)
        self.server = server
        self.user = user
        self.password = password
        self.database = database
        # self.conn =  pymssql.connect(self.server,self.user,self.password,self.database)
        # self.cursor = self.conn.cursor()
        
        
    def selectdata(self):
        listdata =[]
        with pymssql.connect(self.server,self.user,self.password,self.database) as conn:
            with conn.cursor(as_dict = False) as cursor:
                cursor.execute('''SELECT CustomerID, CompanyName, ContactName, ContactTitle, Address,City,Country,convert(varchar,isnull(PostalCode,'-')) as postal
                                 FROM dbo.Customers''')
                                #where CustomerID = %s''',getid)
                listdata.append(col[0] for col in cursor.description)
                for row in cursor:
                    listdata.append(row)
        return listdata
          

        return listdata

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.Canvas = canvas.Canvas
        self._saved_page_states = []
 

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
 

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            # pdb.set_trace()
            # self.setFont('Arial', 8)
            self.draw_page_number(num_pages)
            self.Canvas.showPage(self)
        self.Canvas.save(self)
 
 
    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString(211 * mm, 15 * mm + (0.2 * inch),
                             "Page %d of %d" % (self._pageNumber, page_count))

class Head_and_Foot():
    def __init__(self,*args,**kwargs):
        super(Head_and_Foot,self).__init__()
        # self.canvas = canvas
        # self.doc = doc
        # self.content = content
        # self.header = self.header()
        # self.footer = self.footer

    @staticmethod
    def header(canvas, doc, content):
        canvas.saveState()
        w, h = content.wrap(doc.width, doc.topMargin)
        content.drawOn(canvas, doc.leftMargin, doc.height + doc.bottomMargin + doc.topMargin - h)
        canvas.restoreState()

    @staticmethod
    def footer(canvas, doc, content):
        canvas.saveState()
        w, h = content.wrap(doc.width, doc.bottomMargin)
        content.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    @classmethod
    def header_and_footer(cls,canvas, doc, header_content, footer_content):
        cls.header(canvas, doc, header_content)
        cls.footer(canvas, doc, footer_content)


class GenPDF(QRunnable):
    def __init__(self,fn, getid = None,*args,**kwargs):
        super(GenPDF,self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.getid = getid
        self.signals = WorkerSignals()

        self.kwargs['progress_callback'] = self.signals.progress

    @staticmethod
    def _header_footer(canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        # styles = getSampleStyleSheet()
 
        # Header
        header = Paragraph('This is a multi-line header.  It goes on every page.   ')
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin,doc.height + doc.bottomMargin + doc.topMargin - h)
 
        # Footer
        footer = Paragraph('This is a multi-line footer.  It goes on every page.   ')
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
 
        # Release the canvas
        canvas.restoreState()  
    
    '''
    Worker thread
    '''
    @pyqtSlot()
    def run(self):
        filename =  os.path.join('.\\pdftable.pdf')
        pdf = SimpleDocTemplate(filename,pagesize=A4 )

        styles = getSampleStyleSheet()
        styleN = styles["BodyText"]
        # styleN.wordWrap = 'CJK'
        styleN.wordWrap = 'LTR'

        # frame = Frame(pdf.leftMargin,pdf.bottomMargin,pdf.width,pdf.height,id='normal')
        # header_content = Paragraph("This is a header. testing testing testing  ", styles['Normal'])
        # footer_content = Paragraph("This is a footer. It goes on every page.  ", styles['Normal'])

        # template = PageTemplate(id='test', frames=frame, onPage=partial(Head_and_Foot().header_and_footer, header_content=header_content, footer_content=footer_content))

        
        elems = []

        # data = [
        #     ("Tom",12,"Gun",100),
        #     ("Jack",13,"Car",150),
        #     ("Will",14,"Book",200),
        #     ("Bill",13,"Ball",250)
        # ]

        width,height = A4
        widthtList = [
            width * 20 /100,
            width * 20/100,
            width * 20/100,
            width * 20/100,
            ]

        

        print(self.getid)
        data = GetDB("localhost","client1","admin","Northwind").selectdata()
        # print(data)
        data2 = [[Paragraph(cell, styleN) for cell in row] for row in data]
        # print(list(data[0]))

        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        ptext = '%s' % time.ctime()

        elems.append(Paragraph(ptext, styles["Normal"]))
        elems.append(Spacer(1, 12))

        table = Table(data2,repeatRows=1,hAlign=TA_LEFT,vAlign=TA_JUSTIFY)

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
        # elems.append(PageBreak())

        try:
            # pdf.addPageTemplates([template])
            pdf.build(elems,onFirstPage=self._header_footer, onLaterPages=self._header_footer,canvasmaker=NumberedCanvas)
            # print(filename)
        except Exception as e:
            self.signals.error.emit(str(e))
            return

        # self.signals.file_save_as.emit(filename)


class DemoDialog(QDialog):
    def __init__(self):
        super(DemoDialog,self).__init__()
        uic.loadUi('D:\VSCODE\myPyQt5\source\dai.ui', self)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('D:\VSCODE\myPyQt5\source\genreport.ui', self)
        # self.browser = QtWebEngineWidgets.QWebEngineView()

        # self.settings = self.browser.settings()
        # self.settings.setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)

        # full_url = QUrl.fromUserInput(self.PDFJS).toString() + '?file=' + QUrl.fromUserInput(self.PDF).toString()
        
        # print(QUrl.fromUserInput(full_url)) 
        # self.WebWidget.load(QUrl.fromUserInput(full_url)) 
        # self.c1.text
        
        self.threadpool = QThreadPool()
        self.ref1.clicked.connect(self.chagefile)
        self.showdi.clicked.connect(self.demodialog)
        self.homebut.clicked.connect(self.gohome)
        self.reportbut.clicked.connect(self.goreport)
        self.aboutbut.clicked.connect(self.goabout)

        self.stack1.setCurrentWidget(self.Homepage)


    def demodialog(self):
        dlg = DemoDialog()
        dlg.exec()

    def gohome(self):
        self.stack1.setCurrentWidget(self.Homepage)

    def goreport(self):
        self.stack1.setCurrentWidget(self.Reportpage)

    def goabout(self):
        self.stack1.setCurrentWidget(self.Aboutpage)




    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):
        # for n in range(0, 5):
        #     time.sleep(1)
        progress_callback.emit(0)

        return "Done."

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def chagefile(self):
        worker = GenPDF(fn=[],getid=self.c1.text()) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        # GenPDF(sys.argv)
        # work.signals.error.connect()
        self.threadpool.start(worker)
        # print(self.c1.text())

        self.PDFJS = r'D:\VSCODE\myPyQt5\pdfjs\web\viewer.html'
        self.PDF = r'D:\VSCODE\myPyQt5\pdftable.pdf'
        full_url = QUrl.fromUserInput(self.PDFJS).toString() + '?file=' + QUrl.fromUserInput(self.PDF).toString()
        self.WebWidget.load(QUrl.fromUserInput(full_url)) 
    
def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()