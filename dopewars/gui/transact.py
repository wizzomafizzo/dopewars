# dope wars qt transactions dialog

import math

from PyQt5.QtWidgets import QDialog

import common
import qt_transact_dialog


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
