# dope wars qt new game dialog

import random

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QListWidgetItem

import common

import qt_newgame_dialog


class NewGameDialog(QDialog):
    def __init__(self, parent):
        super(QDialog, self).__init__(parent.window)
        self.parent = parent
        self.ui = qt_newgame_dialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.settings = {
            "name": "John Cena",
            "length": 30,
            "start_world": "Westeros"
        }

        self.ui.name.textChanged.connect(self.update)
        self.ui.world_list.currentItemChanged.connect(self.update)

        self.ui.day_15_button.clicked.connect(lambda: self.toggle_buttons(15))
        self.ui.day_30_button.clicked.connect(lambda: self.toggle_buttons(30))
        self.ui.day_60_button.clicked.connect(lambda: self.toggle_buttons(60))
        self.ui.day_90_button.clicked.connect(lambda: self.toggle_buttons(90))

        self.ui.quit_button.clicked.connect(lambda: self.done(1))
        self.ui.new_button.clicked.connect(lambda: self.done(0))

        self.populate_worlds()

    def closeEvent(self, event):
        self.done(1)

    def reject(self):
        self.done(1)

    def update(self):
        self.settings["name"] = self.ui.name.text()

        for length in 15, 30, 60, 90:
            checked = getattr(self.ui, "day_" + str(length) + "_button").isChecked()
            if checked:
                self.settings["length"] = length

        selected = self.ui.world_list.currentItem()
        if selected is not None:
            self.settings["start_world"] = selected.text()

        can_start = (self.settings["name"] != "" and
                     self.settings["length"] > 0 and
                     self.settings["start_world"] in common.worlds.keys())
        self.ui.new_button.setEnabled(can_start)

    def toggle_buttons(self, clicked_length):
        for length in 15, 30, 60, 90:
            if clicked_length == length:
                getattr(self.ui, "day_" + str(length) + "_button").setChecked(True)
            else:
                getattr(self.ui, "day_" + str(length) + "_button").setChecked(False)
        self.update()

    def populate_worlds(self):
        for world in sorted(common.worlds.keys()):
            self.ui.world_list.addItem(QListWidgetItem(world))
        self.ui.world_list.setCurrentRow(random.randint(0, len(common.worlds) - 1))
