# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication
import SQPrint

if __name__=='__main__':
    app = QApplication(sys.argv)
    sp = SQPrint.SQPrint()
    sp.show()
    sys.exit(app.exec())