#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
#from unittest.mock import MagicMock

from bot import PurpleBot


class BotTestCase(TestCase):
    bot = PurpleBot()

    def setUp(self):
        PurpleBot._get_rand = lambda self, max: int(max/2)

    def test_roll(self):
        self.assertEqual(10, self.bot._get_roll(20))


if __name__ == '__main__':
    unittest.main()
