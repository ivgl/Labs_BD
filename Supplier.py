from PyQt6.QtWidgets import QTableView, QMessageBox, QDialog, QWidget, QAbstractScrollArea, QHeaderView
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtSql import QSqlQueryModel
from PyQt6.QtCore import pyqtSlot
import settings as st
import psycopg2
from operator import itemgetter


INSERT = 'INSERT INTO suppliers ("Name") VALUES (%s);'

SELECT_ONE = 'SELECT "Name" FROM suppliers WHERE "ID" = %s;'

UPDATE = 'UPDATE suppliers SET "Name" = %s WHERE "ID" = %s'

DELETE = '''
    DELETE FROM products_suppliers WHERE "SupplierID" = %s;
    DELETE FROM suppliers WHERE "ID" = %s;
'''


class Model(QSqlQueryModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.updateTable()

    def updateTable(self):
        sql = '''
			SELECT * FROM suppliers ORDER BY "ID" DESC;
        '''
        self.setQuery(sql)

    def add(self, name):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(INSERT, (name,))
        conn.commit()
        conn.close()
        self.updateTable()

    def update(self, supplierID, name):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(UPDATE, (name, supplierID))
        conn.commit()
        conn.close()
        self.updateTable()

    def delete(self, supplierID):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(DELETE, (supplierID, supplierID))
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
            if dialog.is_supplier_new(dialog.name):
                self.model().add(dialog.name)

    @pyqtSlot()
    def update(self):
        dialog = Dialog(parent=self)
        row = self.currentIndex().row()
        supplierID = self.model().record(row).value(0)
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(SELECT_ONE, (supplierID,))
        (dialog.name,) = cursor.fetchone()
        dialog.name = dialog.name.strip()
        conn.close()
        if dialog.exec():
            self.model().update(supplierID, dialog.name)

    @pyqtSlot()
    def delete(self):
        row = self.currentIndex().row()
        supplierID = self.model().record(row).value(0)
        ans = QMessageBox.question(self, 'Delete supplier', 'Are you sure?')
        if ans == QMessageBox.StandardButton.Yes:
            self.model().delete(supplierID)


class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Suppliers')

        name_label = QLabel('Name', parent=self)
        self.__name_edit = QLineEdit(parent=self)

        ok_button = QPushButton('Ok', parent=self)
        cancel_button = QPushButton('Cancel', parent=self)

        layout = QVBoxLayout(self)
        layout.addWidget(name_label)
        layout.addWidget(self.__name_edit)

        layout2 = QHBoxLayout()
        layout2.addWidget(ok_button)
        layout2.addWidget(cancel_button)

        layout.addLayout(layout2)

        cancel_button.clicked.connect(self.reject)
        ok_button.clicked.connect(self.finish)

    def is_supplier_new(self, name):
        conn = psycopg2.connect(**st.db_params)
        q = conn.cursor()
        q.execute('SELECT DISTINCT "Name" FROM suppliers')
        ListS = q.fetchall()
        ListS = list(map(itemgetter(0), ListS))
        ListS = list(map(str, ListS))
        ListS = list(map(str.strip, ListS))
        conn.commit()
        conn.close()
        if name in ListS:
            return False
        else:
            return True

    @pyqtSlot()
    def finish(self):
        if self.name is None:
            return
        self.accept()

    @property
    def name(self):
        result = self.__name_edit.text().strip()
        if result == '':
            return None
        else:
            return result

    @name.setter
    def name(self, value):
        self.__name_edit.setText(value)
