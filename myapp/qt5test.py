import sys
import os
from PyQt5 import QAxContainer,QtCore
from PyQt5.QtWidgets import QApplication,QTextEdit,QWidget,QMessageBox,QMainWindow,QLineEdit,QVBoxLayout
from PyQt5 import uic,QtWidgets,QtWebEngineWidgets
# from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import Qt,QUrl
from datetime import datetime
import pymssql
import os

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('D:\VSCODE\myPyQt5\myapp\qt5demo.ui',self)
        self.setWindowTitle('Qt5Demotest')
        self.pushButton.clicked.connect(self.printdata)
        self.comboBox.addItem('c')
        self.pushButton_2.clicked.connect(self.getcombo)
        self.dateTimeEdit.dateTime = datetime.now
        self.tableWidget.setColumnWidth(0,50)
        self.tableWidget.setColumnWidth(1,100)
        self.tableWidget.setColumnWidth(2,50)
        self.tableWidget.setColumnWidth(3,100)
        self.getdb()
        self.Slider1.valueChanged['int'].connect(self.scrolllb.setNum)
        self.Slider1.valueChanged['int'].connect(self.countdata)

    def printdata(self):
        a = int(self.lineEdit.text())
        b = int(self.lineEdit_2.text())
        self.lineEdit_3.setText(str(a+b))
        print(self.lineEdit_3.text())
        msg = QMessageBox()
        msg.setWindowTitle("test message")
        msg.setText("this is main")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Cancel|QMessageBox.Ignore|QMessageBox.Ok)
        msg.setInformativeText("informative text, yal")
        msg.setDetailedText("test detail")

        msg.buttonClicked.connect(self.popup_button)
        
        x = msg.exec_()

    def popup_button(self,i):
        print(i.text())

    def getcombo(self):
        data = self.comboBox.currentText()
        index = self.comboBox.findText(data)
        print(index)
        print(data)
        if index == 0:
            self.scrolllb.setStyleSheet("background-color: rgb(255, 0, 0)")
        elif index ==1:
            self.scrolllb.setStyleSheet("background-color: rgb(125, 255, 0)")
        else:
            self.scrolllb.setStyleSheet("background-color: rgb(125, 125, 255)")

    
    def getdb(self):
        con_string = """Driver={SQL Server};
                Server=127.0.0.1;
                Database = test;
                UID = client1;
                PWD = nutert0405;
                """
        sql = """ SELECT * FROM test.dbo.xx	"""
        # try:
        #     with pyodbc.connect(con_string) as con:
        #         c1 = con.cursor()
        #         c1.execute(sql)
        #         self.tableWidget.setRowCount(8)
        #         for i,row in enumerate(c1):
        #             self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(str(row[0])))
        #             self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(row[1]))
        #             self.tableWidget.setItem(i,2,QtWidgets.QTableWidgetItem(str(row[3])))
        #             self.tableWidget.setItem(i,3,QtWidgets.QTableWidgetItem(row[4]))


        # except Exception as e:
        #     print('Error -> {}'.format(e))

    def countdata(self,value):
        print(value)


class GetDB():
    def __init__(self,server,user,password,database,*args, **kwargs):
        super(GetDB, self).__init__(*args, **kwargs)
        self.conn =  pymssql.connect(server,user,password,database)
        self.cursor = self.conn.cursor()
        
        
    def selectdata(self):
        listdata = []
        self.cursor.execute('SELECT * FROM dbo.xx')
        # print(self.cursor.fetchall())
        for row in self.cursor:
            listdata.append(row)
          

        return listdata

class PDFtest(QMainWindow):
    def __init__(self):
        super(PDFtest, self).__init__()
        PDFJS = r'D:\VSCODE\myPyQt5\pdfjs\web\viewer.html'
        # PDFJS = 'file:///usr/share/pdf.js/web/viewer.html'
        PDF = r'D:\VSCODE\myPyQt5\pdftable.pdf'

        # PDFJS2 = f"file://{os.path.abspath('./web/viewer.html')}"
        # print(PDFJS2)
        # PDF2 = f'file://{"%20".join(sys.argv[1:])}'
        # print("loading PDF:", PDF2)
        self.input1 = QLineEdit()
        self.browser = QtWebEngineWidgets.QWebEngineView()

        settings = self.browser.settings()
        settings.setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)

  
        full_url = QUrl.fromUserInput(PDFJS).toString() + '?file=' + QUrl.fromUserInput(PDF).toString()
  
        self.browser.load(QUrl.fromUserInput(full_url)) 
        print(QUrl.fromUserInput(full_url)) 

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.input1)
        self.layout.addWidget(self.browser)

        self.container = QWidget()
        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)

        # self.show()
        # self.load(QUrl("www.google.com"))
     

if __name__ == '__main__':
    # print(
    #     f"PyQt5 version: {QtCore.PYQT_VERSION_STR}, Qt version: {QtCore.QT_VERSION_STR}"
    # )
    app = QApplication(sys.argv)
    demo = PDFtest()
    # demo.setGeometry(600, 50, 800, 600)
    # demo = AppDemo()
    demo.show()
    # v = qpageview.View()
    # v.show()
    # v.loadPdf(r"D:\VSCODE\myPyQt5\report.pdf")


    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('closing window')

    



    
        
