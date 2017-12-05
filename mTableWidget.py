# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTableWidget,QApplication,QAbstractItemView,QTableWidgetItem
from PyQt5.QtGui import QColor,QFont
import sys


class mTableWidget(QTableWidget):
    def __init__(self,parent=None):
        super(mTableWidget,self).__init__(parent)
        # self.__header=['item_code','item_barcode','item_plu','item_name','item_unit','item_spec','sell_price','mem_price','spec_price','provider','procedure_area','bghj']
        # self._setHeader(self.__headList)

    def _setHeader(self,list_header):
        self.setColumnCount(len(list_header))
        self.setHorizontalHeaderLabels(list_header)
        self.__setHeaderBaackground()

    def _setRow(self,row=20):
        self.setRowCount(row)
    def __setHeaderBaackground(self):
        self.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}") #set background color
        self.setStyleSheet("selection-background-color:lightblue;") #set selected color
        self.setSelectionBehavior(QAbstractItemView.SelectRows) #set rows selected ,not item selected
        self.setColumnWidth(3,350)
        # for x in range(self.columnCount()):
        #     hi = self.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象
        #     hi.setStyleSheet("QHeaderView::section{background:skyblue;}")
        #     # hi.setBackground(QColor(0, 60, 10))
        # print(help(hi.setBackground))
        #     # hi.setTextColor(QColor(200,111,30))
    def _setItemValue(self,i,j,text):
        self.setItem(i,j,QTableWidgetItem(text))

if __name__=='__main__':
    h=['item_code','item_barcode','item_plu','item_name','item_unit','item_spec','sell_price','mem_price','spec_price','provider','procedure_area','bghj']
    app = QApplication(sys.argv)
    m = mTableWidget()
    m._setHeader(h)
    m.show()
    m._setRow(1)
    m._setItemValue(0,0,'asdf')
    sys.exit(app.exec())