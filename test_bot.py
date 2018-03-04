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
        PurpleBot._get_rand = lambda self, max: ((yield  0), (yield  3), (yield 5), (yield 8))

        self.assertEqual('Results:\n' + \
                          '<code>abcde</code> : <b>8</b> (5 3 [8])\n' + \
                          '<code>cd   </code> : <b>8</b> (0 8 [3])\n' + \
                          '<code>a    </code> : <b>-5</b> (0 -5 [3])\n', self.bot.generate_init([("a", "-5"), ("abcde", "3"), ("cd", "8")]))

        # a 0 (-5) 3 -> -5 #3
        # abcde 5 (+3) 8 -> 8 #1
        # cd 0 (+8) 3 -> 8 #2


if __name__ == '__main__':
    unittest.main()
