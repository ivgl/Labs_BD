# @pyqtSlot()
# def add(self):
#    dialog = Dialog(parent=self)
#    if dialog.exec():
#        balance = self.model().addbalance()[0][0]
#        self.model().add(dialog.totalprice, dialog.dates,
#                         dialog.operationtype, dialog.numberof)
#        for i in range(0, int(dialog.numberof)):
#            dialogitems = DialogItems(parent=self)
#            if dialogitems.exec():
#                 price = self.model().addprice(dialogitems.productid)[0][0]
#                  amount = self.model().addamount(
#                       dialogitems.productid)[0][0]
#                   if (price*amount < balance):
#                        balance = balance - price*amount
#                        self.model().additem(dialogitems.productid, dialogitems.amount)
#                    else:
#                        print("error")

a = [(1,), (5,)]
for i in range(0, 2):
    print(a[i][0])
