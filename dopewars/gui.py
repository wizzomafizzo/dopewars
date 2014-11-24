# dope wars qt gui

import sys
import math

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QDialog

import common
import dopewars
import qt_main_window
import qt_transact_dialog
import qt_finances_dialog
import qt_store_dialog


class DrugWidget(QTableWidgetItem):
    """Extends drug table items to have name attribute."""
    def __init__(self, text, name):
        self.name = name
        QTableWidgetItem.__init__(self, text)


class TransactDialog():
    """Dialog to specify amount for buy, sell and dump.
    Shows some info about transaction depending on kind."""
    def __init__(self, parent, kind):
        self.dialog = QDialog(parent.window)
        self.ui = qt_transact_dialog.Ui_Dialog()
        self.ui.setupUi(self.dialog)

        self.ui.max_button.clicked.connect(self.max_button)
        self.ui.amount_spinbox.valueChanged.connect(self.update)

        self.amount = 1  # final value checked on accept
        self.max_amount = 1
        self.kind = kind

        # get selected item
        if kind == "Buy":
            self.name = parent.ui.dealer_table.currentItem().name
        else:
            self.name = parent.ui.trenchcoat_table.currentItem().name

        # free space
        max_drugs = parent.world.player.trenchcoat["max"]
        self.free_space = max_drugs - parent.world.player.total_drugs()

        # dealer price
        self.price = parent.world.dealer[self.name]

        # amount player owns
        if kind != "Buy":
            trenchcoat = parent.world.player.trenchcoat["drugs"]
            self.owned = trenchcoat[self.name]["count"]

        # set windows title
        pretty_name = common.drugs[self.name]["name"]
        self.dialog.setWindowTitle("%s %s" % (kind, pretty_name))

        # max amount can be bought/sold/dumped
        cash = parent.world.player.cash
        if kind == "Buy":
            self.max_amount = math.floor(cash / self.price)
            if self.max_amount > self.free_space:
                self.max_amount = self.free_space
        else:
            self.max_amount = self.owned

        self.ui.amount_spinbox.setMaximum(self.max_amount)
        self.ui.amount_spinbox.setValue(self.max_amount)
        self.update()

    def max_button(self):
        """Set spinbox to max amount."""
        self.ui.amount_spinbox.setValue(self.max_amount)

    def update(self):
        """Update final amount, info and toggle buttons."""
        self.amount = self.ui.amount_spinbox.value()

        # max button
        if self.amount == self.max_amount:
            self.ui.max_button.setEnabled(False)
        else:
            self.ui.max_button.setEnabled(True)

        # transaction info
        if self.kind == "Dump":
            self.ui.total_label.setText("%i left" % (self.owned - self.amount))
        else:
            self.ui.total_label.setText("$%i total" % (self.amount * self.price))


class FinancesDialog():
    """Dialog for managing bank account and loans."""
    def __init__(self, parent):
        self.dialog = QDialog(parent.window)
        self.ui = qt_finances_dialog.Ui_Dialog()
        self.ui.setupUi(self.dialog)

        self.parent = parent
        self.world = self.parent.world

        self.ui.cash_spinbox.valueChanged.connect(self.update)
        self.ui.bank_spinbox.valueChanged.connect(self.update)
        self.ui.loan_spinbox.valueChanged.connect(self.update)
        self.ui.deposit_button.clicked.connect(self.deposit_button)
        self.ui.withdraw_button.clicked.connect(self.withdraw_button)
        self.ui.pay_loan_button.clicked.connect(self.pay_loan_button)
        self.ui.take_loan_button.clicked.connect(self.take_loan_button)
        self.ui.max_bank_button.clicked.connect(self.max_bank_button)
        self.ui.max_cash_button.clicked.connect(self.max_cash_button)

        self.update()

        self.ui.cash_spinbox.setValue(self.world.player.cash)
        self.ui.bank_spinbox.setValue(self.world.player.bank)

    def update(self):
        """Toggle all buttons, update labels and spinbox settings."""
        self.ui.cash_spinbox.setMaximum(self.world.player.cash)
        self.ui.bank_spinbox.setMaximum(self.world.player.bank)

        self.ui.cash_lcd.display(self.parent.world.player.cash)
        self.ui.bank_lcd.display(self.parent.world.player.bank)
        self.ui.loan_lcd.display(self.parent.world.player.loan)

        # toggle max buttons
        if self.world.player.cash == self.ui.cash_spinbox.value():
            self.ui.max_cash_button.setEnabled(False)
        else:
            self.ui.max_cash_button.setEnabled(True)

        if self.world.player.bank == self.ui.bank_spinbox.value():
            self.ui.max_bank_button.setEnabled(False)
        else:
            self.ui.max_bank_button.setEnabled(True)

        # toggle bank and cash buttons
        if self.ui.cash_spinbox.value() == 0:
            self.ui.deposit_button.setEnabled(False)
        else:
            self.ui.deposit_button.setEnabled(True)

        if self.ui.bank_spinbox.value() == 0:
            self.ui.withdraw_button.setEnabled(False)
        else:
            self.ui.withdraw_button.setEnabled(True)

        # toggle bank and cash spinboxes
        if self.world.player.cash == 0:
            self.ui.cash_spinbox.setEnabled(False)
        else:
            self.ui.cash_spinbox.setEnabled(True)

        if self.world.player.bank == 0:
            self.ui.bank_spinbox.setEnabled(False)
        else:
            self.ui.bank_spinbox.setEnabled(True)

        # loan spinbox
        if self.world.player.loan > 0:
            self.ui.loan_spinbox.setEnabled(False)
        else:
            self.ui.loan_spinbox.setEnabled(True)

        # take loan
        if self.ui.loan_spinbox.value() > 0 and self.world.player.loan == 0:
            self.ui.take_loan_button.setEnabled(True)
        else:
            self.ui.take_loan_button.setEnabled(False)

        # pay loan
        if (self.parent.world.player.cash >= self.parent.world.player.loan
            and self.parent.world.player.loan > 0):
            self.ui.pay_loan_button.setEnabled(True)
        else:
            self.ui.pay_loan_button.setEnabled(False)

    def deposit_button(self):
        """Deposit amount to bank."""
        self.world.deposit_bank(self.ui.cash_spinbox.value())
        self.update()
        self.parent.update()

    def withdraw_button(self):
        """Withdraw amount from bank."""
        self.world.withdraw_bank(self.ui.bank_spinbox.value())
        self.update()
        self.parent.update()

    def pay_loan_button(self):
        """Pay off entire loan."""
        self.world.pay_loan()
        self.update()
        self.parent.update()

    def take_loan_button(self):
        """Take out new loan."""
        self.world.take_loan(self.ui.loan_spinbox.value())
        self.ui.loan_spinbox.setValue(0)
        self.update()
        self.parent.update()

    def max_bank_button(self):
        """Set bank spinbox to max allowed."""
        self.ui.bank_spinbox.setValue(self.world.player.bank)

    def max_cash_button(self):
        """Set cash spinbox to max allowed."""
        self.ui.cash_spinbox.setValue(self.world.player.cash)


