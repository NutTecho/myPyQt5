from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class DemoDialog(QDialog):
    def __init__(self):
        super(DemoDialog,self).__init__()
        uic.loadUi('D:\VSCODE\myPyQt5\source\dai.ui', self)