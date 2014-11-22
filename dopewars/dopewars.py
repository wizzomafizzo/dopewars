# dope wars

import random

import common
import player


class World():
    def __init__(self):
        self.day = [1, 1]  # current/max

        self.areas = common.areas
        self.current_area = random.choice(common.areas)

        self.events = []

        self.player = None
        self.dealer = None

    def new_world(self, player_name, max_days=common.config["max_days"]):
        """Create a brand new game."""
        self.day[1] = max_days

        self.player = player.Player()
        self.player.name = player_name

        self.new_dealer()

    # TODO: load world

    # dealer
    def new_dealer(self):
        self.dealer = {}
        for k, v in common.drugs.items():
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
