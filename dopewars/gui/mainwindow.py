# dope wars qt main window

import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

import common
import world
from gui.common import DrugWidget
from gui.finances import FinancesDialog
from gui.store import StoreDialog
from gui.transact import TransactDialog
import qt_main_window


class MainWindow():
    def __init__(self):
        """Display the main dopewars window."""
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.ui = qt_main_window.Ui_MainWindow()
        self.ui.setupUi(self.window)

        # set up signals
        self.ui.actionQuit.triggered.connect(self.app.closeAllWindows)

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

        self.log = []

        # set up world
        self.world = world.World()
        self.world.new_world("Test Guy")

        self.add_log("<h2>A new game begins!</h2>")
        self.add_log("It's day <b>%i</b>.<i style='color: red; font-size: large'>You've got a loan to pay off!</i>" % self.world.day[0])

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
        self.clear_log()
        self.add_log("It's day <b>%i.</b>" % self.world.day[0])
        self.update()

    def update_areas(self):
        """Set up and toggle area buttons."""
        self.ui.world_layout.setTitle(self.world.world_name)
        self.ui.jet_button.setText("Jet!")
        self.ui.jet_button.setEnabled(False)
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

    def add_log(self, message):
        self.log.append(message)
        self.render_log()

    def clear_log(self):
        self.log = []

    def render_log(self):
        html = "<html><body>"
        for msg in self.log:
            html = html + msg
        html = html + "</body></html>"
        self.ui.action_log_textedit.setHtml(html)
