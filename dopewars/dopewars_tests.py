import unittest

import common
#from dopewars import *

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_new(self):
        self.assertEqual(self.player.name, "John Cena")
        self.player.name = "Test Guy"
        self.assertEqual(self.player.name, "Test Guy")
        self.assertEqual(self.player.health, [100, 100])
        self.assertEqual(self.player.cash, 2000)
        self.assertEqual(self.player.loan, 2000)
        self.assertEqual(self.player.bank, 0)
        self.assertEqual(self.player.trenchcoat, {"max":100,"drugs":{}})

    # TODO: save/load

    def test_health(self):
        self.setUp()
        self.assertEqual(self.player.health, [100, 100])
        self.player.damage(10)
        self.assertEqual(self.player.health[0], 90)
        self.assertTrue(self.player.is_alive())
        self.player.damage(90)
        self.assertEqual(self.player.health[0], 0)
        self.assertFalse(self.player.is_alive())
        self.player.heal(50)
        self.assertTrue(self.player.is_alive())
        self.player.heal(100)
        self.assertEqual(self.player.health, [100, 100])

    def test_cash(self):
        self.setUp()
        self.assertEqual(self.player.cash, 2000)
        self.player.add_cash(100)
        self.assertEqual(self.player.cash, 2100)
        self.assertFalse(self.player.spend_cash(2101))
        self.assertEqual(self.player.cash, 2100)
        self.assertTrue(self.player.spend_cash(2100))
        self.assertEqual(self.player.cash, 0)

    def test_drugs(self):
        self.setUp()
        self.assertEqual(self.player.total_drugs(), 0)
        self.assertTrue(self.player.add_drug("weed",0,1))
        self.assertEqual(self.player.total_drugs(), 1)
        self.assertFalse(self.player.add_drug("weed",0,1000))
        self.assertEqual(self.player.total_drugs(), 1)
        self.assertTrue(self.player.add_drug("weed",0,1))
        self.assertEqual(self.player.total_drugs(), 2)
        self.assertEqual(self.player.trenchcoat["drugs"]["weed"]["count"], 2)
        self.assertFalse(self.player.buy_drug("weed",100,100))
        self.assertTrue(self.player.buy_drug("weed",100,1))
        self.assertFalse(self.player.remove_drug("weed",100))
        self.assertEqual(self.player.total_drugs(), 3)
        self.assertTrue(self.player.remove_drug("weed",1))
        self.assertEqual(self.player.total_drugs(), 2)
        self.assertTrue(self.player.remove_drug("weed",2))
        self.assertEqual(self.player.total_drugs(), 0)
        self.assertFalse(self.player.trenchcoat["drugs"].pop("weed",False))

    def test_loan(self):
        self.setUp()
        self.assertEqual(self.player.loan, 2000)
        self.player.add_loan(1000)
        self.assertEqual(self.player.loan, 3000)
        self.assertTrue(self.player.remove_loan(500))
        self.assertEqual(self.player.loan, 2500)
        self.assertFalse(self.player.remove_loan(3000))
        self.assertEqual(self.player.loan, 2500)
        self.assertTrue(self.player.remove_loan(2500))
        self.assertEqual(self.player.loan, 0)

    def test_bank(self):
        self.setUp()
        self.assertEqual(self.player.bank, 0)
        self.player.add_bank(1000)
        self.assertEqual(self.player.bank, 1000)
        self.assertTrue(self.player.remove_bank(500))
        self.assertEqual(self.player.bank, 500)
        self.assertFalse(self.player.remove_bank(1000))
        self.assertEqual(self.player.bank, 500)
        self.assertTrue(self.player.remove_bank(500))
        self.assertEqual(self.player.bank, 0)

class TestWorld(unittest.TestCase):
    def setUp(self):
        self.world = World()

    def test_setup(self):
        self.setUp()
        self.assertEqual(self.world.day, [1,1])
        self.assertEqual(self.world.areas, common.areas)
        self.assertTrue(isinstance(self.world.current_area, str))
        self.assertEqual(self.world.events, [])
        self.assertEqual(self.world.player, None)
        self.assertEqual(self.world.dealer, None)

    def test_new(self):
        self.setUp()
        self.world.new_world("Test Guy")
        self.assertEqual(self.world.day, [1,common.config["max_days"]])
        self.assertEqual(self.world.player.name, "Test Guy")
        self.world.new_world("Test Guy", 100)
        self.assertEqual(self.world.day, [1,100])

    # TODO: dealer
    # TODO: events
