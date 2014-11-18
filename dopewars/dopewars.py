# dope wars

drugs = {
    "weed": {
        "name": "Weed",
        "base_price": 100
    }
}

class Player():
    def __init__(self, name):
        self.name = name
        self.health = [100, 100] # current/max

        self.cash = 0
        self.loan = 1000
        self.bank = 0

        self.trenchcoat = {
            "max": 100,
            "drugs": {}
        }

    def print_status(self):
        template = "%s\nHP: %i/%i\nCash: $%f\nLoan: $%f\nBank: $%f"
        print(template % (self.name,
                          self.health[0], self.health[1],
                          self.cash,
                          self.loan,
                          self.bank))

    def save(self):
        {
            "name": self.name,
            "health": self.health,
            "cash": self.cash,
            "loan": self.loan,
            "bank": self.bank,
            "trenchcoat": self.trenchcoat
        }

    def load(self, player):
        self.name = player["name"]
        self.healh = player["health"]
        self.cash = player["cash"]
        self.loan = player["loan"]
        self.bank = player["bank"]
        self.trenchcoat = player["trenchcoat"]

    # health
    def damage(self, amount):
        self.health[0] -= amount

    def heal(self, amount):
        self.health[0] += amount
        # don't heal more than max health
        if self.health[0] > self.health[1]:
            self.health[0] = self.health[1]

    def is_alive(self):
        if self.health[0] > 0:
            True
        else:
            False

    # cash
    def add_cash(self, amount):
        self.cash += amount

    def spend_cash(self, amount):
        # can't spend more than you have
        if self.cash >= amount:
            self.cash -= amount
            True
        else:
            False
