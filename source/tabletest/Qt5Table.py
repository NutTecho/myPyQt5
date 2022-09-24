from resources import *
import textwrap
from PyQt5 import QtCore, QtGui, uic 
from PyQt5.QtWidgets import QApplication, QListView, QMainWindow, QTableView, QVBoxLayout, QWidget, QTabWidget
from PyQt5.QtGui import QColor,QIcon
from PyQt5.QtCore import QVariant, Qt,QAbstractListModel,QAbstractTableModel , QModelIndex, QRunnable, QThreadPool, QTimer, Qt,QTimer, pyqtSignal, pyqtSlot
import sys
from datetime import datetime
import pymssql

# ===== use pyrcc5 resources.qrc -o resources.py  to create qrc file=====

class DataModel(QAbstractTableModel):
    def __init__(self, item,header,parent = None,*args,**kwargs):
        super(DataModel,self).__init__(parent,*args,**kwargs)
        self.listitem = item
        self.listheader = header
        self.listindex = range(1,len(item)+1)

    def data(self,index,role):
        value = self.listitem[index.row()][index.column()]
        if role == Qt.DisplayRole:

            if isinstance(value,str):
                return "%s" % value

            if isinstance(value,float):
                return "%.2f" %value

            if isinstance(value, datetime):
                return value.strftime("%Y-%m-%d")

            return value
            
        if role == Qt.ForegroundRole:
            if (
                (isinstance(value, int) or isinstance(value, float))
                and value > 10
                ):
                return QColor('red')

        # if role == Qt.BackgroundRole:
        #     if (isinstance(value, int) or isinstance(value, float) and value > 10):
        #         value = int(value)
        #         return QColor('#053061')



        if role == Qt.DecorationRole:
            # value = self.listitem[index.row()][index.column()]
            if isinstance(value,int) and value > 10:
                if value:
                    # return QtGui.QIcon(r'D:\VSCODE\myPyQt5\myapp\tabletest\tick.png')
                    return QtGui.QIcon(":/icons/tick.png")
            # return QtGui.QIcon(r'D:\VSCODE\myPyQt5\myapp\tabletest\cross.png')
            return QtGui.QIcon(":/icons/cross.png")

            if isinstance(value, datetime):
                # return QtGui.QIcon(r'D:\VSCODE\myPyQt5\myapp\tabletest\calendar.png')
                return QtGui.QIcon(":/icons/calendar.png")


    def rowCount(self, index):
        #self.listitem.shape[0] when use numpy or pandas
        return len(self.listitem)

    def columnCount(self,index):
        #self.listitem.shape[1] when use numpy or pandas
        return len(self.listitem[0])

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return QVariant(self.listheader[section])
                # return str(self.listitem.column[section])
            if orientation == Qt.Vertical:
                # return str(self.listitem.index[section])
                return QVariant(self.listindex[section])
            return QVariant()


class GetDB():
    def __init__(self,*args, **kwargs):
        super(GetDB, self).__init__(*args, **kwargs)
        # self.conn =  pymssql.connect(server,user,password,database)
        # self.cursor = self.conn.cursor(as_dict = False)
        
      
    def selectdata(self,server,user,password,database):
        listdata = []
        with pymssql.connect(server,user,password,database) as conn:
            with conn.cursor(as_dict=False) as cursor:
                cursor.execute('SELECT * FROM dbo.xx')
                listdata.append( list(col[0] for col in cursor.description))
                print(listdata)
                for row in cursor:
                    listdata.append(row)
                    # print(row)
                # print(self.cursor.fetchall())
                # return  self.cursor.fetchall()
        return listdata

           

UiMain,QtBaseClass = uic.loadUiType(r'D:\VSCODE\myPyQt5\myapp\tabletest\tabletest.ui')


class MainWindow(QMainWindow,UiMain):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        UiMain.__init__(self)
        self.setupUi(self)

        self.db = GetDB()
        self.data = self.db.selectdata("localhost","client1","admin","test")
        # print(self.data)
        # self.model = DataModel(item = [[1,2,3],[4,5,6],[7,8,9]])

        # data = [
        # [True, 9, 2],
        # [1, 0, -1],
        # [3, 5, False],
        # [3, 3, 2],
        # [datetime(2019, 5, 4), 8, 9],
        # ]

        # header = ["id","fname","lname","age","toy","money"]

        # header = self.db.getheader()
        # print(header)
       
        self.model2 = DataModel(item = self.data[1:],header = self.data[0])
        # self.listView.setModel(self.model)
        self.tableView.setModel(self.model2)
        self.tableView.clicked.connect(self.getindex)
        # self.tableView.selectionModel.selectionChanged.connect(self.getindex)

    def getindex(self,selected):
        print(selected.row())
        print(selected.data())


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()