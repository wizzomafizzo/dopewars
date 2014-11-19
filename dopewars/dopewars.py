# dope wars

drugs = {
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

    def print_status(self):
        template = "%s\nHP: %i/%i\nCash: $%f\nLoan: $%f\nBank: $%f"
        print(template % (self.name,
                          self.health[0], self.health[1],
                          self.cash,
                          self.loan,
                          self.bank))

    def save(selfa):
        """Return entire player instance as a map."""
        {
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
        """If player has enough cash, deduct from total and return True, else False."""
        # can't spend more than you have
        if self.cash >= amount:
            self.cash -= amount
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

    def new_world(self, player_name, max_days=30):
        """Create a brand new game."""
        self.day[1] = max_days
        self.player = Player()
        self.player.name = player_name

    # TODO: load world

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
