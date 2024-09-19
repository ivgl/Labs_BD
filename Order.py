from PyQt6.QtWidgets import QTableView, QMessageBox, QDialog, QWidget, QAbstractScrollArea, QHeaderView
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtSql import QSqlQueryModel
from PyQt6.QtCore import pyqtSlot
import settings as st
import psycopg2
from operator import itemgetter

INSERT_RETURN_ORDER = '''
INSERT INTO orders ("TotalPrice", "Dates", "OperationType") VALUES ((0), (%s), ('Return'));
'''

INSERT_SUPPLIER_ORDER = '''
INSERT INTO orders ("TotalPrice", "Dates", "OperationType") VALUES ((0), (%s), ('Purchasing'));
'''

INSERT_CUSTOMER_ORDER = '''
INSERT INTO orders ("TotalPrice", "Dates", "OperationType") VALUES ((0), (%s), ('Sell'));
'''

INSERTITEMS = '''
INSERT INTO "orderItems" ("OrderID", "ProductID", "Amount") VALUES ((SELECT "ID" FROM orders ORDER BY "ID" DESC LIMIT 1), (SELECT "ID" FROM products WHERE "Name" = %s), (%s));
'''

DELETE = '''
    DELETE FROM "orderItems" WHERE "OrderID" = (SELECT "ID" FROM orders ORDER BY "ID" DESC LIMIT 1);
    DELETE FROM orders WHERE "ID" = (SELECT "ID" FROM orders ORDER BY "ID" DESC LIMIT 1);
'''

