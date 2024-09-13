from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import pyqtSlot
from MainMenu import MainMenu
import Product
import Supplier
import Order


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.showMaximized()
        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)

        main_menu.product_mode_request.connect(self.product_mode_on)
        main_menu.supplier_mode_request.connect(self.supplier_mode_on)
        main_menu.order_mode_request.connect(self.order_mode_on)

    @pyqtSlot()
    def product_mode_on(self):
        old = self.centralWidget()
        pv = Product.View(parent=self)
        self.setCentralWidget(pv)
        self.menuBar().setMode_Product(pv)
        if old is not None:
            old.deleteLater()

    @pyqtSlot()
    def supplier_mode_on(self):
        old = self.centralWidget()
        sv = Supplier.View(parent=self)
        self.setCentralWidget(sv)
        self.menuBar().setMode_Supplier(sv)
        if old is not None:
            old.deleteLater()

    @pyqtSlot()
    def order_mode_on(self):
        old = self.centralWidget()
        ov = Order.View(parent=self)
        self.setCentralWidget(ov)
        self.menuBar().setMode_Order(ov)
        if old is not None:
            old.deleteLater()
