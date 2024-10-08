from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QActionGroup
from PyQt6.QtCore import pyqtSlot, pyqtSignal


class MainMenu(QMenuBar):
    product_mode_request = pyqtSignal()
    supplier_mode_request = pyqtSignal()
    order_mode_request = pyqtSignal()
    accounting_mode_request = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        product_menu = self.addMenu("Product")
        self.addP = product_menu.addAction('Add product')
        self.updateP = product_menu.addAction('Update product')
        self.deleteP = product_menu.addAction('Delete product')

        suppliers_menu = self.addMenu("Suppliers")
        self.addS = suppliers_menu.addAction('Add supplier')
        self.updateS = suppliers_menu.addAction('Update supplier')
        self.deleteS = suppliers_menu.addAction('Delete supplier')

        orders_menu = self.addMenu("Orders")
        self.addreturnO = orders_menu.addAction('Add return order')
        self.addsupplierO = orders_menu.addAction('Add supplier order')
        self.addcustomerO = orders_menu.addAction('Add customer order')

        accounting_menu = self.addMenu("Accounting")
        self.storageS = accounting_menu.addAction('Storage status')
        self.ordersP = accounting_menu.addAction('Orders period')
        self.financialsP = accounting_menu.addAction('Financials period')

        mode_menu = menu = self.addMenu("Mode")
        mode_action_group = ag = QActionGroup(self)
        self.product_mode_action = act = mode_menu.addAction("Product")
        act.setCheckable(True)
        act.toggled.connect(self.toggle_product_mode)
        ag.addAction(act)
        self.supplier_mode_action = act = mode_menu.addAction("Supplier")
        act.setCheckable(True)
        act.toggled.connect(self.toggle_supplier_mode)
        ag.addAction(act)
        self.order_mode_action = act = mode_menu.addAction("Order")
        act.setCheckable(True)
        act.toggled.connect(self.toggle_order_mode)
        ag.addAction(act)
        self.accounting_mode_action = act = mode_menu.addAction("Accounting")
        act.setCheckable(True)
        act.toggled.connect(self.toggle_accounting_mode)
        ag.addAction(act)

    def setMode_Product(self, widget):
        self.addP.triggered.connect(widget.add)
        self.updateP.triggered.connect(widget.update)
        self.deleteP.triggered.connect(widget.delete)

    def setMode_Supplier(self, widget):
        self.addS.triggered.connect(widget.add)
        self.updateS.triggered.connect(widget.update)
        self.deleteS.triggered.connect(widget.delete)

    def setMode_Order(self, widget):
        self.addreturnO.triggered.connect(widget.addreturnorder)
        self.addsupplierO.triggered.connect(widget.addsupplierorder)
        self.addcustomerO.triggered.connect(widget.addcustomerorder)

    def setMode_Accounting(self, widget):
        self.storageS.triggered.connect(widget.storage_status)
        self.ordersP.triggered.connect(widget.orders_period)
        self.financialsP.triggered.connect(widget.financials_period)

    @pyqtSlot(bool)
    def toggle_product_mode(self, enabled):
        if enabled:
            self.product_mode_request.emit()

    @pyqtSlot(bool)
    def toggle_supplier_mode(self, enabled):
        if enabled:
            self.supplier_mode_request.emit()

    @pyqtSlot(bool)
    def toggle_order_mode(self, enabled):
        if enabled:
            self.order_mode_request.emit()

    @pyqtSlot(bool)
    def toggle_accounting_mode(self, enabled):
        if enabled:
            self.accounting_mode_request.emit()
