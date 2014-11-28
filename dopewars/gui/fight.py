# dope wars qt fight dialog

import random

from PyQt5.QtWidgets import QDialog

import common
import world

import qt_fight_dialog

config = {
    "run_chance": 20
}

class FightDialog(QDialog):
    def __init__(self, parent):
        super(QDialog, self).__init__(parent.window)
        self.parent = parent
        self.ui = qt_fight_dialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.give_up_button.clicked.connect(self.give_up)
        self.ui.shoot_button.clicked.connect(self.shoot)
        self.ui.run_button.clicked.connect(self.try_run)
        self.ui.dump_button.clicked.connect(self.dump_everything)

        self.cop_count = random.randint(1, 10)
        self.cop_health = [100, 100]

        self.update()

    def closeEvent(self, event):
        self.give_up()

    def set_status(self, msg):
        self.ui.status_label.setText(msg)

    def update(self):
        self.ui.cop_count_label.setText(str(self.cop_count))
        self.ui.cop_health_slider.setMaximum(self.cop_health[1])
        self.ui.cop_health_slider.setValue(self.cop_health[0])

        player = self.parent.world.player
        self.ui.health_slider.setMaximum(player.health[1])
        self.ui.health_slider.setValue(player.health[0])

        weapon, ammo = player.weapon
        if weapon is not None:
            pretty_name = common.weapons[weapon]["name"]
            self.ui.weapon_equipped.setText("%s [%i]" % (pretty_name, ammo))
        else:
            self.ui.weapon_equipped.setText("Unarmed")

        if player.has_drugs() or player.has_weapons():
            self.ui.dump_button.setEnabled(True)
        else:
            self.ui.dump_button.setEnabled(False)

        if weapon is not None and ammo > 0:
            self.ui.shoot_button.setEnabled(True)
        else:
            self.ui.shoot_button.setEnabled(False)

        if not self.parent.world.player.is_alive():
            self.done(999)

    def dump_everything(self):
        self.parent.world.player.dump_weapon()
        self.parent.world.player.dump_all_drugs()
        self.cop_turn("You dump your weapon and drugs.")
        self.update()

    def give_up(self):
        self.parent.world.add_log("You gave yourself up like a <b style='font-size: x-large; color: pink; text-decoration: underline'>BITCH</b><br>")
        if self.parent.world.player.has_drugs() or self.parent.world.player.has_weapons():
            self.parent.world.add_log("Officer Hardass says, \"I'll be taking that\"")
            self.parent.world.player.dump_weapon()
            self.parent.world.player.dump_all_drugs()
        else:
            self.parent.world.add_log("Officer Hardass pats you down and mumbles something about getting you next time")
        self.done(111)

    def try_run(self):
        if world.rand_percent(config["run_chance"]):
            self.parent.world.add_log("You got away!")
            self.done(333)
        else:
            self.cop_turn("You can't run from the law...")
        self.update()

    def cop_turn(self, prepend):
        if world.rand_percent(50):
            self.parent.world.player.damage(10)
            self.set_status(prepend + " Cops hit you for 10 damage!!!")
        else:
            self.set_status(prepend)

    def shoot(self):
        weapon = self.parent.world.player.weapon
        if weapon[0] is None or weapon[1] is None:
            return False

        self.cop_health[0] -= common.weapons[weapon[0]]["damage"]
        self.parent.world.player.weapon[1] -= 1

        if self.cop_health[0] <= 0:
            if self.cop_count <= 1:
                self.parent.world.add_log("<b style='font-size: x-large'>FUCK THE POLICE!</b>")
                self.done(222)
            else:
                self.cop_count -= 1
                self.cop_health[0] = self.cop_health[1]
                self.cop_turn("One down!")
        else:
            self.cop_turn("You hit the cop for %i damage!" % common.weapons[weapon[0]]["damage"])
        self.update()
