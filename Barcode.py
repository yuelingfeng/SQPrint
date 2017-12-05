# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QObject, Qt, pyqtSignal,QPoint
from PyQt5.QtGui import QPainter, QFont, QColor, QPen

class Barcode(QWidget):
    # _singal_Move=pyqtSignal(dict)
    _singal_MouseRelesse = pyqtSignal(dict)
    def __init__(self,parent=None): #lineWidth=2,lineHeight=80
        super(Barcode,self).__init__(parent)
        self.setStyleSheet("border:1px;border-style:solid;border-color:black")
        self.__SMECode=['101','01010','101'] #Start char,mid char,end char
        self.__logicEAN13=['AAAAAA','AABABB','AABBAB','ABAABB','ABBAAB','ABBBAA','ABABAB','ABABBA','ABBABA']
        self.__numLeftCodeAEAN13=['0001101','0011001','0010011','0111101','0100011','0110001','0101111','0111011','0110111','0001011']
        self.__numLeftCodeBEAN13=['0100111','0110011','0011011','0100001','0011101','0111001','0000101','0010001','0001001','0010111']
        self.__numRightCodeEAN13=['1110010','1100110','1101100','1000010','1011100','1001110','1010000','1000100','1001000','1110100']
        self.__lineWidth=1.1
        self.__lineHeight=40
        self.__barcode='6901028045902'
        self.setGeometry(300, 300, 240, 100)
        self._x = 0
        self._y = 0
        self._OrginX = 0
        self._OrginY = 0
        self._disX = 0
        self._disY = 0
        self._point=QPoint(0,0)
        self._info={}
        self._size={}
        self._setWidth()
        self._setHeight()


    def paintEvent(self, e):
        qp =QPainter(self)
        qp.begin(self)
        if len(self.__barcode)==13:
            self.__drawLines(e,qp,self.__Ean13(self.__barcode))
            self.__drawText(e,qp,self.__barcode)
        else:
            self.__drawLines(e,qp,self.__Ean8(self.__barcode))
            self.__drawText(e,qp,self.__barcode)
        qp.end()

    def setBarcode(self,barcode):
        self.__barcode=barcode
        self.update()

    def _setWidth(self):
        self.setMaximumWidth(self.__lineWidth * 110)
        self.setMinimumWidth(self.__lineWidth * 110)
        self.update()

    def _setHeight(self):
        self.setMaximumHeight(self.__lineHeight+15)
        self.setMinimumHeight(self.__lineHeight + 15)
        self.update()

    def _getLineWidth(self):
        return self.__lineWidth

    def _setLineWidth(self,lineWidth):
        self.__lineWidth=lineWidth
        self._setWidth()

    def __drawLines(self,e,qp,num):
        lineIndex=0 #the line index
        penBlack = QPen(QColor(0,0,0), self.__lineWidth)
        penWidth = QPen(QColor(255,255,255), self.__lineWidth )
        if len(self.__barcode)==13: #EAN13
            for c in num:
                # print(lineIndex)
                if (lineIndex <3)  or (lineIndex>91) or (lineIndex>44 and lineIndex <50):
                    lHeight=self.__lineHeight+10
                else:
                    lHeight=self.__lineHeight
                if c =='1':
                    qp.setPen(penBlack)
                    qp.drawLine(self.__lineWidth*11+(lineIndex+1)*self.__lineWidth,0,self.__lineWidth*11+(lineIndex+1)*self.__lineWidth,lHeight)
                else:
                    qp.setPen(penWidth)
                    qp.drawLine(self.__lineWidth*11 + (lineIndex+1)*self.__lineWidth, 0, self.__lineWidth*11 + (lineIndex+1)*self.__lineWidth, lHeight)
                lineIndex=lineIndex+1
        else: #EAN8
            for c in num:
                if (lineIndex <3)  or (lineIndex>63) or (lineIndex>31 and lineIndex <36):
                    lHeight=self.__lineHeight+10
                else:
                    lHeight=self.__lineHeight
                if c =='1':
                    qp.setPen(penBlack)
                    qp.drawLine(self.__lineWidth*11+(lineIndex+1)*self.__lineWidth,0,self.__lineWidth*11+(lineIndex+1)*self.__lineWidth,lHeight)
                else:
                    qp.setPen(penWidth)
                    qp.drawLine(self.__lineWidth*11 + (lineIndex+1)*self.__lineWidth, 0, self.__lineWidth*11 + (lineIndex+1)*self.__lineWidth, lHeight)
                lineIndex=lineIndex+1

    def __drawText(self,e,qp,b):
        if len(b)==13:
            x=5*self.__lineWidth
            for i in range(0,len(b)):
                qp.drawText(x,self.__lineHeight+13,b[i])
                if i ==0  :
                    x = x + self.__lineWidth * 13
                elif i == 6:
                    x=x+self.__lineWidth*18
                else:
                    x =x +self.__lineWidth*6
        else:
            x=16*self.__lineWidth
            for i in range(0,len(b)):
                qp.drawText(x,self.__lineHeight+13,b[i])
                if i ==0  :
                    x = x + self.__lineWidth*7
                elif i == 3:
                    x=x+self.__lineWidth*12
                else:
                    x =x +self.__lineWidth*7

    def __Ean13(self,b):
        rec = self.__SMECode[0] # Add start char
        logicValue=self.__logicEAN13[int(b[0])-1]
        for i in range(1,7): #left barcode
            if logicValue[i-1]=='A':
                rec = rec + self.__numLeftCodeAEAN13[int(b[i])]
            else:
                rec = rec + self.__numLeftCodeBEAN13[int(b[i])]
        rec = rec +self.__SMECode[1] # Add middle char

        for  i in range(7,len(b)):
            rec = rec + self.__numRightCodeEAN13[int(b[i])]
        rec=rec+self.__SMECode[2]
        return rec

    def __Ean8(self,b):
        rec = self.__SMECode[0] # Add start char
        # logicValue=self.__logicEAN13[int(b[0])-1] #The Ean8 encoding rules are the same as Ean13
        for i in range(0,4): #left barcode
                rec = rec + self.__numLeftCodeAEAN13[int(b[i])]
        rec = rec +self.__SMECode[1] # Add middle char

        for  i in range(4,len(b)):
            rec = rec + self.__numRightCodeEAN13[int(b[i])]
        rec=rec+self.__SMECode[2]
        print(rec)
        return rec

    def mouseMoveEvent(self, event):
        self._point = self.pos()
        self._x = event.x()
        self._y = event.y()
        self._disX = self._x - self._OrginX
        self._disY = self._y - self._OrginY
        self.move(self._point.x() + self._disX, self._point.y() + self._disY)

    def mousePressEvent(self, event):
        self._OrginX = event.x()
        self._OrginY = event.y()

    # def mouseDoubleClickEvent(self, *args, **kwargs):
    #     self._info['Name'] = self.objectName()
    #     self._info['X'] = self.x()
    #     self._info['Y'] = self.y()
    #     self._info['Height'] = self.height()
    #     self._info['Width'] = self.width()
    #     self._singal_Move.emit(self._info)

    def mouseReleaseEvent(self, event):
        self._info['Name'] = self.objectName()
        self._info['X'] = self.x()
        self._info['Y'] = self.y()
        self._info['Height'] = self.height()
        self._info['Width'] = self.width()
        self._info['LineWidth']=self._getLineWidth()
        self._size[self.objectName()] = self._info
        self._singal_MouseRelesse.emit(self._size)

if __name__=='__main__':
    app = QApplication(sys.argv)
    barcode = Barcode()
    barcode.setBarcode('12345670')
    # barcode.setBarcode('6901028045902')
    barcode._setLineWidth(1.1)
    barcode.show()
    sys.exit(app.exec())