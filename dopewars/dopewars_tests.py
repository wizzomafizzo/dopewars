import unittest

from dopewars import *

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_new(self):
        self.assertEqual(self.player.name, "John Cena")
        self.player.name = "Test Guy"
        self.assertEqual(self.player.name, "Test Guy")

    def test_health(self):
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
        self.assertEqual(self.player.cash, 0)
        self.player.add_cash(100)
        self.assertEqual(self.player.cash, 100)
        self.assertFalse(self.player.spend_cash(101))
        self.assertEqual(self.player.cash, 100)
        self.assertTrue(self.player.spend_cash(100))
        self.assertEqual(self.player.cash, 0)
