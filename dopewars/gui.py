# dope wars qt gui

import sys, math

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog

import dopewars, common
import qt_main_window, qt_transact_dialog, qt_finances_dialog, qt_store_dialog

class DrugWidget(QTableWidgetItem):
    """Extends drug table items to have name attribute."""
    def __init__(self, text, name):
        self.name = name
        QTableWidgetItem.__init__(self, text)

class TransactDialog():
    # TOD: just use parent
    def __init__(self, parent, kind, name, price, cash, free_space, owned):
        self.dialog = QDialog(parent)
        self.ui = qt_transact_dialog.Ui_Dialog()
        self.ui.setupUi(self.dialog)

        self.ui.max_button.clicked.connect(self.max_button)
        self.ui.amount_spinbox.valueChanged.connect(self.update_total)

        self.kind = kind
        self.amount = 1
        self.max_amount = 1
        self.price = price
        self.owned = owned

        self.update_total()

        self.dialog.setWindowTitle("%s %s" % (kind, name))

        if kind == "Buy":
            self.max_amount = math.floor(cash / price)
            if self.max_amount > free_space:
                self.max_amount = free_space
        else:
            self.max_amount = owned

        self.ui.amount_spinbox.setMaximum(self.max_amount)
        self.ui.amount_spinbox.setValue(self.max_amount)

    def max_button(self):
        self.ui.amount_spinbox.setValue(self.max_amount)

    def update_total(self):
        self.amount = self.ui.amount_spinbox.value()
        if self.kind == "Dump":
            self.ui.total_label.setText("%i left" % (self.owned - self.amount))
        else:
            self.ui.total_label.setText("$%i total" % (self.amount * self.price))

class FinancesDialog():
    def __init__(self, parent):
        self.dialog = QDialog(parent.window)
        self.ui = qt_finances_dialog.Ui_Dialog()
        self.ui.setupUi(self.dialog)

        self.parent = parent
        self.world = self.parent.world

        self.ui.cash_spinbox.valueChanged.connect(self.update)
        self.ui.bank_spinbox.valueChanged.connect(self.update)
        self.ui.deposit_button.clicked.connect(self.deposit_button)
        self.ui.withdraw_button.clicked.connect(self.withdraw_button)
        self.ui.max_bank_button.clicked.connect(self.max_bank_button)
        self.ui.max_cash_button.clicked.connect(self.max_cash_button)

        self.update()

        self.ui.cash_spinbox.setValue(self.world.player.cash)
        self.ui.bank_spinbox.setValue(self.world.player.bank)

    def update(self):
        self.ui.cash_spinbox.setMaximum(self.world.player.cash)
        self.ui.bank_spinbox.setMaximum(self.world.player.bank)

        if self.world.player.cash == self.ui.cash_spinbox.value():
            self.ui.max_cash_button.setEnabled(False)
        else:
            self.ui.max_cash_button.setEnabled(True)

        if self.world.player.bank == self.ui.bank_spinbox.value():
            self.ui.max_bank_button.setEnabled(False)
        else:
            self.ui.max_bank_button.setEnabled(True)

        if self.ui.cash_spinbox.value() == 0:
            self.ui.deposit_button.setEnabled(False)
        else:
            self.ui.deposit_button.setEnabled(True)

        if self.ui.bank_spinbox.value() == 0:
            self.ui.withdraw_button.setEnabled(False)
        else:
            self.ui.withdraw_button.setEnabled(True)

        self.ui.loan_amount.setText("$%i" % self.world.player.loan)

        if self.world.player.loan > 0:
            self.ui.pay_loan_button.setEnabled(True)
            self.ui.loan_spinbox.setEnabled(False)
            self.ui.take_loan_button.setEnabled(False)
        else:
            self.ui.pay_loan_button.setEnabled(False)
            self.ui.loan_spinbox.setEnabled(True)
            self.ui.take_loan_button.setEnabled(True)

    def deposit_button(self):
        amount = self.ui.cash_spinbox.value()
        # TODO: make this world method
        self.world.player.spend_cash(amount)
        self.world.player.add_bank(amount)
        self.update()
        self.parent.update()

    def withdraw_button(self):
        amount = self.ui.bank_spinbox.value()
        # TODO: make this world method
        self.world.player.add_cash(amount)
        self.world.player.remove_bank(amount)
        self.update()
        self.parent.update()

    def max_bank_button(self):
        self.ui.bank_spinbox.setValue(self.world.player.bank)

    def max_cash_button(self):
        self.ui.cash_spinbox.setValue(self.world.player.cash)

