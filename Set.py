# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.path.realpath(__file__))
from PyQt5.QtWidgets import QWidget,QApplication,QMessageBox,QFontDialog
from PyQt5.QtCore import QMetaObject,Qt
from PyQt5.uic import loadUi
from PyQt5.QtGui import QFont
from MoveLabel import MoveLabel
from Barcode import Barcode
import re
#describe:This module is used to set the print style
#date ：2017-11-12
#Creator:YLF

class PrintSet(QWidget):
    def __init__(self,*args):
        super(PrintSet,self).__init__(*args)
        # try :
        loadUi('D:/python_workspace/SQPrint/UI/set.ui',self)
        self.__objectdict={}
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.__fontStyle=QFont.Normal

        # except ImportError:
            # QMessageBox.warning(self,"Warning","初始化Set失败！",
                                      # QMessageBox.Ok)
        self.__object=self.findChildren(MoveLabel) #get a list for MoveLabel class
        for o in self.findChildren(Barcode):
            self.__object.append(o)#Add object barcode

        for l in self.__object:      #connect signal and solt
            # l._singal_Move.connect(self._setValue)
            l._singal_MouseRelesse.connect(self._printModule)
            l._singal_MouseRelesse.connect(self._setValue)

        self.pushButton_Save.clicked.connect(self._save) #Save button singal & solt

        self.lineEdit_W.returnPressed.connect(self._setWdith)
        self.lineEdit_H.returnPressed.connect(self._setHeight)
        self.lineEdit_X.returnPressed.connect(self._setX)
        self.lineEdit_Y.returnPressed.connect(self._setY)
        self.lineEdit_LineWidth.returnPressed.connect(self._setLineWdith)

        self.lineEdit_LabelWidth.returnPressed.connect(self._setLabelWidth)
        self.lineEdit_LabelHeight.returnPressed.connect(self._setLabelHeight)

        self.groupBox_labels.clicked.connect(self.__getGroupBoxInfo)

        self.comboBox_ChooseLabel.currentIndexChanged.connect(self.__cbxChanged)

        self.pushButton_SetFont.clicked.connect(self.__setFont)
        for f in self._getfiles():
            self.comboBox_ChooseLabel.addItem(f.split('.')[0])


    def _setLabelName(self,labelName):
        self.lineEdit_LabelName.setText(labelName)

    def _setValue(self,dict): #Put the value into lineedit
        for o in dict:
            if o=='widget_Barcode':
                self.lineEdit_ObjectName.setText(dict[o]['Name'])
                self.lineEdit_X.setText(str(dict[o]['X']))
                self.lineEdit_Y.setText(str(dict[o]['Y']))
                self.lineEdit_H.setText(str(dict[o]['Height']))
                self.lineEdit_W.setText(str(dict[o]['Width']))
                self.lineEdit_LineWidth.setText(str(dict[o]['LineWidth']))
            else:
                self.lineEdit_ObjectName.setText(dict[o]['Name'])
                self.lineEdit_X.setText(str(dict[o]['X']))
                self.lineEdit_Y.setText(str(dict[o]['Y']))
                self.lineEdit_H.setText(str(dict[o]['Height']))
                self.lineEdit_W.setText(str(dict[o]['Width']))
                self.lineEdit_LineWidth.setText('')

    def _printModule(self,dict): #Update then dict for printmodule
        # print(dict)
        for i in dict:
            if dict[i]['X'] in range(self.groupBox_labels.x(),self.groupBox_labels.x()+self.groupBox_labels.width()) \
                    and dict[i]['Y'] in range(self.groupBox_labels.y(),self.groupBox_labels.y()+self.groupBox_labels.height()):
                # self.__label={i:dict[i]}
                # print("%s:%s" % (i,dict[i]))
                dict[i]['X']=dict[i]['X']-self.groupBox_labels.x()
                dict[i]['Y'] = dict[i]['Y'] - self.groupBox_labels.y()
                self.__objectdict[i]=dict[i]
            else:
                for o in dict:
                    if dict[o]['Name'] in self.__objectdict:
                    # print(self.__objectdict)
                        del self.__objectdict[i]

    def _save(self): #Save the label to the model
        self.__objectdict['groupBox_labels']={'Width':self.groupBox_labels.width(),'Height':self.groupBox_labels.height()}
        if len(self.lineEdit_LabelName.text()) >0:
            file_object = open('Module/'+str(self.lineEdit_LabelName.text())+'.txt', 'w')
            if file_object.write(str(self.__objectdict)):
                file_object.close()
                QMessageBox.information (self, "information", "Save sucessed!",
                                    QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Warning", "Please enter label's name！",
                QMessageBox.Ok)

    def _setWdith(self):
        if len(self.lineEdit_W.text())<1 or self.lineEdit_ObjectName.text()=='':
            return
        if not self.__checkNum(self.lineEdit_W.text()):
            QMessageBox.information(self, "information", "Just can enter int or float",
                                    QMessageBox.Ok)
            return
        try:
            for o in self.__object:
                if o.objectName() == self.lineEdit_ObjectName.text():
                    o.setMinimumWidth(float(self.lineEdit_W.text()))
                    o.setMaximumWidth(float(self.lineEdit_W.text()))
                    self.__objectdict[o.objectName()]['Width']=self.lineEdit_W.text()
        except KeyError as e:
            print(e)

    def _setHeight(self): #solt
        if len(self.lineEdit_W.text())<1 or self.lineEdit_ObjectName.text()=='':
            return
        if not self.__checkNum(self.lineEdit_H.text()):
            QMessageBox.information(self, "information", "Just can enter int or float",
                                    QMessageBox.Ok)
        try:
            for o in self.__object:
                if o.objectName() == self.lineEdit_ObjectName.text():
                    o.setMinimumHeight(float(self.lineEdit_H.text()))
                    o.setMaximumHeight(float(self.lineEdit_H.text()))
                    self.__objectdict[o.objectName()]['Height']=self.lineEdit_H.text()
        except KeyError as e:
            print(e)

    def _setX(self): #solt
        if len(self.lineEdit_W.text())<1 or self.lineEdit_ObjectName.text()=='':
            return
        if not self.__checkNum(self.lineEdit_W.text()):
            QMessageBox.information(self, "information", "Just can enter int or float",
                                    QMessageBox.Ok)
        try:
            for o in self.__object:
                if o.objectName() == self.lineEdit_ObjectName.text():
                    o.move(int(self.lineEdit_X.text())+self.groupBox_labels.x(),o.y())
                    self.__objectdict[o.objectName()]['X']=self.lineEdit_X.text()
        except KeyError as e:
            print(e)

    def _setY(self): #solt
        if len(self.lineEdit_W.text())<1 or self.lineEdit_ObjectName.text()=='':
            return
        if not self.__checkNum(self.lineEdit_W.text()):
            QMessageBox.information(self, "information", "Just can enter int or float",
                                    QMessageBox.Ok)
        try:
            for o in self.__object:
                if o.objectName() == self.lineEdit_ObjectName.text():
                    o.move(o.x(),int(self.lineEdit_Y.text())+self.groupBox_labels.y())
                    self.__objectdict[o.objectName()]['Y']=self.lineEdit_Y.text()
        except KeyError as e:
            print(e)

    def _setLineWdith(self): #solt
        if not self.__checkNum(self.lineEdit_W.text()):
            QMessageBox.information(self, "information", "Just can enter int or float",
                                    QMessageBox.Ok)
        try:
            for o in self.__object:
                if o.objectName() == 'widget_Barcode':
                    o._setLineWidth(float(self.lineEdit_LineWidth.text()))
                    self.__objectdict[o.objectName()]['LineWidth']=self.lineEdit_LineWidth.text()

        except KeyError as e:
            print(e)

    def _getfiles(self): #Gets the file name of the print label
        return os.listdir(os.path.dirname(os.path.realpath(__file__))+'/Module/')

    def _openFilesLabel(self,filename): #When you open the set moduel, move each object to the correct location
        try:
            f=open(os.path.dirname(os.path.realpath(__file__))+'/Module/'+filename)
        except :
            QMessageBox.warning(self, "Warning", "The module files is missing！Please create again!",
            QMessageBox.Ok)
            return
        l=f.readline()
        if len(l)>0:
            self.__objectdict=eval(l)
        else:
            QMessageBox.warning(self, "Warning", "The module files is missing！Please create again!",
            QMessageBox.Ok)
            return
        for i in self.__objectdict:
            for j in self.__object:
                if j.objectName() == i:
                    # print(i)
                    j.move(self.__objectdict[i]['X']+self.groupBox_labels.x(),self.__objectdict[i]['Y']+self.groupBox_labels.y())
                    j.setMinimumWidth(int(self.__objectdict[i]['Width']))
                    j.setMaximumWidth(int(self.__objectdict[i]['Width']))

                    if 'Font' in self.__objectdict[i]:   #set font
                        self.__fontStyle=QFont.Normal if  self.__objectdict[i]['Font'].split(',')[-1] =='Regular'  else QFont.Bold
                        j.setFont(QFont(self.__objectdict[i]['Font'].split(',')[0],int(self.__objectdict[i]['Font'].split(',')[1]),self.__fontStyle))
                    if j.objectName()=='widget_Barcode':
                        j._setLineWidth(float(self.__objectdict[i]['LineWidth']))

    def __checkNum(self,input): #Check an input is int or float or not
        __int_float=re.compile(r'^[0-9]*\.?[0-9]*$')
        return __int_float.match(input)

    def __getGroupBoxInfo(self):
        print('click')
        self.lineEdit_ObjectName.setText(self.groupBox_labels.ObjectName())
        self.lineEdit_X.setText(str(self.groupBox_labels.x()))
        self.lineEdit_Y.setText(str(self.groupBox_labels.y()))
        self.lineEdit_H.setText(str(self.groupBox_labels.height()))
        self.lineEdit_W.setText(str(self.groupBox_labels.width()))

    def _setLabelWidth(self): #Set label width
        if not self.__checkNum(self.lineEdit_LabelWidth.text()):
            QMessageBox.information(self, "information", "Just can enter int or float",
                                    QMessageBox.Ok)
        self.groupBox_labels.setMinimumWidth(float(self.lineEdit_LabelWidth.text()))
        self.groupBox_labels.setMaximumWidth(float(self.lineEdit_LabelWidth.text()))

    def _setLabelHeight(self): #Set label height
        if not self.__checkNum(self.lineEdit_LabelHeight.text()):
            QMessageBox.information(self, "information", "Just can enter int or float",
                                    QMessageBox.Ok)
        self.groupBox_labels.setMinimumHeight(float(self.lineEdit_LabelHeight.text()))
        self.groupBox_labels.setMaximumHeight(float(self.lineEdit_LabelHeight.text()))

    def __cbxChanged(self): #A solt for dorpdownlistbox changed
        self._openFilesLabel(self.comboBox_ChooseLabel.currentText() + '.txt')
        self._setLabelName(self.comboBox_ChooseLabel.currentText())  # Set the name of the label you chose

    def __setFont(self):
        font, succeed = QFontDialog.getFont()
        if succeed:
            for o in self.__object:
                if o.objectName() == self.lineEdit_ObjectName.text():
                    o.setFont(font)
                    self.__objectdict[o.objectName()]['Font']=font.key()
        # self.label_font.setFont(font)

if __name__=='__main__':
    app = QApplication(sys.argv)
    ps = PrintSet()
    ps.show()
    sys.exit(app.exec())