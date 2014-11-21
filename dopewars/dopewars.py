# dope wars

import random

DRUGS = {
    "weed": {
        "name": "Weed",
        "base_price": 100
    }
}

class Player():
    def __init__(self):
        self.name = "John Cena"
        self.health = [100, 100] # current/max

        self.cash = 0
        self.loan = 1000
        self.bank = 0

        self.trenchcoat = {
            "max": 100,
            "drugs": {}
        }

        # TODO: weapons

    # prettu printing
    def print_trenchcoat(self):
        print("Max: %s" % (self.trenchcoat["max"]))
        for k, v in self.trenchcoat["drugs"].items():
            print("%s x%i ($%f)" % (DRUGS[k]["name"],
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

    def heal(self, amount):
        """Increase player health by amount."""
        self.health[0] += amount
        # don't heal more than max health
        if self.health[0] > self.health[1]:
            self.health[0] = self.health[1]

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

    def spend_cash(self, amount):
        """If player has enough cash, deduct from total. False if not enough."""
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
        """Add any drug to trenchcoat at cost, False if not enough space/cash."""
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

    # loans
    def add_loan(self, amount):
        """Add amount to player loan."""
        self.loan += amount

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

class World():
    def __init__(self):
        self.day = [1, 30] # current/max

        self.current_area = "foo"
        self.areas = ["foo", "bar"]

        self.events = []

        self.player = None
        self.dealer = None

    def new_world(self, player_name, max_days=30):
        """Create a brand new game."""
        self.day[1] = max_days

        self.player = Player()
        self.player.name = player_name

        self.new_dealer()

    # TODO: load world

    # dealer
    def new_dealer(self):
        self.dealer = {}
        for k, v in DRUGS.items():
            # TODO: shouldn't be harcoded (or so simple)
            self.dealer[k] = random.randint(1, 3) * v["base_price"]

    def buy_from_dealer(self, name, count=1):
        # check they actually have the drug
        if name in self.dealer.keys():
            price = self.dealer[name]
            return self.player.buy_drug(name, price, count)
        else:
            return False

    # events
    def add_event(self, name, wait=0):
        """Queue up a new event."""
        self.events.append({"name": name, "wait": wait})

    def sort_events(self):
        """Return a tuple of queued events sorted now[0] and future[1]."""
        now = []
        future = []
        for event in self.events:
            if event["wait"] <= 0:
                now.append(event)
            else:
                future.append(event)
        return now, future

    def events_now(self):
        """Return queued events due now."""
        return self.sort_events()[0]

    def events_future(self):
        """Return queued events next turn or later."""
        return self.sort_events()[1]