class StoreDialog():
    def __init__(self, parent):
        self.dialog = QDialog(parent.window)
        self.ui = qt_store_dialog.Ui_Dialog()
        self.ui.setupUi(self.dialog)

class MainWindow():
    def __init__(self):
        """Display the main dopewars window."""
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.ui = qt_main_window.Ui_MainWindow()
        self.ui.setupUi(self.window)

        self.ui.buy_button.clicked.connect(self.buy_button)
        self.ui.sell_button.clicked.connect(self.sell_button)
        self.ui.dump_button.clicked.connect(self.dump_button)

        self.ui.finances_button.clicked.connect(self.finances_button)
        self.ui.store_button.clicked.connect(self.store_button)

        self.ui.dealer_table.itemDoubleClicked.connect(self.buy_button)
        self.ui.trenchcoat_table.itemDoubleClicked.connect(self.sell_button)

        self.ui.dealer_table.itemSelectionChanged.connect(self.toggle_buttons)
        self.ui.trenchcoat_table.itemSelectionChanged.connect(self.toggle_buttons)

        self.ui.area_1_button.clicked.connect(lambda: self.travel_to(0))
        self.ui.area_2_button.clicked.connect(lambda: self.travel_to(1))
        self.ui.area_3_button.clicked.connect(lambda: self.travel_to(2))
        self.ui.area_4_button.clicked.connect(lambda: self.travel_to(3))
        self.ui.area_5_button.clicked.connect(lambda: self.travel_to(4))
        self.ui.area_6_button.clicked.connect(lambda: self.travel_to(5))

        self.world = dopewars.World()
        self.world.new_world("Test Guy")
        self.world.player.add_drug("weed", 150, 25)

        self.update()
        self.clear_action_log()
        self.log_action("A new game begins!")

        self.window.show()
        sys.exit(self.app.exec_())

    def finances_button(self):
        finances = FinancesDialog(self)
        finances.dialog.exec()

    def store_button(self):
        store = StoreDialog(self)
        store.dialog.exec()

    def travel_to(self, index):
        self.world.travel_to(index)
        self.update()

    def update_areas(self):
        self.ui.world_layout.setTitle(self.world.world_name)
        for i in range(6):
            getattr(self.ui, "area_%s_button" % (i+1)).setText(self.world.areas[i])
            on = True
            if self.world.areas[i] == self.world.current_area:
                on = False
            getattr(self.ui, "area_%s_button" % (i+1)).setEnabled(on)

    def toggle_buttons(self):
        if self.ui.dealer_table.currentItem() is not None:
            self.ui.buy_button.setEnabled(True)
        else:
            self.ui.buy_button.setEnabled(False)

        if self.ui.trenchcoat_table.currentItem() is not None:
            self.ui.dump_button.setEnabled(True)
            if self.ui.trenchcoat_table.currentItem().name in self.world.dealer.keys():
                self.ui.sell_button.setEnabled(True)
            else:
                self.ui.sell_button.setEnabled(False)
        else:
            self.ui.sell_button.setEnabled(False)
            self.ui.dump_button.setEnabled(False)

    def buy_button(self):
        name = self.ui.dealer_table.currentItem().name
        max_drugs = self.world.player.trenchcoat["max"]
        free_space = max_drugs - self.world.player.total_drugs()
        transact = TransactDialog(self.window,
                                  "Buy",
                                  common.drugs[name]["name"],
                                  self.world.dealer[name],
                                  self.world.player.cash,
                                  free_space,
                                  0)

        def buy():
            self.world.buy_from_dealer(name, transact.amount)
            self.update()

        transact.dialog.accepted.connect(buy)
        transact.dialog.exec()

    def sell_button(self):
        name = self.ui.trenchcoat_table.currentItem().name
        owned = self.world.player.trenchcoat["drugs"][name]["count"]
        transact = TransactDialog(self.window,
                                  "Sell",
                                  common.drugs[name]["name"],
                                  self.world.dealer[name],
                                  self.world.player.cash,
                                  0,
                                  owned)

        def sell():
            self.world.sell_to_dealer(name, transact.amount)
            self.update()

        transact.dialog.accepted.connect(sell)
        transact.dialog.exec()

    def dump_button(self):
        name = self.ui.trenchcoat_table.currentItem().name
        owned = self.world.player.trenchcoat["drugs"][name]["count"]
        transact = TransactDialog(self.window,
                                  "Dump",
                                  common.drugs[name]["name"],
                                  self.world.dealer[name],
                                  self.world.player.cash,
                                  0,
                                  owned)

        def dump():
            self.world.player.remove_drug(name, transact.amount)
            self.update()

        transact.dialog.accepted.connect(dump)
        transact.dialog.exec()

    def update(self):
        """Refresh all widgets with update values."""
        # name
        self.ui.name_label.setText(self.world.player.name)
        # days
        self.ui.days_label.setText("Day %i/%i" % (self.world.day[0],
                                                  self.world.day[1]))
        # health
        self.ui.health_slider.setMaximum(self.world.player.health[1])
        self.ui.health_slider.setValue(self.world.player.health[0])
        self.ui.health_slider.setToolTip("%i/%i" % (self.world.player.health[0],
                                                    self.world.player.health[1]))
        # cash
        self.ui.cash_lcd.display(self.world.player.cash)
        # bank
        self.ui.bank_lcd.display(self.world.player.bank)
        # loan
        self.ui.loan_lcd.display(self.world.player.loan)

        # dealer
        self.populate_dealer()
        # trenchcoat
        self.populate_trenchcoat()

        # areas
        self.update_areas()

    def populate_dealer(self):
        self.ui.dealer_table.setRowCount(len(self.world.dealer.keys()))
        row = 0
        for name, price in self.world.dealer.items():
            pretty_name = common.drugs[name]["name"]
            name_cell = DrugWidget(pretty_name, name)
            price_cell = DrugWidget(str(price), name)
            price_cell.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.dealer_table.setItem(row, 0, name_cell)
            self.ui.dealer_table.setItem(row, 1, price_cell)
            row += 1

    def populate_trenchcoat(self):
        self.ui.trenchcoat_table.setRowCount(len(self.world.player.trenchcoat["drugs"].keys()))
        row = 0
        for k, v in self.world.player.trenchcoat["drugs"].items():
            pretty_name = common.drugs[k]["name"]
            name_cell = DrugWidget(pretty_name, k)
            price_cell = DrugWidget(str(v["price"]), k)
            price_cell.setTextAlignment(QtCore.Qt.AlignCenter)
            count_cell = DrugWidget(str(v["count"]), k)
            count_cell.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.trenchcoat_table.setItem(row, 0, name_cell)
            self.ui.trenchcoat_table.setItem(row, 1, price_cell)
            self.ui.trenchcoat_table.setItem(row, 2, count_cell)
            row += 1
        # max space
        self.ui.max_drugs_label.setText("%i/%i" % (self.world.player.total_drugs(),
                                                   self.world.player.trenchcoat["max"]))

    def clear_action_log(self):
        self.ui.action_log_textedit.setPlainText("")

    def log_action(self, message):
        current = self.ui.action_log_textedit.toPlainText()
        self.ui.action_log_textedit.setPlainText("%s%s\n" % (current, message))

if __name__ == "__main__":
    MainWindow()
