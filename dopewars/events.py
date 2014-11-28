# dope wars events

import random
import math

import common


def random_drug():
    return random.choice(list(common.drugs.keys()))

def do_event(world, name, args):
    events_map[name](world, args)

def do_trenchcoat(world, args):
    return {
        "ask": "Buy some doot for doot?",
        "do":
    }

def do_bust(world, args):
    multiplier = 3
    if args is not None:
        dealer_pick = args
        price = world.make_drug_price(args)
    else:
        dealer_pick = random.choice(list(world.dealer.keys()))
        price = world.dealer[dealer_pick]
    new_price = price * multiplier
    world.dealer[dealer_pick] = new_price
    world.add_log(common.events["bust"]["msg"] % (common.drugs[dealer_pick]["name"]))
    return None

def do_boom(world, args):
    dealer_pick = random.choice(list(world.dealer.keys()))
    price = world.dealer[dealer_pick]
    new_price = math.floor(price * 0.2)
    world.dealer[dealer_pick] = new_price
    world.add_log(common.events["boom"]["msg"] % (common.drugs[dealer_pick]["name"]))
    return None

def pick_event():
    events = list(common.events.keys())
    picked = random.choice(events)
    return picked

events_map = {
    "bust": do_bust,
    "boom": do_boom
}
