# dope wars qt finances dialog

from PyQt5.QtWidgets import QDialog

import qt_finances_dialog


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
