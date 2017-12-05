# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget,QApplication,QMessageBox,QLabel,QFrame
from PyQt5.QtGui import QFont,QPixmap,QPainter
from Barcode import Barcode
from PyQt5.QtPrintSupport import QPrinterInfo, QPrinter,QPrintDialog
from PyQt5.QtCore import QRect, QPoint, QSize,Qt
import sys,os


#describe:This module is used to print
#date ：2017-12-05
#Creator:YLF

class Print(QFrame):
    def __init__(self,*args):
        super(Print,self).__init__()
        self.__args=args
        self.__oL = []  # Object list
        self.__printer = QPrinter(QPrinter.HighResolution)

        self.__createPrintmodel()


    def __openModel(self,filename):
        try:
            f=open(os.path.dirname(os.path.realpath(__file__))+'/Module/'+filename+'.txt')
            l=f.readline()
            if len(l)>0:
                return l
            else:
                QMessageBox.warning(self, "Warning", "The module file's content is missing！Please create again!",
                                    QMessageBox.Ok)
                return False
        except :
            QMessageBox.warning(self, "Warning", "The module files is missing！Please create again!",
            QMessageBox.Ok)
            return False

    def __createPrintmodel(self):
        f=self.__openModel(self.__args[0])
        if (f):
            dict=eval(f)
            for s in dict:
                # print('%s:%s' %(s,dict[s]))
                if s=='groupBox_labels': #Set label size
                    self.setGeometry(0, 0, int(dict[s]['Width']), int(dict[s]['Height']))
                if s[:5]=='label':
                    # print(dict[s])
                    label = QLabel(self)
                    label.move(int(dict[s]['X']),int(dict[s]['Y']))
                    label.setMinimumWidth(float(dict[s]['Width']))
                    label.setMaximumWidth(float(dict[s]['Width']))
                    label.setMinimumHeight(float(dict[s]['Height']))
                    label.setMaximumHeight(float(dict[s]['Height']))
                    label.setObjectName(s.split('_')[1])
                    label.setText(s.split('_')[1])
                    if 'Font' in dict[s]:
                        __fontStyle = QFont.Normal if dict[s]['Font'].split(',')[-1] == 'Regular' else QFont.Bold
                        label.setFont(QFont(dict[s]['Font'].split(',')[0],int(dict[s]['Font'].split(',')[1]),__fontStyle))

                    self.__oL.append(label)
                if s=='widget_Barcode':
                    barcode = Barcode(self)
                    barcode.setObjectName('Barcode')
                    barcode.move(int(dict[s]['X']),int(dict[s]['Y']))
                    barcode.setMinimumWidth(float(dict[s]['Width']))
                    barcode.setMaximumWidth(float(dict[s]['Width']))
                    barcode.setMinimumHeight(float(dict[s]['Height']))
                    barcode.setMaximumHeight(float(dict[s]['Height']))
                    self.__oL.append(barcode)

        else:
            return

    def _printLabel(self):
        # self.label.setText(self.__args[5]) if self.label.setObjectName=='Item_Name'else self.label.setText('')
        dialog = QPrintDialog(self.__printer, self) #choose printer
        if not dialog.exec_():
            return
        for o in self.__oL: #set value to label
            # print(o.objectName())
            if o.objectName()=='ItemCode':
                o.setText(self.__args[1])
            if o.objectName()=='Barcode':
                o.setBarcode(self.__args[2])
            if o.objectName()=='ItemBarcode':
                o.setText(self.__args[2])
            if o.objectName()=='PLU':
                o.setText(self.__args[3])
            if o.objectName()=='ItemName':
                o.setText(self.__args[4])
        # for s in self.__args:
        #     print(s)
        painter = QPainter(self.__printer)
        image = QPixmap()
        image = self.grab(QRect(QPoint(0, 0),
                                  QSize(self.size().width(),
                                        self.size().height()
                                        )
                                  )
                            )  # /* 绘制窗口至画布 */
        rect = painter.viewport()
        size = image.size()
        size.scale(rect.size(), Qt.KeepAspectRatio)
        painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
        painter.setWindow(image.rect())
        painter.drawPixmap(0, 0, image)


if __name__=='__main__':
    app = QApplication(sys.argv)
    m = Print('Normal','123456','6901028115356','10018','是宝宝')
    # m.show()
    m._printLabel()

    sys.exit(app.exec())