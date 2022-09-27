from PyQt5.QtWidgets import QApplication
from main_widget import MainWindow
import sys
import os



def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('closing window')

if __name__ == '__main__':
    main()
    
