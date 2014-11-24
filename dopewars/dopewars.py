# dope wars

import random
import math

import common
import player


class World():
    def __init__(self):
        self.day = [1, 1]  # current/max

        self.world_name = common.areas[0]
        self.areas = common.areas[1:]
        self.current_area = random.choice(self.areas)

        self.loan_interest = 15

        self.events = []

        self.player = None
        self.dealer = None

    def new_world(self, player_name, max_days=common.config["max_days"]):
        """Create a brand new game."""
        self.day[1] = max_days

        self.player = player.Player()
        self.player.name = player_name

        self.new_dealer()

    def dump_drug(self, name, count):
        self.player.remove_drug(name, count)

    def deposit_bank(self, amount):
        if self.player.spend_cash(amount):
            self.player.add_bank(amount)
            return True
        else:
            return False

    def withdraw_bank(self, amount):
        if self.player.remove_bank(amount):
            self.player.add_cash(amount)
            return True
        else:
            return False

    def update_loan(self):
        if self.player.loan > 0:
            interest = math.floor((self.player.loan / 100) * self.loan_interest)
            self.player.loan += interest

    def next_day(self):
        self.day[0] += 1
        self.new_dealer()
        self.update_loan()
        # TODO: process events

    def travel_to(self, index):
        self.current_area = self.areas[index]
        self.next_day()

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

    def sell_to_dealer(self, name, count=1):
        dealer_drugs = self.dealer.keys()
        player_drugs = self.player.trenchcoat["drugs"].keys()
        if name in dealer_drugs and name in player_drugs:
            price = self.dealer[name]
            if self.player.remove_drug(name, count):
                self.player.add_cash(count * price)
                return True
            else:
                return False
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
