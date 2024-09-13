import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtSql import QSqlDatabase
import settings as st


class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        db = QSqlDatabase.addDatabase('QPSQL')
        db.setHostName(st.db_params['host'])
        db.setDatabaseName(st.db_params['dbname'])
        db.setPort(st.db_params['port'])
        db.setUserName(st.db_params['user'])
        db.setPassword(st.db_params['password'])
        ok = db.open()
        if ok:
            print('OK', file=sys.stderr)
        else:
            print('FAILED', file=sys.stderr)
