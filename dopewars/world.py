# dope wars world

import random
import math
import pickle

import common
import player
import events

config = {
    "price_shift": 0.3,
    "min_drugs": 10,
    "loan_interest": 15,
    "old_lady_chance": 20,
    "rand_event_chance": 40
}

templates = {
    "old_lady_bust": "<b style='color: purple'>I heard there's going to be a big %s bust tomorrow!</b><br>",
    "new_game": "<h2>A new game begins!</h2> It's day <b>%i</b> of <b>%i</b> and <b style='color: red; font-size: large'>you've got a loan to pay off!</b>",
    "new_day": "It's day <b>%i</b>"
}

def rand_percent(percent):
    if percent > 100:
        percent = 100
    result = random.randint(1, 100)
    if result > percent:
        return False
    else:
        return True

class World():
    def __init__(self):
        self.day = [1, 30]  # current/max

        self.world_name = None
        self.areas = None
        self.current_area = None

        self.events = []
        self.last_prices = {}
        self.log = []

        self.highscores = {15: [], 30: [], 60: [], 90: []}

        self.player = None
        self.dealer = None

    def old_lady(self):
        name = events.random_drug()
        self.add_event("bust", name, 1)
        self.add_log(templates["old_lady_bust"] % common.drugs[name]["name"])

    def add_log(self, msg):
        self.log.append(msg)

    def clear_log(self):
        self.log = []

    def new_world(self, player_name,
                  max_days=common.config["max_days"],
                  world=common.config["default_world"]):
        """Create a brand new game."""
        self.day[1] = max_days

        self.player = player.Player()
        self.player.name = player_name

        self.world_name = world
        self.areas = common.worlds[self.world_name]
        self.current_area = random.choice(self.areas)

        self.new_dealer()

        self.clear_log()
        self.add_log(templates["new_game"] % (self.day[0], self.day[1]))

    def next_day(self):
        self.clear_log()
        self.day[0] += 1
        self.update_last_prices()
        self.new_dealer()
        self.update_loan()
        self.add_log(templates["new_day"] % self.day[0])

        if rand_percent(config["old_lady_chance"]):
            self.old_lady()

        if rand_percent(config["rand_event_chance"]):
            self.add_event(events.pick_event(), None, 0)

        ask = []
        for event in self.process_events():
            if event is not None:
                ask.append(event)
        return ask


    def update_last_prices(self):
        for drug in self.dealer.keys():
            dealer_price = self.dealer[drug]
            self.last_prices[drug] = dealer_price

    def travel_to(self, index):
        self.current_area = self.areas[index]
        return self.next_day()

    def dump_drug(self, name, count):
        self.player.remove_drug(name, count)

    def hospital_cost(self):
        # TODO: move to config
        return (self.player.health[1] - self.player.health[0]) * 10

    def can_afford_hospital(self):
        if self.player.cash >= self.hospital_cost():
            return True
        else:
            return False

    def visit_hospital(self):
        if self.can_afford_hospital():
            self.player.spend_cash(self.hospital_cost())
            self.player.heal_all()
            return True
        else:
            return False

    # weapons
    def buy_weapon(self, name):
        price = common.weapons[name]["weapon_price"]
        if self.player.spend_cash(price):
            self.player.set_weapon(name)
            return True
        else:
            return False

    def buy_ammo(self, name):
        price = common.weapons[name]["ammo_price"]
        if self.player.spend_cash(price):
            self.player.add_ammo(10)
            return True
        else:
            return False

    # dealer
    def make_drug_price(self, name):
        base_price = common.drugs[name]["base_price"]
        difference = math.floor(base_price * config["price_shift"])
        return base_price + random.randint(0 - difference, difference)

    def new_dealer(self):
        self.dealer = {}
        drug_list = list(common.drugs.keys())
        drug_count = random.randint(config["min_drugs"], len(drug_list) - 1)
        random.shuffle(drug_list)

        for drug in drug_list[0:drug_count]:
            self.dealer[drug] = self.make_drug_price(drug)

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
    def add_event(self, name, args, wait=0):
        """Queue up a new event."""
        self.events.append({"name": name, "args": args, "wait": wait})

    def events_now(self):
        """Return queued events due now."""
        return self.sort_events()[0]

    def events_future(self):
        """Return queued events next turn or later."""
        return self.sort_events()[1]

    def do_event(self, event):
        return events.do_event(self, event["name"], event["args"])

    def process_events(self):
        events = self.events
        self.events = []
        for event in events:
            if event["wait"] > 0:
                self.add_event(event["name"], event["args"], event["wait"] - 1)
            else:
                yield self.do_event(event)

    # bank
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

    # loan
    def pay_loan(self):
        if self.player.loan > 0 and self.player.cash >= self.player.loan:
            self.player.spend_cash(self.player.loan)
            self.player.loan = 0
            return True
        else:
            return False

    def take_loan(self, amount):
        if self.player.loan == 0:
            self.player.add_loan(amount)
            self.player.add_cash(amount)
            self.update_loan()
            return True
        else:
            return False

    def update_loan(self):
        if self.player.loan > 0:
            interest = math.floor((self.player.loan / 100) * config["loan_interest"])
            self.player.loan += interest
