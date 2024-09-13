from PyQt6.QtWidgets import QTableView, QMessageBox, QDialog, QWidget, QAbstractScrollArea, QHeaderView
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtSql import QSqlQueryModel
from PyQt6.QtCore import pyqtSlot
import settings as st
import psycopg2
from operator import itemgetter

INSERTORDERS = '''
INSERT INTO orders ("TotalPrice", "Dates", "OperationTypeID") VALUES ((%s), (%s), (SELECT "ID" FROM operation_types WHERE "Name" = %s));
INSERT INTO financials ("Balance","OrderID") VALUES ((SELECT "Balance" FROM financials ORDER BY "ID" DESC LIMIT 1), (SELECT "ID" FROM orders ORDER BY "ID" DESC LIMIT 1))
'''

INSERTITEMS = '''
INSERT INTO "orderItems" ("OrderID", "ProductID", "Amount") VALUES ((SELECT "ID" FROM orders ORDER BY "ID" DESC LIMIT 1), (SELECT "ID" FROM products WHERE "Name" = %s), (%s));
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

    def add(self, totalprice, dates, operationtype, numberof):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(INSERTORDERS, (totalprice, dates, operationtype))
        conn.commit()
        conn.close()
        self.updateTable()

    def additem(self, productid, amount):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(INSERTITEMS, (productid, amount))
        conn.commit()
        conn.close()
        self.updateTable()


class View(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        model = Model(parent=self)
        self.setModel(model)
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)

    @pyqtSlot()
    def add(self):
        dialog = Dialog(parent=self)
        if dialog.exec():
            self.model().add(dialog.totalprice, dialog.dates,
                             dialog.operationtype, dialog.numberof)
            for i in range(0, int(dialog.numberof)):
                dialogitems = DialogItems(parent=self)
                if dialogitems.exec():
                    self.model().additem(dialogitems.productid, dialogitems.amount)


class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Orders')

        totalprice_label = QLabel('TotalPrice', parent=self)
        self.__totalprice_edit = QLineEdit(parent=self)

        dates_label = QLabel('Dates', parent=self)
        self.__dates_edit = QLineEdit(parent=self)

        operationtype_label = QLabel('Operation type', parent=self)
        self.__operationtype_choose = QComboBox(parent=self)
        self.__operationtype_choose.addItems(self.get_operationtype_list())

        numberof_label = QLabel('Number of', parent=self)
        self.__numberof_edit = QLineEdit(parent=self)

        ok_button = QPushButton('Ok', parent=self)
        cancel_button = QPushButton('Cancel', parent=self)

        layout = QVBoxLayout(self)
        layout.addWidget(totalprice_label)
        layout.addWidget(self.__totalprice_edit)
        layout.addWidget(dates_label)
        layout.addWidget(self.__dates_edit)
        layout.addWidget(operationtype_label)
        layout.addWidget(self.__operationtype_choose)
        layout.addWidget(numberof_label)
        layout.addWidget(self.__numberof_edit)

        layout2 = QHBoxLayout()
        layout2.addWidget(ok_button)
        layout2.addWidget(cancel_button)

        layout.addLayout(layout2)

        cancel_button.clicked.connect(self.reject)
        ok_button.clicked.connect(self.finish)

    def get_operationtype_list(self):
        conn = psycopg2.connect(**st.db_params)
        q = conn.cursor()
        q.execute('SELECT DISTINCT "Name" FROM operation_types')
        ListS = q.fetchall()
        ListS = list(map(itemgetter(0), ListS))
        ListS = list(map(str, ListS))
        ListS = list(map(str.strip, ListS))
        conn.commit()
        conn.close()
        return ListS

    @pyqtSlot()
    def finish(self):
        if self.totalprice is None:
            return
        self.accept()

    @property
    def totalprice(self):
        result = self.__totalprice_edit.text().strip()
        if result == '':
            return None
        else:
            return result

    @property
    def dates(self):
        return str(self.__dates_edit.text()).strip()

    @property
    def numberof(self):
        return str(self.__numberof_edit.text()).strip()

    @property
    def operationtype(self):
        return str(self.__operationtype_choose.currentText()).strip()

    @totalprice.setter
    def totalprice(self, value):
        self.__totalprice_edit.setText(value)


class DialogItems(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Order items')

        productid_label = QLabel('Product', parent=self)
        self.__productid_choose = QComboBox(parent=self)
        self.__productid_choose.addItems(self.get_product_list())

        amount_label = QLabel('Amount', parent=self)
        self.__amount_edit = QLineEdit(parent=self)

        ok_button = QPushButton('Ok', parent=self)
        cancel_button = QPushButton('Cancel', parent=self)

        layout = QVBoxLayout(self)
        layout.addWidget(productid_label)
        layout.addWidget(self.__productid_choose)
        layout.addWidget(amount_label)
        layout.addWidget(self.__amount_edit)

        layout2 = QHBoxLayout()
        layout2.addWidget(ok_button)
        layout2.addWidget(cancel_button)

        layout.addLayout(layout2)

        cancel_button.clicked.connect(self.reject)
        ok_button.clicked.connect(self.finish)

    def get_product_list(self):
        conn = psycopg2.connect(**st.db_params)
        q = conn.cursor()
        q.execute('SELECT DISTINCT "Name" FROM products')
        ListS = q.fetchall()
        ListS = list(map(itemgetter(0), ListS))
        ListS = list(map(str, ListS))
        ListS = list(map(str.strip, ListS))
        conn.commit()
        conn.close()
        return ListS

    @pyqtSlot()
    def finish(self):
        if self.productid is None:
            return
        self.accept()

    @property
    def productid(self):
        result = self.__productid_choose.currentText().strip()
        if result == '':
            return None
        else:
            return result

    @property
    def amount(self):
        return str(self.__amount_edit.text()).strip()

    @productid.setter
    def productid(self, value):
        self.__productid_choose.setText(value)
