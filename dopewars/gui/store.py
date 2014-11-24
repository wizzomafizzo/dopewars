# dope wars qt store dialog

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog

import common
from gui.common import DrugWidget
import qt_store_dialog


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
