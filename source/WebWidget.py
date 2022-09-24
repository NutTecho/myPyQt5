from PyQt5.QtWidgets import QWidget,QVBoxLayout
from PyQt5 import uic,QtWidgets,QtWebEngineWidgets
from PyQt5.QtCore import Qt,QUrl


class WebWidget(QWidget):
     def __init__(self,  parent=None):
        super(WebWidget, self).__init__()
        self.PDFJS = r'D:\VSCODE\myPyQt5\pdfjs\web\viewer.html'
        self.PDF = r'D:\VSCODE\myPyQt5\pdftable.pdf'
        
        self.browser = QtWebEngineWidgets.QWebEngineView()

        self.settings = self.browser.settings()
        self.settings.setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)

        full_url = QUrl.fromUserInput(self.PDFJS).toString() + '?file=' + QUrl.fromUserInput(self.PDF).toString()
        
        self.browser.load(QUrl.fromUserInput(full_url)) 
        print(QUrl.fromUserInput(full_url)) 

        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        self.setLayout(layout)

      #   self.container = QWidget()
      #   self.container.setLayout(layout)

      #   self.setCentralWidget(self.container)