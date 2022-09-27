from PyQt5.QtCore import Qt,QAbstractListModel , QModelIndex
from PyQt5.QtGui import QColor,QIcon,QPixmap,QImage
from datetime import datetime
import os

tick_path = os.path.join(os.getcwd(),"Project1","image","tick.png")
cross_path = os.path.join(os.getcwd(),"Project1","image","cross.png")
tick = QImage(tick_path)
cross = QImage(cross_path)
green = QColor('green')

class ListModel(QAbstractListModel):
    """
    :param item: list data 
    """

    def __init__(self,item = None ,*args ,**kwargs):
        super(ListModel,self).__init__(*args,**kwargs)
        self._listitem = item or []

    def data(self,index ,role):
        if role == Qt.DisplayRole:
            _,text = self._listitem[index.row()]
            return text

        if role == Qt.DecorationRole:
            status,_ = self._listitem[index.row()]
            if status:
                return tick
            return cross

    def rowCount(self, index):
        return len(self._listitem)

