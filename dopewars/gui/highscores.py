# dope wars qt high score dialog

from PyQt5.QtWidgets import QDialog

import qt_highscores_dialog


class HighScoresDialog():
    def __init__(self, parent):
        self.parent = parent
        self.dialog = QDialog(self.parent.window)
        self.ui = qt_highscores_dialog.Ui_Dialog()
        self.ui.setupUi(self.dialog)