class StoreDialog():
    def __init__(self, parent):
        """Display store dialog."""
        self.dialog = QDialog(parent.window)
        self.ui = qt_store_dialog.Ui_Dialog()
        self.ui.setupUi(self.dialog)

        self.parent = parent
        self.world = self.parent.world

        self.ui.weapons_table.itemSelectionChanged.connect(self.update)
        self.ui.buy_button.clicked.connect(self.buy_weapon)

        self.update()
        self.ui.weapons_table.setCurrentCell(0, 0)

    def populate_weapons(self):
        """Populate weapons table with weapons on offer."""
        # TODO: sort alphabetically
        weapon = self.world.player.weapon[0]
        row_count = len(common.weapons.keys())
        self.ui.weapons_table.setRowCount(row_count)

        if weapon is not None:
            row = 1
            name = common.weapons[weapon]["name"]
            price = common.weapons[weapon]["ammo_price"]
            name_cell = DrugWidget((name + " Ammo (10)"), weapon)
            price_cell = DrugWidget(str(price), weapon)
            price_cell.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.weapons_table.setItem(0, 0, name_cell)
            self.ui.weapons_table.setItem(0, 1, price_cell)
        else:
            row = 0

        for name in common.weapons.keys():
            if name != weapon:
                name_cell = DrugWidget(common.weapons[name]["name"], name)
                price_cell = DrugWidget(str(common.weapons[name]["weapon_price"]), name)
                price_cell.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.weapons_table.setItem(row, 0, name_cell)
                self.ui.weapons_table.setItem(row, 1, price_cell)
                row += 1

    def update(self):
        self.populate_weapons()

        self.ui.cash_lcd.display(self.world.player.cash)

        self.ui.buy_button.setEnabled(False)
        selected = self.ui.weapons_table.currentItem()
        if selected is not None:
            if selected.name == self.world.player.weapon[0]:
                lookup = "ammo_price"
            else:
                lookup = "weapon_price"

            if self.world.player.cash >= common.weapons[selected.name][lookup]:
                self.ui.buy_button.setEnabled(True)

        weapon, ammo = self.world.player.weapon
        if weapon is not None:
            pretty_name = common.weapons[weapon]["name"]
            self.ui.weapon_equipped.setText("%s [%i]" % (pretty_name, ammo))
        else:
            self.ui.weapon_equipped.setText("Unarmed")

    def buy_weapon(self):
        name = self.ui.weapons_table.currentItem().name
        if name == self.world.player.weapon[0]:
            self.world.buy_ammo(name)
        else:
            self.world.buy_weapon(name)
        self.update()
        self.parent.update()
        self.ui.weapons_table.setCurrentCell(0, 0)


