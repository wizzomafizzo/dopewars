# dope wars core variables/functions


config = {
    "max_days": 30,
    "default_world": "Westeros"
}

events = {
    "bust": {
        "chance": 100,
        "kind": "bust",
        "msg": "%s prices have skyrocketed!<br>"
    },
    "boom": {
        "chance": 100,
        "kind": "boom",
        "msg": "A huge shipment of %s has come through, prices have hit rock bottom!<br>"
    }
}

drugs = {
    "acid": {
        "name": "Acid",
        "base_price": 2500
    },

    "cocaine": {
        "name": "Coke",
        "base_price": 20000
    },
    "crack": {
        "name": "Crack",
        "base_price": 2100
    },
    "ecstasy": {
        "name": "Ecstasy",
        "base_price": 30
    },
    "hash": {
        "name": "Hash",
        "base_price": 800
    },
    "ketamine": {
        "name": "Ketamine",
        "base_price": 1200
    },
    "oxy": {
        "name": "Oxy",
        "base_price": 650
    },
    "heroin": {
        "name": "Heroin",
        "base_price": 8000
    },
    "meth": {
        "name": "Meth",
        "base_price": 150
    },
    "mdma": {
        "name": "MDMA",
        "base_price": 3000
    },
    "mushrooms": {
        "name": "Shrooms",
        "base_price": 700
    },
    "lean": {
        "name": "Lean",
        "base_price": 15
    },
    "dmt": {
        "name": "DMT",
        "base_price": 500
    },
    "weed": {
        "name": "Weed",
        "base_price": 350
    }
}

weapons = {
    "slingshot": {
        "name": "Slingshot",
        "weapon_price": 100,
        "ammo_price": 1,
        "damage": 25
    },
    "handgun": {
        "name": "Handgun",
        "weapon_price": 1000,
        "ammo_price": 10,
        "damage": 70
    }
}

worlds = {
    "Westeros": ["The North",
                 "The Vale of Arryn",
                 "The Riverlands",
                 "The Westerlands",
                 "The Iron Islands",
                 "The Crownlands"],
    "Springfield": ["Moe's Tavern",
                    "Stoner's Pot Palace",
                    "Kwik-E-Mart",
                    "The Leftorium",
                    "Sleep Eazy Motel",
                    "Krusty Burger"]
}
