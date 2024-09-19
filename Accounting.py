from PyQt6.QtWidgets import QTableView, QMessageBox, QDialog, QWidget, QAbstractScrollArea, QHeaderView
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton, QDateEdit, QComboBox, QCheckBox
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtSql import QSqlQueryModel
from PyQt6.QtCore import Qt, pyqtSlot
import settings as st
import psycopg2
from operator import itemgetter


SUPPLIE_STATUS = 'SELECT "Name", "StorageAmount" FROM products;'

ORDERS_PERIOD = '''
    SELECT "ID", "OperationType", "Dates" FROM orders WHERE "Dates" BETWEEN \'%s\' AND \'%s\'
'''

FINANSIALS_PERIOD = '''
SELECT "ID", "OperationType","TotalPrice", "Dates" FROM orders WHERE "Dates" BETWEEN \'%s\' AND date_add(\'%s\', '1 year')
'''


class Model(QSqlQueryModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.updateTable()

    def updateTable(self):
        sql = '''
            SELECT * FROM orders ORDER BY "ID" DESC;
        '''
        self.setQuery(sql)

    def showStorageStatus(self):
        self.setQuery(SUPPLIE_STATUS)

    def ordersperiod(self, start, end):
        self.setQuery(ORDERS_PERIOD % (start, end))

    def financialsperiod(self, date):
        self.setQuery(FINANSIALS_PERIOD % (date, date))


class View(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        model = Model(parent=self)
        self.setModel(model)
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)

    @pyqtSlot()
    def storage_status(self):
        self.model().showStorageStatus()

    @pyqtSlot()
    def orders_period(self):
        orders_period = Dialog_orders_period(parent=self)
        if orders_period.exec():
            self.model().ordersperiod(orders_period.start, orders_period.end)

    @pyqtSlot()
    def financials_period(self):
        financials_period = Dialog_finacnials_period(parent=self)
        if financials_period.exec():
            self.model().financialsperiod(financials_period.date)


class Dialog_orders_period(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Group ID and dates')

        start_label = QLabel('Start date', parent=self)
        self.__start_edit = QDateEdit(parent=self)

        end_label = QLabel('End date', parent=self)
        self.__end_edit = QDateEdit(parent=self)

        ok_button = QPushButton('Ok', parent=self)
        cancel_button = QPushButton('Cancel', parent=self)

        layout = QVBoxLayout(self)
        layout.addWidget(start_label)
        layout.addWidget(self.__start_edit)
        layout.addWidget(end_label)
        layout.addWidget(self.__end_edit)

        layout2 = QHBoxLayout()
        layout2.addWidget(ok_button)
        layout2.addWidget(cancel_button)

        layout.addLayout(layout2)

        cancel_button.clicked.connect(self.reject)
        ok_button.clicked.connect(self.finish)

    @pyqtSlot()
    def finish(self):
        if self.start is None or self.end is None:
            return
        self.accept()

    @property
    def start(self):
        result = self.__start_edit.date().toString("yyyy.MM.dd")
        if result == '':
            return None
        else:
            return result

    @property
    def end(self):
        result = self.__end_edit.date().toString("yyyy.MM.dd")
        if result == '':
            return None
        else:
            return result


class Dialog_finacnials_period(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Financials in year')

        date_label = QLabel('Date', parent=self)
        self.__date_edit = QDateEdit(parent=self)

        ok_button = QPushButton('Ok', parent=self)
        cancel_button = QPushButton('Cancel', parent=self)

        layout = QVBoxLayout(self)
        layout.addWidget(date_label)
        layout.addWidget(self.__date_edit)

        layout2 = QHBoxLayout()
        layout2.addWidget(ok_button)
        layout2.addWidget(cancel_button)

        layout.addLayout(layout2)

        cancel_button.clicked.connect(self.reject)
        ok_button.clicked.connect(self.finish)

    @pyqtSlot()
    def finish(self):
        if self.date is None:
            return
        self.accept()

    @property
    def date(self):
        result = self.__date_edit.date().toString("yyyy.MM.dd")
        if result == '':
            return None
        else:
            return result