class MainWindow():
    def __init__(self):
        """Display the main dopewars window."""
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.ui = qt_main_window.Ui_MainWindow()
        self.ui.setupUi(self.window)

        # set up signals
        self.ui.buy_button.clicked.connect(lambda: self.do_transact("Buy"))
        self.ui.sell_button.clicked.connect(lambda: self.do_transact("Sell"))
        self.ui.dump_button.clicked.connect(lambda: self.do_transact("Dump"))
        self.ui.dealer_table.itemDoubleClicked.connect(lambda: self.do_transact("Buy"))
        self.ui.trenchcoat_table.itemDoubleClicked.connect(lambda: self.do_transact("Sell"))

        self.ui.finances_button.clicked.connect(self.finances_button)
        self.ui.store_button.clicked.connect(self.store_button)

        self.ui.dealer_table.itemSelectionChanged.connect(self.toggle_buttons)
        self.ui.trenchcoat_table.itemSelectionChanged.connect(self.toggle_buttons)

        self.ui.area_1_button.clicked.connect(lambda: self.travel_to(0))
        self.ui.area_2_button.clicked.connect(lambda: self.travel_to(1))
        self.ui.area_3_button.clicked.connect(lambda: self.travel_to(2))
        self.ui.area_4_button.clicked.connect(lambda: self.travel_to(3))
        self.ui.area_5_button.clicked.connect(lambda: self.travel_to(4))
        self.ui.area_6_button.clicked.connect(lambda: self.travel_to(5))

        # set up world
        self.world = dopewars.World()
        self.world.new_world("Test Guy")

        self.clear_action_log()
        self.log_action("A new game begins!")

        self.update()

        # let's do it!
        self.window.show()
        sys.exit(self.app.exec_())

    def finances_button(self):
        """Display finances dialog."""
        finances = FinancesDialog(self)
        finances.dialog.exec()

    def store_button(self):
        """Display store dialog."""
        store = StoreDialog(self)
        store.dialog.exec()

    def travel_to(self, index):
        """Change current area and tick to next day."""
        self.world.travel_to(index)
        self.clear_action_log()
        self.update()

    def update_areas(self):
        """Set up and toggle area buttons."""
        self.ui.world_layout.setTitle(self.world.world_name)
        for i in range(6):
            getattr(self.ui, "area_%s_button" % (i+1)).setText(self.world.areas[i])
            on = True
            if self.world.areas[i] == self.world.current_area:
                on = False
            getattr(self.ui, "area_%s_button" % (i+1)).setEnabled(on)

    def toggle_buttons(self):
        """Toggle all action buttons."""
        # sell button
        if self.ui.dealer_table.currentItem() is not None:
            self.ui.buy_button.setEnabled(True)
        else:
            self.ui.buy_button.setEnabled(False)

        # buy/dump buttons
        selected_trenchcoat = self.ui.trenchcoat_table.currentItem()
        if selected_trenchcoat is not None:
            self.ui.dump_button.setEnabled(True)
            # dealer offering drug?
            if selected_trenchcoat.name in self.world.dealer.keys():
                self.ui.sell_button.setEnabled(True)
            else:
                self.ui.sell_button.setEnabled(False)
        else:
            self.ui.sell_button.setEnabled(False)
            self.ui.dump_button.setEnabled(False)

    def do_transact(self, kind):
        """Display transaction dialog for buy/sell/dump."""
        if kind == "Buy":
            name = self.ui.dealer_table.currentItem().name
        else:
            name = self.ui.trenchcoat_table.currentItem().name

        transact = TransactDialog(self, kind)
        kind_map = {
            "Buy": "buy_from_dealer",
            "Sell": "sell_to_dealer",
            "Dump": "dump_drug"
        }

        def finalise():
            getattr(self.world, kind_map[kind])(name, transact.amount)
            self.update()

        transact.dialog.accepted.connect(finalise)
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

        # weapon
        weapon, ammo = self.world.player.weapon
        if weapon is not None:
            pretty_name = common.weapons[weapon]["name"]
            self.ui.weapon_equipped.setText("%s [%i]" % (pretty_name, ammo))
        else:
            self.ui.weapon_equipped.setText("Unarmed")

        # dealer
        self.populate_dealer()
        # trenchcoat
        self.populate_trenchcoat()

        # areas
        self.update_areas()

    def populate_dealer(self):
        """Populate dealer table with drugs on offer."""
        # TODO: sort alphabetically
        self.ui.dealer_table.setRowCount(len(self.world.dealer.keys()))
        drugs_sorted = sorted(self.world.dealer.keys())
        row = 0
        for name in drugs_sorted:
            pretty_name = common.drugs[name]["name"]
            name_cell = DrugWidget(pretty_name, name)
            price_cell = DrugWidget(str(self.world.dealer[name]), name)
            price_cell.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.dealer_table.setItem(row, 0, name_cell)
            self.ui.dealer_table.setItem(row, 1, price_cell)
            row += 1

    def populate_trenchcoat(self):
        """Populate trenchcoat table with held drugs."""
        # TODO: sort alphabetically
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
        # max space label
        self.ui.max_drugs_label.setText("%i/%i" % (self.world.player.total_drugs(),
                                                   self.world.player.trenchcoat["max"]))

    def clear_action_log(self):
        self.ui.action_log_textedit.setPlainText("")

    def log_action(self, message):
        current = self.ui.action_log_textedit.toPlainText()
        self.ui.action_log_textedit.setPlainText("%s%s\n" % (current, message))

if __name__ == "__main__":
    MainWindow()