RETURN_STATUS = '''
    SELECT "ReturnPossibility" FROM products WHERE "ID" = (SELECT "ID" FROM products WHERE "Name" = %s);
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

    def delete(self):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(DELETE)
        conn.commit()
        conn.close()
        self.updateTable()

    def returnstatus(self, productid):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(RETURN_STATUS, (productid,))
        returnstatus = cursor.fetchmany()
        conn.commit()
        conn.close()
        if returnstatus[0][0]:
            return True
        else:
            return False

    # def add(self, dates, operationtype):
    #    conn = psycopg2.connect(**st.db_params)
    #    cursor = conn.cursor()
    #    cursor.execute(INSERTORDERS, (dates, operationtype))
    #    conn.commit()
    #    conn.close()
    #    self.updateTable()

    def addreturnorder(self, dates):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(INSERT_RETURN_ORDER, (dates,))
        conn.commit()
        conn.close()
        self.updateTable()

    def addsupplierorder(self, dates):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(INSERT_SUPPLIER_ORDER, (dates,))
        conn.commit()
        conn.close()
        self.updateTable()

    def addcustomerorder(self, dates):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(INSERT_CUSTOMER_ORDER, (dates,))
        conn.commit()
        conn.close()
        self.updateTable()

    def updatetotalprice(self, totalprice):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE orders SET "TotalPrice" = %s WHERE "ID" = (SELECT "ID" FROM orders ORDER BY "ID" DESC LIMIT 1)', (totalprice,))
        conn.commit()
        conn.close()
        self.updateTable()

    def updatebalance(self, balance):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE financials SET "Balance" = %s WHERE "ID" = (SELECT "ID" FROM financials ORDER BY "ID" DESC LIMIT 1)', (balance,))
        conn.commit()
        conn.close()
        self.updateTable()

    def updatestorageamount(self, numberof):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT "ID", "ProductID", "Amount"
                       FROM "orderItems"
                       GROUP BY "ID", "ProductID", "Amount"
                       HAVING MAX("OrderID") > ((SELECT "ID" FROM orders ORDER BY "ID" DESC LIMIT 1)-1);
                       ''')
        amounts = cursor.fetchall()
        for i in range(0, numberof):
            cursor.execute(
                'UPDATE products SET "StorageAmount" = ("StorageAmount" + %s) WHERE "ID" = %s', (amounts[i][2], amounts[i][1]))
        conn.commit()
        conn.close()
        self.updateTable()

    def updatestorageamountforcustomer(self, place):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT "ID", "ProductID", "Amount"
                       FROM "orderItems"
                       GROUP BY "ID", "ProductID", "Amount"
                       HAVING MAX("OrderID") > ((SELECT "ID" FROM orders ORDER BY "ID" DESC LIMIT 1)-1);
                       ''')
        amounts = cursor.fetchall()
        print(amounts)
        cursor.execute(
            'UPDATE products SET "StorageAmount" = ("StorageAmount" + %s) WHERE "ID" = %s', (amounts[place][2], amounts[place][1]))
        conn.commit()
        conn.close()
        self.updateTable()

    def updatestorageamountcustomers(self, numberof):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT "ID", "ProductID", "Amount"
                       FROM "orderItems"
                       GROUP BY "ID", "ProductID", "Amount"
                       HAVING MAX("OrderID") > ((SELECT "ID" FROM orders ORDER BY "ID" DESC LIMIT 1)-1);
                       ''')
        amounts = cursor.fetchall()
        for i in range(0, numberof):
            cursor.execute(
                'UPDATE products SET "StorageAmount" = ("StorageAmount" - %s) WHERE "ID" = %s', (amounts[i][2], amounts[i][1]))
        conn.commit()
        conn.close()
        self.updateTable()

    def updatestorageamountcustomers2(self, numberof):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT "ID", "ProductID", "Amount"
                       FROM "orderItems"
                       GROUP BY "ID", "ProductID", "Amount"
                       HAVING MAX("OrderID") > ((SELECT "ID" FROM orders ORDER BY "ID" DESC LIMIT 1)-2) AND MAX("OrderID") < (SELECT "ID" FROM orders ORDER BY "ID" DESC LIMIT 1);
                       ''')
        amounts = cursor.fetchall()
        for i in range(0, numberof):
            cursor.execute(
                'UPDATE products SET "StorageAmount" = ("StorageAmount" - %s) WHERE "ID" = %s', (amounts[i][2], amounts[i][1]))
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

    def addbalance(self):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute('SELECT "Balance" FROM financials')
        balance = cursor.fetchmany()[0][0]
        conn.commit()
        conn.close()
        return balance

    def addpricecustomers(self, productid):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT "ProductPrice" FROM products WHERE "Name" = %s', [productid])
        price = cursor.fetchmany()[0][0]
        conn.commit()
        conn.close()
        return price

    def addpricesuppliers(self, productid, amount):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT "DiscountMinAmount" FROM products_suppliers WHERE "ProductID" = (SELECT "ID" FROM products WHERE "Name" = %s)', [productid])
        discountamount = cursor.fetchmany()[0][0]
        if (discountamount <= amount):
            cursor.execute(
                'SELECT "SupplierPrice" FROM products_suppliers WHERE "ProductID" = (SELECT "ID" FROM products WHERE "Name" = %s)', [productid])
            price = cursor.fetchmany()[0][0]
            cursor.execute(
                'SELECT "DiscountPercentage" FROM products_suppliers WHERE "ProductID" = (SELECT "ID" FROM products WHERE "Name" = %s)', [productid])
            discountpercentage = cursor.fetchmany()[0][0]
            price = price*(1-(discountpercentage/100))
            conn.commit()
            conn.close()
            return price
        else:
            cursor.execute(
                'SELECT "SupplierPrice" FROM products_suppliers WHERE "ProductID" = (SELECT "ID" FROM products WHERE "Name" = %s)', [productid])
            price = cursor.fetchmany()[0][0]
            conn.commit()
            conn.close()
            return price

    def addamountstorage(self, productid):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT "StorageAmount" FROM products WHERE "Name" = %s', (productid,))
        amount = cursor.fetchmany()[0][0]
        conn.commit()
        conn.close()
        return amount

    def addamountorder(self):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT "Amount" FROM "orderItems" WHERE "ID" = (SELECT "ID" FROM "orderItems" ORDER BY "ID" DESC LIMIT 1)')
        amount = cursor.fetchmany()[0][0]
        conn.commit()
        conn.close()
        return amount

    def addamountorderold(self, place):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT "ID", "ProductID", "Amount"
                       FROM "orderItems"
                       GROUP BY "ID", "ProductID", "Amount"
                       HAVING MAX("OrderID") > ((SELECT "ID" FROM orders ORDER BY "ID" DESC LIMIT 1)-2) AND MAX("OrderID") < (SELECT "ID" FROM orders ORDER BY "ID" DESC LIMIT 1);
                       ''')
        productid = cursor.fetchall()
        amount = productid[place][2]
        conn.commit()
        conn.close()
        return amount

    def productidold(self, place):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT "ID", "ProductID", "Amount"
                       FROM "orderItems"
                       GROUP BY "ID", "ProductID", "Amount"
                       HAVING MAX("OrderID") > ((SELECT "ID" FROM orders ORDER BY "ID" DESC LIMIT 1)-2) AND MAX("OrderID") < (SELECT "ID" FROM orders ORDER BY "ID" DESC LIMIT 1);
                       ''')
        productid = cursor.fetchall()

        cursor.execute(
            'SELECT "Name" FROM products WHERE "ID" = %s', (
                productid[place][1], ))
        name = cursor.fetchmany()[0][0]

        conn.commit()
        conn.close()
        return name


class View(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        model = Model(parent=self)
        self.setModel(model)
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)

    # @pyqtSlot()
    # def add(self):
    #    dialog = Dialog(parent=self)
    #    totalprice = 0
    #    if dialog.exec():
    #        self.model().add(dialog.dates,
    #                         dialog.operationtype)
    #        for i in range(0, int(dialog.numberof)):
    #            dialogitems = DialogItems(parent=self)
    #            if dialogitems.exec():
    #                price = self.model().addprice(dialogitems.productid)[0][0]
    #                self.model().additem(dialogitems.productid, dialogitems.amount)
    #                amount = self.model().addamountorder()[0][0]
    #                totalprice = totalprice + price*amount
    #        self.model().addtotalprice(totalprice)

    @ pyqtSlot()
    def addreturnorder(self):
        dialog = Dialog(parent=self)
        balance = self.model().addbalance()
        totalprice = 0
        complete = True
        if dialog.exec():
            self.model().addreturnorder(dialog.dates)
            for i in range(0, int(dialog.numberof)):
                dialogitems = DialogItems(parent=self)
                if dialogitems.exec():
                    price = self.model().addpricecustomers(dialogitems.productid)
                    self.model().additem(dialogitems.productid, dialogitems.amount)
                    amount = self.model().addamountorder()
                    if ((balance > price*amount) and (self.model().returnstatus(dialogitems.productid))):
                        balance = balance - price*amount
                        totalprice = totalprice + price*amount
                    else:
                        self.model().delete()
                        complete = False
                        break
            if (complete):
                self.model().updatetotalprice(totalprice)
                self.model().updatebalance(balance)

    @ pyqtSlot()
    def addsupplierorder(self):
        dialog = Dialog(parent=self)
        balance = self.model().addbalance()
        totalprice = 0
        complete = True
        if dialog.exec():
            self.model().addsupplierorder(dialog.dates)
            for i in range(0, int(dialog.numberof)):
                dialogitems = DialogItems(parent=self)
                if dialogitems.exec():
                    price = self.model().addpricesuppliers(
                        dialogitems.productid, int(dialogitems.amount))
                    self.model().additem(dialogitems.productid, dialogitems.amount)
                    amount = self.model().addamountorder()
                    if (balance > price*amount):
                        balance = balance - price*amount
                        totalprice = totalprice + price*amount
                    else:
                        self.model().delete()
                        complete = False
                        break
            if (complete):
                self.model().updatetotalprice(totalprice)
                self.model().updatebalance(balance)
                self.model().updatestorageamount(int(dialog.numberof))

    @ pyqtSlot()
    def addcustomerorder(self):
        dialog = Dialog(parent=self)
        balance = self.model().addbalance()
        totalprice = 0
        priceneedbuy = 0
        if dialog.exec():
            self.model().addcustomerorder(dialog.dates)
            for i in range(0, int(dialog.numberof)):
                dialogitems = DialogItems(parent=self)
                if dialogitems.exec():
                    self.model().additem(dialogitems.productid, dialogitems.amount)
                    storageamount = self.model().addamountstorage(
                        dialogitems.productid)
                    orderamount = self.model().addamountorder()
                    price = self.model().addpricecustomers(dialogitems.productid)
                    if (orderamount > storageamount):
                        totalprice = totalprice + price * orderamount
                        balance = balance + price*orderamount
                        priceneedbuy = priceneedbuy + price * \
                            (orderamount-storageamount)
                    else:
                        balance = balance + price*orderamount
                        totalprice = totalprice + price * orderamount
            if (priceneedbuy > 0):
                if (balance >= priceneedbuy):
                    # Обновляем данные с прошлого заказа
                    self.model().updatetotalprice(totalprice)
                    self.model().updatebalance(balance)
                    # Создать заказ на недостоющее
                    totalprice2 = 0
                    numberofitems = 0
                    self.model().addsupplierorder(dialog.dates)
                    for i in range(0, int(dialog.numberof)):
                        # 2 функции для productid и amount
                        productid_old = self.model().productidold(int(dialog.numberof)-1-numberofitems)
                        print(productid_old)
                        amount_old = self.model().addamountorderold(
                            int(dialog.numberof)-1-numberofitems)
                        amount_storage = self.model().addamountstorage(productid_old)
                        print(amount_old)
                        print(amount_storage)
                        if (amount_old > amount_storage):
                            self.model().additem(productid_old, (amount_old-amount_storage))
                            # Потенциальная ошибка так как странно нумируется
                            self.model().updatestorageamountforcustomer(
                                0)
                            price = self.model().addpricesuppliers(
                                productid_old, (amount_old-amount_storage))
                            balance = balance - price * \
                                (amount_old-amount_storage)
                            totalprice2 = totalprice2 + price * \
                                (amount_old-amount_storage)
                        numberofitems += 1

                    self.model().updatetotalprice(totalprice2)
                    self.model().updatebalance(balance)
                    self.model().updatestorageamountcustomers2(int(dialog.numberof))

                else:
                    self.model().delete()
            else:
                self.model().updatetotalprice(totalprice)
                self.model().updatebalance(balance)
                self.model().updatestorageamountcustomers(int(dialog.numberof))


class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Orders')

        dates_label = QLabel('Dates', parent=self)
        self.__dates_edit = QLineEdit(parent=self)

        numberof_label = QLabel('Number of items', parent=self)
        self.__numberof_edit = QLineEdit(parent=self)

        ok_button = QPushButton('Ok', parent=self)
        cancel_button = QPushButton('Cancel', parent=self)

        layout = QVBoxLayout(self)
        layout.addWidget(dates_label)
        layout.addWidget(self.__dates_edit)
        layout.addWidget(numberof_label)
        layout.addWidget(self.__numberof_edit)

        layout2 = QHBoxLayout()
        layout2.addWidget(ok_button)
        layout2.addWidget(cancel_button)

        layout.addLayout(layout2)

        cancel_button.clicked.connect(self.reject)
        ok_button.clicked.connect(self.finish)

    @ pyqtSlot()
    def finish(self):
        if self.dates is None:
            return
        self.accept()

    @ property
    def dates(self):
        dates = self.__dates_edit.text().strip()
        if dates == '':
            return None
        else:
            return dates

    @ property
    def numberof(self):
        return str(self.__numberof_edit.text()).strip()

    @ dates.setter
    def dates(self, value):
        self.__dates_edit.setText(value)


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

    @ pyqtSlot()
    def finish(self):
        if self.productid is None:
            return
        self.accept()

    @ property
    def productid(self):
        result = self.__productid_choose.currentText().strip()
        if result == '':
            return None
        else:
            return result

    @ property
    def amount(self):
        return str(self.__amount_edit.text()).strip()

    @ productid.setter
    def productid(self, value):
        self.__productid_choose.setText(value)
