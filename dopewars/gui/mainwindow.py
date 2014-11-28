# dope wars qt main window

import sys, random

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon

import common
import world

from gui.common import DrugWidget
from gui.finances import FinancesDialog
from gui.store import StoreDialog
from gui.transact import TransactDialog
from gui.fight import FightDialog
from gui.newgame import NewGameDialog
from gui.highscores import HighScoresDialog
import qt_main_window

config = {
    "cop_chance": 30
}

class MainWindow():
    def __init__(self):
        """Display the main dopewars window."""
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.ui = qt_main_window.Ui_MainWindow()
        self.ui.setupUi(self.window)

        # set up signals
        self.ui.actionQuit.triggered.connect(self.app.closeAllWindows)
        self.ui.actionNewGame.triggered.connect(self.new_game)

        self.ui.buy_button.clicked.connect(lambda: self.do_transact("Buy"))
        self.ui.sell_button.clicked.connect(lambda: self.do_transact("Sell"))
        self.ui.dump_button.clicked.connect(lambda: self.do_transact("Dump"))

        self.ui.dealer_table.itemDoubleClicked.connect(self.doubleclick_buy)
        self.ui.trenchcoat_table.itemDoubleClicked.connect(self.doubleclick_sell)

        self.ui.finances_button.clicked.connect(self.finances_button)
        self.ui.store_button.clicked.connect(self.store_button)
        self.ui.hospital_button.clicked.connect(self.do_hospital)

        self.ui.dealer_table.itemSelectionChanged.connect(self.toggle_buttons)
        self.ui.trenchcoat_table.itemSelectionChanged.connect(self.toggle_buttons)

        self.ui.area_1_button.clicked.connect(lambda: self.travel_to(0))
        self.ui.area_2_button.clicked.connect(lambda: self.travel_to(1))
        self.ui.area_3_button.clicked.connect(lambda: self.travel_to(2))
        self.ui.area_4_button.clicked.connect(lambda: self.travel_to(3))
        self.ui.area_5_button.clicked.connect(lambda: self.travel_to(4))
        self.ui.area_6_button.clicked.connect(lambda: self.travel_to(5))

        self.new_game()

        self.window.show()
        sys.exit(self.app.exec_())

    def new_game(self):
        new_game = NewGameDialog(self)
        action = new_game.exec()
        if action != 1:
            self.world = world.World()
            self.world.new_world(new_game.settings["name"],
                                 new_game.settings["length"],
                                 new_game.settings["start_world"])
            self.update()
        else:
            sys.exit()

    def finish_game(self):
        # TODO: high score list
        high_scores = HighScoresDialog(self)
        high_scores.dialog.exec()
        self.new_game()

    def process_ask(self, events):
        for event in events

    def travel_to(self, index):
        """Change current area and tick to next day."""
        self.world.travel_to(index)
        if world.rand_percent(config["cop_chance"]):
            self.do_fight()
        self.update()

    def finances_button(self):
        """Display finances dialog."""
        finances = FinancesDialog(self)
        finances.dialog.exec()

    def store_button(self):
        """Display store dialog."""
        store = StoreDialog(self)
        store.dialog.exec()

    def do_fight(self):
        fight = FightDialog(self)
        fight.exec()
        self.update()

    def do_hospital(self):
        self.world.visit_hospital()
        self.update()

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

    def update_areas(self):
        """Set up and toggle area buttons."""
        self.ui.world_layout.setTitle(self.world.world_name)

        if self.world.day[0] >= self.world.day[1]:
            self.ui.jet_button.setText("Finish!")
            self.ui.jet_button.setEnabled(True)
            self.ui.jet_button.clicked.connect(self.finish_game)
            for i in range(6):
                getattr(self.ui, "area_%s_button" % (i + 1)).setText(self.world.areas[i])
                getattr(self.ui, "area_%s_button" % (i + 1)).setEnabled(False)
        else:
            self.ui.jet_button.setText("Jet!")
            self.ui.jet_button.setEnabled(False)
            for i in range(6):
                getattr(self.ui, "area_%s_button" % (i + 1)).setText(self.world.areas[i])
                on = True
                if self.world.areas[i] == self.world.current_area:
                    on = False
                getattr(self.ui, "area_%s_button" % (i + 1)).setEnabled(on)

    def toggle_buttons(self):
        """Toggle all action buttons."""
        # short functions for setting button states
        def lookup_drug(selected):
            if selected:
                return [selected.name, common.drugs[selected.name]]
            else:
                return None

        dealer = lookup_drug(self.ui.dealer_table.currentItem())
        trenchcoat = lookup_drug(self.ui.trenchcoat_table.currentItem())

        can_buy = (dealer is not None and
                   dealer[0] in self.world.dealer.keys() and
                   self.world.player.cash >= self.world.dealer[dealer[0]] and
                   self.world.player.space_available() > 0)
        self.ui.buy_button.setEnabled(can_buy)

        can_sell = (trenchcoat is not None and
                    trenchcoat[0] in self.world.dealer.keys() and
                    trenchcoat[0] in self.world.player.drugs().keys())
        self.ui.sell_button.setEnabled(can_sell)

        can_dump = (trenchcoat is not None and
                    trenchcoat[0] in self.world.player.drugs().keys())
        self.ui.dump_button.setEnabled(can_dump)

        can_heal = (self.world.can_afford_hospital() and
                    self.world.player.is_damaged())
        self.ui.hospital_button.setEnabled(can_heal)

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
        # TODO: make a function
        weapon, ammo = self.world.player.weapon
        if weapon is not None:
            pretty_name = common.weapons[weapon]["name"]
            self.ui.weapon_equipped.setText("%s [%i]" % (pretty_name, ammo))
        else:
            self.ui.weapon_equipped.setText("Unarmed")

        self.toggle_buttons()
        self.populate_dealer()
        self.populate_trenchcoat()
        self.update_areas()
        self.render_log()

        if not self.world.player.is_alive():
            self.finish_game()

    def doubleclick_buy(self):
        if self.ui.buy_button.isEnabled(): self.do_transact("Buy")

    def doubleclick_sell(self):
        if self.ui.sell_button.isEnabled(): self.do_transact("Sell")

    def populate_dealer(self):
        """Populate dealer table with drugs on offer."""
        self.ui.dealer_table.setRowCount(len(self.world.dealer.keys()))
        drugs_sorted = sorted(self.world.dealer.keys())
        row = 0
        for name in drugs_sorted:
            pretty_name = common.drugs[name]["name"]
            name_cell = DrugWidget(pretty_name, name)
            price = self.world.dealer[name]

            if name in self.world.last_prices.keys():
                old_price = self.world.last_prices[name]
                if price > old_price:
                    name_icon = ":/glyph/icons/glyphicons-219-circle-arrow-top.png"
                elif price < old_price:
                    name_icon = ":/glyph/icons/glyphicons-220-circle-arrow-down.png"
                else:
                    name_icon = ":/glyph/icons/glyphicons-192-circle-minus.png"
            else:
                name_icon = ":/glyph/icons/glyphicons-192-circle-minus.png"
            name_cell.setIcon(QIcon(name_icon))

            price_cell = DrugWidget(str(price), name)
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
        if self.world.player.total_drugs() == self.world.player.trenchcoat["max"]:
            self.ui.max_drugs_label.setStyleSheet("color: red;")
        else:
            self.ui.max_drugs_label.setStyleSheet("color: black;")

    def render_log(self):
        html = "<html><body>"
        for msg in self.world.log:
            html = html + msg
            html = html + "</body></html>"
        self.ui.action_log_textedit.setHtml(html)
