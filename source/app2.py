from PyQt5 import QtCore, QtGui, uic 
from PyQt5.QtWidgets import QApplication, QListView, QMainWindow, QTableView, QVBoxLayout, QWidget, QTabWidget
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt,QAbstractListModel, QObject, QRunnable, QThreadPool, QTimer, Qt,QTimer, pyqtSignal, pyqtSlot
from pyqtgraph import PlotWidget,mkPen
from MplWidget import MplWidget as mpl
import sys
import json
import pymssql
from random import randint
import matplotlib
matplotlib.use('Qt5Agg')

from pyqtgraph.graphicsItems.GradientEditorItem import Tick
from pyqtgraph.graphicsItems.PlotDataItem import dataType

from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch,cm
from reportlab.pdfgen.canvas import Canvas

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

doc = SimpleDocTemplate("result.pdf",pagesize=A4,rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)

Story = []
logo = "logo.png"

conn =  pymssql.connect("localhost","client1","admin","test")
cursor = conn.cursor(as_dict=True)


def getdb():
    c =  cursor.execute('SELECT * FROM dbo.xx where name = %s',"")
    return  c.fetchall()
   

# conn.close()



# with pymssql.connect() as conn:
#     with conn.cursor(as_dict=True) as cursor:
#         cursor.execute()



class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
    file_save_as = pyqtSignal(str)


class Generator(QRunnable):
    def __init__(self,fn,*args,**kwargs):
        super(Generator,self).__init__(self)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        self.kwargs['progress_callback'] = self.signals.progress


    def newgen(self):
        # add image
        im = Image(logo,2*inch,2*inch)
        Story.append(im)

        #set styles
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify',alighnment=TA_JUSTIFY))


        #set text
        ptext = '%s' % format
        Story.append(Paragraph(ptext,styles=["Normal"]))
        Story.append(Spacer(1,12))

        #build file
        doc.build(Story)

    '''
    Worker thread
    '''
    @pyqtSlot()
    def run(self):
        try:
            outfile = "result.pdf"
            template = PdfReader("template.pdf",decompress=False).pages[0]
            template_obj = pagexobj(template)

            canvas = Canvas(outfile)

            newname = makerl(canvas,template_obj)
            canvas.doForm(newname)
            canvas.drawString(170,170,self.data['name'])
            canvas.save()
        except Exception as e:
            self.signals.error.emit(str(e))
            return

        self.signals.file_save_as.emit(outfile)


class DataModel(QAbstractListModel):
    def __init__(self, *args , item = None,**kwargs):
        super(DataModel,self).__init__(*args,**kwargs)
        self.listitem = [] or item

    def data(self,index,role):
        if role == Qt.DisplayRole:
            _,text = self.listitem[index.row()]
            return text
        
        if role == Qt.DecorationRole:
            status,_ = self.listitem[index.row()]
            if status:
                return Tick

    def rowCount(self, index):
        return len(self.listitem)

    def columnCount(self,index):
        return len(self.listitem[0])
    

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        uic.loadUi('D:\VSCODE\myPyQt5\myapp\exam1.ui', self)
        self.threadpool = QThreadPool()
        self.x = list(range(100))
        self.y1 = [randint(0,100) for _ in range(100)]
        self.y2 = [randint(0,100) for _ in range(100)]

        # data = []
        # self.model = DataModel(data)

        self.table = QTableView()
        # self.table.setModel(self.model)
        #Load the UI Page
        # self.MplWidget(self,width=5,height=4,dpi=100)
        # self.addToolBar(NavigationToolbar(self.MplWidget.canvas ,self))
        # self.MplWidget.canvas.axes.plot(self.x, self.y)
        # self.MplWidget.canvas.axes.plot(t, sinus_signal)
        # self.test1.pressed.connect(self.slottest1)

        
        self.MplWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
        self.MplWidget.canvas.axes.set_xlabel('test x')
        self.MplWidget.canvas.axes.set_ylabel('test y')
        self.MplWidget.canvas.axes.grid(True)
        self.MplWidget.canvas.draw()

        self.plt_ref1 = None
        self.plt_ref2 = None
        # self.mplwidget.canvas = MplCanvas(self,width=5,height=4,dpi=100)
        # self.mplwidget.axes.plot(self.x,self.y)

        # self.toolbar = NavbarTool(self.sc,self)
        # self.layout = QVBoxLayout()
        # self.layout.addWidget(self.toolbar)
        # self.layout.addWidget(self.sc)

        # self.mplWidget().setLa
        # self.setLayout(self.layout)
        # self.setCentralWidget(self.widget)


        # use pyqtgraph to plot graph
      
       

        self.plot(self.x,self.y1,name="y1",color=(255,0,0))
        self.plot(self.x,self.y2,name="y2",color=(0,255,255))
        self.graphWidget.setBackground(QColor(100,50,254,25))
        self.graphWidget.setTitle("Your Title Here", color="b", size="15pt")
        styles = {'color':'r', 'font-size':'15px'}
        self.graphWidget.setLabel('left', 'Temperature (°C)', **styles)
        self.graphWidget.setLabel('bottom', 'Hour (H)', **styles)
        self.graphWidget.addLegend()
        self.graphWidget.showGrid(x=True, y=True)


        # self.setCentralWidget(self.graphWidget)

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_data)
        self.timer.start()

    def plot(self, hour, temperature,name,color):
        self.pencolor = mkPen(color=color,width=2,style=Qt.SolidLine)
        self.graphWidget.plot(hour, temperature, name=name ,pen=self.pencolor,symbol='+', symbolSize=10, symbolBrush=('b'))

    def update_data(self):
        self.x = self.x[1:]
        self.x.append(self.x[-1] + 1)

        self.y1 = self.y1[1:]
        self.y1.append(randint(0,100))

        self.y2 = self.y2[1:]
        self.y2.append(randint(0,100))

        self.graphWidget.clear()
        self.plot(self.x,self.y1,name="y1",color=(255,0,0))
        self.plot(self.x,self.y2,name="y2",color=(0,255,255))

        if(self.plt_ref1 is None and self.plt_ref2 is None):
            plt_ref1 =  self.MplWidget.canvas.axes.plot(self.x, self.y1)
            plt_ref2 =  self.MplWidget.canvas.axes.plot(self.x, self.y2)
            self.MplWidget.canvas.axes.legend(['y1','y2'],loc='upper right')
            self.plt_ref1 = plt_ref1[0]
            self.plt_ref2 = plt_ref2[0]
        else:
            # self.MplWidget.canvas.axes.cla() 
            self.plt_ref1.set_ydata(self.y1)
            self.plt_ref2.set_ydata(self.y2)
            # self.plt_ref1.set_xdata(self.x)
            # self.plt_ref2.set_xdata(self.x)
        
        # self.MplWidget.canvas.axes.bar(self.x, self.y)
        self.MplWidget.canvas.draw()

    def slottest1(self):
        print("test")

    def demotest(self):
        work = Generator([])
        # work.signals.error.connect()
        self.threadpool.start(work)


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()