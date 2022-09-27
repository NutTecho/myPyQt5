from PyQt5.QtCore import Qt,QAbstractTableModel , QModelIndex , QVariant
from PyQt5.QtGui import QColor,QIcon,QPixmap,QImage
from datetime import datetime
import os

tick_path = os.path.join('.\\Project1\\image\\tick.png')
cross_path = os.path.join('.\\Project1\\image\\cross.png')
tick = QImage(tick_path)
cross = QImage(cross_path)
green = QColor('green')

class TableModel(QAbstractTableModel):
    """
   :param item: list data 
   :param header: list header
    """

    def __init__(self,item,header,parent = None, *args ,**kwargs):
        super(TableModel,self).__init__(parent,*args,**kwargs)
        self._listitem = [] or item
        self._listheader = header
        self._listindex = range(1,len(item)+1)

    def data(self,index ,role):
        # set format to show data
        if role == Qt.DisplayRole:
            value = self._listitem[index.row()][index.column()]
            # Perform per-type checks and render accordingly.
            if isinstance(value, datetime):
                # Render time to YYY-MM-DD.
                return value.strftime("%Y-%m-%d")

            if isinstance(value, float):
                # Render float to 2 dp
                return "%.2f" % value

            if isinstance(value, str):
                # Render strings with quotes
                return '%s' % value

            else:
                return str(value)

        # set image decolation
        if role == Qt.DecorationRole:
            value = self._listitem[index.row()][index.column()]
            if isinstance(value, datetime):
                return QIcon('calendar.png')

            if isinstance(value, bool):
                if value:
                    return tick

                return cross

        # set row color with condition
        if role == Qt.BackgroundRole and self._listitem[index.row()][self.columnCount(index) - 1] == 'ok':
            # See below for the data structure.
            return QColor('lightgreen')

        #set text alignment
        if role == Qt.TextAlignmentRole:
            value = self._listitem[index.row()][index.column()]

            if isinstance(value, int) or isinstance(value, float):
                # Align right, vertical middle.
                return Qt.AlignVCenter + Qt.AlignRight
        
        # set text foreground
        if role == Qt.ForegroundRole:
            value = self._listitem[index.row()][index.column()]

            if (
                (isinstance(value, int) or isinstance(value, float))
                and value < 0
            ):
                return QColor('red')
        
    def rowCount(self, index):
        return len(self._listitem)

    def columnCount(self,index):
        return len(self._listitem[0])

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return QVariant(self._listheader[section])
                # return str(self.listitem.column[section])
            if orientation == Qt.Vertical:
                # return str(self.listitem.index[section])
                return QVariant(self._listindex[section])
            return QVariant()

    # def headerData(self, section, orientation, role):
    #     # section is the index of the column/row.
    #     if role == Qt.DisplayRole:
    #         if orientation == Qt.Horizontal:
    #             return str(self._listitem.columns[section])

    #         if orientation == Qt.Vertical:
    #             return str(self._listitem.index[section])