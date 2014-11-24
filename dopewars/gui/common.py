# dope wars qt common widgets

from PyQt5.QtWidgets import QTableWidgetItem


class DrugWidget(QTableWidgetItem):
    """Extends drug table items to have name attribute."""
    def __init__(self, text, name):
        self.name = name
        QTableWidgetItem.__init__(self, text)
