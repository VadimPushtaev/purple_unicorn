#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
from collections import namedtuple
from unittest.mock import patch

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

    def test_roll_msg(self):
        dice_result = namedtuple('DiceResult', ['string', 'value'])
        p = patch("dice_parser.DiceParser.parse")
        bot = PurpleBot()
        p.start().return_value = dice_result("a", 10)

        self.assertEqual("A rolls:\na = <b>10</b>", bot.roll_msg(username="A", expression="expression"))

    def test_flip_coin(self):
        rolled = iter([0, 1, 0, 1])
        PurpleBot._get_rand = lambda self, max: next(rolled)
        bot = PurpleBot()
        self.assertEqual("AAAA: орёл", bot.flip_coin("AAAA"))
        self.assertEqual("AAAA: решка", bot.flip_coin("AAAA"))
        self.assertEqual("AAAA: орёл", bot.flip_coin("AAAA"))
        self.assertEqual("AAAA: решка", bot.flip_coin("AAAA"))

    def test_search(self):
        search_result = namedtuple("SearchResult", ['url', 'title', 'breadcrumbs', 'snippets'])
        search_results = [
            search_result("url1", "title1", "compendium -> cat1", ["sn1", "sn2", "", "sn3"]),
            search_result("url2", "title2", "spells -> cat2", ["sn4", "sn5", "", "sn6"]),
            search_result("url3", "title3", "forum -> cat3", ["sn7", "sn8", "", "sn9"]),
            search_result("url4", "title4", "monster -> cat", ["sn10", "sn11", "", "sn12"])
        ]
        p = patch("dndbeyond_websearch.Searcher.search")
        bot = PurpleBot()
        p.start().return_value = search_results

        self.assertEqual("Found 3 result(s)\n\n" +
                         "<a href=\"url1\">title1</a> (compendium -> cat1)\n\n" +
                         "sn1\n" +
                         "sn2\n" +
                         "\n" +
                         "sn3\n\n" +
                         "<a href=\"url2\">title2</a> (spells -> cat2)\n\n" +
                         "<a href=\"url4\">title4</a> (monster -> cat)\n", bot.execute_search("query"))


if __name__ == '__main__':
    unittest.main()
