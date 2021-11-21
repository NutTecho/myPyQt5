import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QApplication, QLabel, QLineEdit, QMainWindow, QMenu, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        self.lb1 = QLabel()
        self.input1 = QLineEdit()
        self.input1.textChanged.connect(self.lb1.setText)

        self.btn = QPushButton("Press me")
        self.btn_is_true = True

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.input1)
        self.layout.addWidget(self.lb1)
        self.layout.addWidget(self.btn)

        self.container = QWidget()
        self.container.setLayout(self.layout)

      
        
        self.btn.setCheckable(True)
        self.btn.clicked.connect(self.wasclick)
        # self.btn.released.connect(self.wasrelease)
        self.btn.setChecked(self.btn_is_true)

        self.setCentralWidget(self.container)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

    # def contextMenuEvent(self, e):
    #     context = QMenu(self)
    #     context.addAction(QAction("test1",self))
    #     context.addAction(QAction("test2",self))
    #     context.addAction(QAction("test3",self))
    #     context.exec(e.globalPos())
    
    def on_context_menu(self,Pos):
        context = QMenu(self)
        context.addAction(QAction("test1",self))
        context.addAction(QAction("test2",self))
        context.addAction(QAction("test3",self))
        context.exec(self.mapToGlobal(Pos))



    def mouseMoveEvent(self, e):
       self.lb1.setText(str(e.globalPos()))

    def mousePressEvent(self, e):
        self.lb1.setText("mousePress")

    def mouseReleaseEvent(self, e):
        self.lb1.setText("mouseRelease")

    def clicktest(self,checked):
        if(checked):
            self.btn.setStyleSheet("background-color: rgb(125, 255, 0)")
            self.btn.setText("True")
            self.setWindowTitle("Test is true")
        else:
            self.btn.setStyleSheet("background-color: rgb(255, 0, 0)")
            self.btn.setText("False")
            self.setWindowTitle("Test is false")
            # print("hello",checked)

    def wasclick(self,checked):
        self.btn_is_true = checked
        self.clicktest(checked)
        print(self.btn_is_true)

    def wasrelease(self):
        self.btn_is_true = self.btn.isChecked()
        self.clicktest(self.btn.isChecked())
        print(self.btn_is_true)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()