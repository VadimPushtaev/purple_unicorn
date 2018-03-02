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
        self.assertEquals("I'm crazy purple unicorn!!!!!", self.bot.get_random_greetings("ABC"))
        PurpleBot._get_rand = lambda self, max: 4
        self.assertEquals('ABC, why are you talking to me?!', self.bot.get_random_greetings("ABC"))

    def test_init(self):
        PurpleBot._get_rand = lambda self, max: ((yield  0), (yield  3), (yield 5), (yield 8))


if __name__ == '__main__':
    unittest.main()
