from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QWidget,QVBoxLayout



class MplWidget(QWidget):
    def __init__(self, parent=None):
        super(MplWidget, self).__init__()
        # fig = Figure(figsize=(5,4),dpi = 100)
        # self.axes = fig.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(Figure())
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.toolbar = NavigationToolbar(self.canvas,parent=None)
        vert_layout = QVBoxLayout()
        vert_layout.addWidget(self.toolbar)
        vert_layout.addWidget(self.canvas)
       
       
        self.setLayout(vert_layout)

        # super(MplWidget,self).__init__(fig)