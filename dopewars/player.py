# dope wars player

import common


class Player():
    def __init__(self):
        self.name = "John Cena"
        self.health = [100, 100]  # current/max

        self.cash = 2000
        self.loan = 5500
        self.bank = 0

        self.weapon = [None, 0]  # name/ammo

        self.trenchcoat = {
            "max": 100,
            "drugs": {}
        }

    # prettu printing
    def print_trenchcoat(self):
        print("Max: %s" % (self.trenchcoat["max"]))
        for k, v in self.trenchcoat["drugs"].items():
            print("%s x%i ($%f)" % (common.drugs[k]["name"],
                                    v["count"],
                                    v["price"]))

    def print_status(self):
        template = "%s\nHP: %i/%i\nCash: $%f\nLoan: $%f\nBank: $%f"
        print(template % (self.name,
                          self.health[0], self.health[1],
                          self.cash,
                          self.loan,
                          self.bank))

    # save/load
    def save(self):
        """Return entire player instance as a map."""
        return {
            "name": self.name,
            "health": self.health,
            "cash": self.cash,
            "loan": self.loan,
            "bank": self.bank,
            "trenchcoat": self.trenchcoat
        }

    def load(self, player):
        """Load exported player into current instance."""
        self.name = player["name"]
        self.healh = player["health"]
        self.cash = player["cash"]
        self.loan = player["loan"]
        self.bank = player["bank"]
        self.trenchcoat = player["trenchcoat"]

    # health
    def damage(self, amount):
        """Reduce player health by amount."""
        self.health[0] -= amount
        if self.health[0] < 0:
            self.health[0] = 0
        return True

    def heal(self, amount):
        """Increase player health by amount."""
        self.health[0] += amount
        # don't heal more than max health
        if self.health[0] > self.health[1]:
            self.health[0] = self.health[1]
        return True

    def is_alive(self):
        """Return True if player is alive, has more than 0 health."""
        if self.health[0] > 0:
            return True
        else:
            return False

    # cash
    def add_cash(self, amount):
        """Give player amount of cash."""
        self.cash += amount
        return True

    def spend_cash(self, amount):
        """If player has enough cash, deduct amount. False if not enough."""
        # can't spend more than you have
        if self.cash >= amount:
            self.cash -= amount
            return True
        else:
            return False

    # drugs
    def total_drugs(self):
        """Return total number of all drugs in trenchcoat."""
        total = 0
        for drug in self.trenchcoat["drugs"].values():
            total += drug["count"]
        return total

    def add_drug(self, name, price, count):
        """Add any drug to trenchcoat at no cost, False if not enough space."""
        if name not in common.drugs.keys():
            raise Exception("Drug type '%s' does not exist" % (name))

        # check if there's enough space
        if count + self.total_drugs() > self.trenchcoat["max"]:
            return False

        if name in self.trenchcoat["drugs"].keys():
            count += self.trenchcoat["drugs"][name]["count"]

        self.trenchcoat["drugs"][name] = {
            "price": price,
            "count": count
        }

        return True

    def buy_drug(self, name, price, count):
        """Add any drug to trenchcoat at cost, False if not enough cash."""
        if self.spend_cash(price * count):
            self.add_drug(name, price, count)
            return True
        else:
            return False

    def remove_drug(self, name, count):
        """Remove number of drug from trenchcoat, False if too many."""
        if name not in self.trenchcoat["drugs"].keys():
            return False

        new_count = self.trenchcoat["drugs"][name]["count"] - count
        if new_count > 0:
            self.trenchcoat["drugs"][name]["count"] = new_count
            return True
        elif new_count == 0:
            self.trenchcoat["drugs"].pop(name)
            return True
        else:
            return False

    def dump_all_drugs(self):
        self.trenchcoat["drugs"] = {}
        return True

    # loans
    def add_loan(self, amount):
        """Add amount to player loan."""
        self.loan += amount
        return True

    def remove_loan(self, amount):
        """Remove amount from player loan, False if too much."""
        if amount <= self.loan:
            self.loan -= amount
            return True
        else:
            return False

    # bank
    def add_bank(self, amount):
        """Add amount to player bank."""
        self.bank += amount

    def remove_bank(self, amount):
        """Remove amount from player bank, False if too much."""
        if amount <= self.bank:
            self.bank -= amount
            return True
        else:
            return False

    # weapons
    def set_weapon(self, name):
        if name in common.weapons.keys():
            self.weapon = [name, 0]
            return True
        else:
            return False

    def add_ammo(self, amount):
        self.weapon[1] += amount
        return True

    def shoot_weapon(self):
        if self.weapon[1] > 0:
            self.weapon[1] -= 1
            return True
        else:
            return False

    def dump_weapon(self):
        self.weapon = [None, 0]
        return True
