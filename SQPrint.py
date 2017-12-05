# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal 
from PyQt5.uic import loadUi
from ASADB import DB
# from mTableWidget import mTableWidget
import Set

class SQPrint(QMainWindow):
    def __init__(self,*args):
        super(SQPrint,self).__init__(*args)
        loadUi('D:/python_workspace/SQPrint/UI/main.ui',self)
        self.showMaximized()
        self.tabWidget.currentChanged.connect(self._tabpageSelect) #Connect signal and slot
        self.actionImport.triggered.connect(self._actionDataImport)
        self.actionSet.triggered.connect(self._actionSet)
        self.__labelHeadList=['item_code','item_barcode','item_plu','item_name','item_unit','item_spec','sell_price','mem_price','spec_price','provider','procedure_area',]
        self.tableWidget_Label._setHeader(self.__labelHeadList) #Set the tabWidget_label header
        self.tableWidget_Code._setHeader(self.__labelHeadList) #Set the tabWidget_label header
        # init label display content
        self.label_entert.setText="请输入"
        #signal for lienedit when the  enter  key is pressed
        self.lineEdit_Enter.returnPressed.connect(self.__enterPressed)


    def _actionSet(self):
        if self.radioButton_Normal.isChecked:
            self.__labelName='Normal'
        if self.radioButton_Special.isChecked():
            self.__labelName='Special'
        self.set=Set.PrintSet()
        self.set.show()
    
    def _actionDataImport(self):
        QMessageBox.warning(self,"Warning","恢复出厂设置将导致用户数据丢失，是否继续操作？",
                                      QMessageBox.Reset|QMessageBox.Help|QMessageBox.Cancel,QMessageBox.Reset)
    
    def _tabpageSelect(self,int): #This is a slot
        self.label_NoteMsg.setText(self.__numbers_to_strings(int))
    
    #Get name by id 
    def __numbers_to_strings(self,int): 
        switcher = {
            0: "label",
            1: "code",
            2: "Custom",
            3: "POP"
        }
                
        return switcher.get(int,'Nothing')
    def __enterPressed(self):
        sqlstr="select * from code_list"
        db=DB()
        r=db._query(sqlstr)
        if r[0]=='error':
            QMessageBox.warning(self, "DB Connect Error", r[1],
                                QMessageBox.Ok)
        else:
            rows=len(r)
            self.tableWidget_Label._setRow(rows)
            for i in range(0,rows):
                for j in range(0,len(r[i])):
                    self.tableWidget_Label._setItemValue(i,j,str(r[i][j]))
if __name__=='__main__':
    app = QApplication(sys.argv)
    sp = SQPrint()
    sp.show()
    sys.exit(app.exec())