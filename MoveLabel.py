# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QPoint,pyqtSignal, QMetaObject
from PyQt5.QtGui import QFont

class MoveLabel(QLabel):
    #signals
    # _singal_Move=pyqtSignal(dict)
    _singal_MouseRelesse = pyqtSignal(dict)
    def __init__(self, parent=None):
        super(MoveLabel, self).__init__(parent)
        self.setStyleSheet("border:1px;border-style:solid;border-color:black")
        self._x = 0
        self._y = 0
        self._OrginX = 0
        self._OrginY = 0
        self._disX = 0
        self._disY = 0
        self._point=QPoint(0,0)
        self.__info={}
        self.__Size={}
        self.__font=QFont

    def mouseMoveEvent(self, event):
        self._point = self.pos()
        self._x = event.x()
        self._y = event.y()
        self._disX = self._x - self._OrginX
        self._disY = self._y - self._OrginY
        self.move(self._point.x()+self._disX,self._point.y()+self._disY)

    def mousePressEvent(self, event):
        self._OrginX = event.x()
        self._OrginY = event.y()

    # def mouseDoubleClickEvent(self, *args, **kwargs):
    #     self.__info['Name']=self.objectName()
    #     self.__info['X']=self.x()
    #     self.__info['Y']=self.y()
    #     self.__info['Height']=self.height()
    #     self.__info['Width']=self.width()
    #     self._singal_Move.emit(self.__info)

    def mouseReleaseEvent(self, event):
        self.__info['Name'] = self.objectName()
        self.__info['X']=self.x()
        self.__info['Y']=self.y()
        self.__info['Height']=self.height()
        self.__info['Width']=self.width()
        self.__font = self.font()
        self.__info['Font']=self.__font.key()
        self.__Size[self.objectName()]=self.__info
        self._singal_MouseRelesse.emit(self.__Size)


