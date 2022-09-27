from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, 
    QDialog, 
    QListView, 
    QMainWindow, 
    QTableView, 
    QVBoxLayout, 
    QWidget, 
    QTabWidget,
    QLineEdit)

from PyQt5.QtCore import (
    Qt, 
    QObject, 
    QRunnable, 
    QThreadPool, 
    QTimer)
   
from PyQt5 import QtGui

from table_model import TableModel
from list_model import ListModel
from database import GetDB
import numpy as np
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # list view ModelView concept
        # uic.loadUi("D:\VSCODE\myPyQt5\Project1\exam1.ui", self)
        # self.threadpool = QThreadPool()
        # self.data = [(False, 'my first todo'),(True, 'my first todo'),(False, 'my first todo')]
        # self.model = DataModel(item = self.data)
        # self.listView.setModel(self.model)

        # Table view ModelView concept
        # self.table = QTableView() 

        # data = GetDB("localhost","client1","admin","test").selectdata()
        # self.model = TableModel(data[1:],data[0])
        # self.table.setModel(self.model)
        # self.setCentralWidget(self.table)

        data = [(False, 'an item'), (True, 'another item'),(True, 'another item')]

        self.list = QListView()
        self.model = ListModel(data)
        self.list.setModel(self.model)
        self.setCentralWidget(self.list)

        # self.table.setRowCount(5)
        # self.table.setColumnCount(3)

       

        # self.layout = QVBoxLayout()
        # self.layout.addWidget(self.table)
        # self.setLayout(self.vBox)

        # self.container = QWidget()
        # self.container.setLayout(self.layout)
        # self.setCentralWidget(self.table)



