from PyQt6.QtWidgets import QTableView, QMessageBox, QDialog, QWidget, QAbstractScrollArea, QHeaderView
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtSql import QSqlQueryModel
from PyQt6.QtCore import pyqtSlot
import settings as st
import psycopg2
from operator import itemgetter


INSERT = '''
    INSERT INTO products ("Name") VALUES (%s);
    INSERT INTO price ("ProductID", "Price") VALUES ((SELECT "ID" FROM products ORDER BY "ID" DESC LIMIT 1), (%s));
    INSERT INTO return_possibility ("ProductID", "ReturnPossibility") VALUES ((SELECT "ID" FROM products ORDER BY "ID" DESC LIMIT 1), (%s));
    INSERT INTO storage_supplies ("ProductID", "Amount") VALUES ((SELECT "ID" FROM products ORDER BY "ID" DESC LIMIT 1), (%s));
    INSERT INTO products_suppliers ("SupplierID", "ProductID", "Price", "DiscountMinAmount", "DiscountPercentage") VALUES ((SELECT "ID" FROM suppliers WHERE "Name" = %s), (SELECT "ID" FROM products ORDER BY "ID" DESC LIMIT 1), (%s), (%s), (%s));
'''

SELECT_ONE = 'SELECT "Name" FROM products WHERE "ID" = %s;'

UPDATE = 'UPDATE products SET "Name" = %s WHERE "ID" = %s'

DELETE = '''
    DELETE FROM price WHERE "ProductID" = %s;
    DELETE FROM return_possibility WHERE "ProductID" = %s;
    DELETE FROM storage_supplies WHERE "ProductID"= %s;
    DELETE FROM products_suppliers WHERE "ProductID" = %s;
    DELETE FROM "orderItems" WHERE "ProductID" = %s;
    DELETE FROM products WHERE "ID" = %s;
'''


class Model(QSqlQueryModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.updateTable()

    def updateTable(self):
        sql = '''
            SELECT "ID", "Name" FROM products ORDER BY "ID" DESC;
        '''
        self.setQuery(sql)

    def add(self, name, customerprice, returnpossibility, storageamount, supplier, supplierprice, discountamount, discountpercentage):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(INSERT, (name, customerprice, returnpossibility,
                       storageamount, supplier, supplierprice, discountamount, discountpercentage))
        conn.commit()
        conn.close()
        self.updateTable()

    def update(self, productID, name):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(UPDATE, (name, productID))
        conn.commit()
        conn.close()
        self.updateTable()

    def delete(self, productID):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(DELETE, (productID, productID, productID,
                       productID, productID, productID))
        conn.commit()
        conn.close()
        self.updateTable()


class View(QTableView):
    def __init__(self, parent: None):
        super().__init__(parent)
        model = Model(parent=self)
        self.setModel(model)
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)

    @ pyqtSlot()
    def add(self):
        dialog = Dialog(parent=self)
        if dialog.exec():
            self.model().add(dialog.name, dialog.customerprice, dialog.returnpossibility,
                             dialog.storageamount, dialog.supplier, dialog.supplierprice, dialog.discountamount, dialog.discountpercentage)

    @pyqtSlot()
    def update(self):
        dialog = Dialog(parent=self)
        row = self.currentIndex().row()
        productID = self.model().record(row).value(0)
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(SELECT_ONE, (productID,))
        (dialog.name,) = cursor.fetchone()
        dialog.name = dialog.name.strip()
        conn.close()
        if dialog.exec():
            self.model().update(productID, dialog.name)

    @pyqtSlot()
    def delete(self):
        row = self.currentIndex().row()
        productID = self.model().record(row).value(0)
        ans = QMessageBox.question(self, 'Delete product', 'Are you sure?')
        if ans == QMessageBox.StandardButton.Yes:
            self.model().delete(productID)


class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Product')

        name_label = QLabel('Name', parent=self)
        self.__name_edit = QLineEdit(parent=self)

        customerprice_label = QLabel('Customer Price', parent=self)
        self.__customerprice_edit = QLineEdit(parent=self)

        returnpossibility_label = QLabel('Return Possibility', parent=self)
        self.__returnpossibility_edit = QLineEdit(parent=self)

        storageamount_label = QLabel('Storage Amount', parent=self)
        self.__storageamount_edit = QLineEdit(parent=self)

        supplier_label = QLabel('Supplier Name', parent=self)
        self.__supplier_choose = QComboBox(parent=self)
        self.__supplier_choose.addItems(self.get_supplier_list())

        supplierprice_label = QLabel('Supplier Price', parent=self)
        self.__supplierprice_edit = QLineEdit(parent=self)

        discountamount_label = QLabel(
            'Amount when discount is starting', parent=self)
        self.__discountamount_edit = QLineEdit(parent=self)

        discountpercentage_label = QLabel('Discount Percentage', parent=self)
        self.__discountpercentage_edit = QLineEdit(parent=self)

        ok_button = QPushButton('Ok', parent=self)
        cancel_button = QPushButton('Cancel', parent=self)

        layout = QVBoxLayout(self)
        layout.addWidget(name_label)
        layout.addWidget(self.__name_edit)
        layout.addWidget(customerprice_label)
        layout.addWidget(self.__customerprice_edit)
        layout.addWidget(returnpossibility_label)
        layout.addWidget(self.__returnpossibility_edit)
        layout.addWidget(storageamount_label)
        layout.addWidget(self.__storageamount_edit)
        layout.addWidget(supplier_label)
        layout.addWidget(self.__supplier_choose)
        layout.addWidget(supplierprice_label)
        layout.addWidget(self.__supplierprice_edit)
        layout.addWidget(discountamount_label)
        layout.addWidget(self.__discountamount_edit)
        layout.addWidget(discountpercentage_label)
        layout.addWidget(self.__discountpercentage_edit)

        layout2 = QHBoxLayout()
        layout2.addWidget(ok_button)
        layout2.addWidget(cancel_button)

        layout.addLayout(layout2)

        cancel_button.clicked.connect(self.reject)
        ok_button.clicked.connect(self.finish)

    def get_supplier_list(self):
        conn = psycopg2.connect(**st.db_params)
        q = conn.cursor()
        q.execute('SELECT DISTINCT "Name" FROM suppliers')
        ListS = q.fetchall()
        ListS = list(map(itemgetter(0), ListS))
        ListS = list(map(str, ListS))
        ListS = list(map(str.strip, ListS))
        conn.commit()
        conn.close()
        return ListS

    @ pyqtSlot()
    def finish(self):
        if self.name is None:
            return
        self.accept()

    @ property
    def name(self):
        result = self.__name_edit.text().strip()
        if result == '':
            return None
        else:
            return result

    @ property
    def customerprice(self):
        return str(self.__customerprice_edit.text()).strip()

    @ property
    def returnpossibility(self):
        return str(self.__returnpossibility_edit.text()).strip()

    @ property
    def storageamount(self):
        return str(self.__storageamount_edit.text()).strip()

    @ property
    def supplier(self):
        return str(self.__supplier_choose.currentText()).strip()

    @ property
    def supplierprice(self):
        return str(self.__customerprice_edit.text()).strip()

    @ property
    def discountamount(self):
        return str(self.__discountamount_edit.text()).strip()

    @ property
    def discountpercentage(self):
        return str(self.__discountpercentage_edit.text()).strip()

    @ name.setter
    def name(self, value):
        self.__name_edit.setText(value)
