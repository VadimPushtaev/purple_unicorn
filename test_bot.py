#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
#from unittest.mock import MagicMock

from bot import PurpleBot


class BotTestCase(TestCase):
    bot = PurpleBot()

    def setUp(self):
        PurpleBot._get_rand = lambda self, max: int(max)

    def test_roll(self):
        PurpleBot._get_rand = lambda self, max: 9
        self.assertEqual(10, self.bot._get_roll(20))

    def test_get_random_message(self):
        PurpleBot._get_rand = lambda self, max: 0
        self.assertEqual("I'm crazy purple unicorn!!!!!", self.bot.get_random_greetings("ABC"))
        PurpleBot._get_rand = lambda self, max: 4
        self.assertEqual('ABC, why are you talking to me?!', self.bot.get_random_greetings("ABC"))

    def test_init(self):
        rolled = iter([
            0, 3,  # a
            7, 8,  # ab
            2, 1   # c
        ])
        PurpleBot._get_rand = lambda self, max: next(rolled)

        self.assertEqual('Results:\n' +
                         '<code>c </code> : <b>11</b> (3 8 [2])\n' +
                         '<code>ab</code> : <b>11</b> (8 3 [9])\n' +
                         '<code>a </code> : <b>-4</b> (1 -5 [4])', self.bot.generate_init([("a", "-5"), ("ab", "3"), ("c", "8")]))

        # name | result | bonus | roll | additional roll
        # a    | -4     | -5    | 1    | 4
        # ab   | 11     | 3     | 8    | 9
        # c    | 11     | 8     | 3    | 2


if __name__ == '__main__':
    unittest.main()
