# -*- coding: utf-8 -*-
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QApplication,QMessageBox
import sys

class DB():
    def __init__(self,soucename="wumis",databasename="wumiszb",username="wumis",password="wumis"):
        self.__souceName=soucename
        self.__databaseName=databasename
        self.__userName=username
        self.__passWord=password
        self.__db =QSqlDatabase.addDatabase("QODBC")
        # self.__db.setHostName('192.168.1.99,2638')
        # self.__db.setPort(2638);
        self.__setUserName()
        self.__setPassWord()
        self.__setSouce()
        #self.__query()


    def __setSouce(self):
        self.__db.setDatabaseName(self.__souceName)

    def _query(self,sqlstr):
        self.__db.open()
        if self.__db.isOpen():
            query = QSqlQuery()
            query.exec(sqlstr)
            re=[]
            index=0
            while(query.next()):
                record = query.record()
                rr=[]
                for i in range(0,len(record)):
                    rr.append(record.value(i))
                re.append(rr)
            return re
        else:
            return ['error',self.__db.lastError().text()]

    def __setUserName(self):
        self.__db.setUserName(self.__userName)

    def __setPassWord(self):
        self.__db.setPassword(self.__passWord)

if __name__=='__main__':
    app = QApplication(sys.argv)
    db = DB('wumis','wumiszb','wumis','wumis')
    db._query('select * from code_list')
    sys.exit(app.exec())