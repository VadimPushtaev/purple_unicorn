#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import random

from dice_parser import DiceParser
from dndbeyond_websearch import Searcher


class PurpleBot:
    def __init__(self):
        self.dice_parser = DiceParser()
        self.dnd_searcher = Searcher()

    def _get_rand(self, max):
        return random.randint(0, max)

    def _get_roll(self, die):
        return 1 + self._get_rand(die - 1)

    def get_random_greetings(self, username):
        msgs = ["I'm crazy purple unicorn!!!!!",
                "Tell me 'bout the raaaaabits",
                "I am fluffy! Fluffy-fluffy-fluffy WOLF!",
                "Let me be a leader and I shall endeavor not to get all of us killed.",
                username + ', why are you talking to me?!']
        r = self._get_rand(len(msgs) - 1)
        return msgs[r]

    def get_random_sticker(self):
        stickers = ['CAADAgADOgAD7sShCiK3hMJMvtbhAg',
                    'CAADAgADXwAD7sShCnji8rK8rHETAg',
                    'CAADAgADPgAD7sShChzV1O0OvX5KAg',
                    'CAADAgADPAAD7sShCkDkzhbVa_89Ag',
                    'CAADAgADNAAD7sShCuKlu6OUNCgmAg',
                    'CAADAgADQAAD7sShCgjoFTxdY7vVAg',
                    'CAADAgADpgIAAu7EoQpMlrIZAAFx37kC']
        r = self._get_rand(len(stickers)-1)
        return stickers[r]

    def get_help_message(self):
        return '<code>/hi</code> - bot will say something\n' + \
               '<code>/roll</code> - roll dices. E.g.: /roll 2d6 + 5\n' + \
               '<code>/r</code> - shortcut for roll command\n' + \
               '<code>/percent</code> - equals to /roll 1d100\n' + \
               '<code>/init</code> - roll dices for initiative (or any saves), result will be sorted; you may also pass your bonuses with your names, e.g.: /init barbarian=2 cleric=0 orc1=1 orc2=1\n' + \
               '<code>/search</code> - look for given query on dndbeyond.com\n' + \
               '<code>/help</code> - this message'

    def generate_init(self, participants):
        parts_tuples = []
        width = 1
        for p in participants:
            roll = self._get_roll(20)
            # name | result | bonus | roll | additional roll
            char = (p[0], roll+int(p[1]), int(p[1]), roll, self._get_roll(10))
            parts_tuples.append(char)
            if len(p[0]) > width:
                width = len(p[0])

        res = "Results:"
        for char in sorted(parts_tuples, key=lambda pt: (-pt[1], -pt[2], -pt[4])):
            res += '\n' + \
                   '<code>' + '{0: <{width}}'.format(char[0], width=width) + '</code> : ' + \
                   '<b>' + str(char[1]) + '</b> ' + \
                   '(' + str(char[3]) + ' ' + str(char[2]) + ' [' + str(char[4]) + '])'
        return res

    def roll_msg(self, username, expression):
        try:
            dice_result = self.dice_parser.parse(expression)
            answer = username + ' rolls:\n' + \
                dice_result.string + ' = <b>' + str(dice_result.value) + '</b>'
            return answer
        except KeyError:
            return "I will not follow your commands!"
        except Exception:
            return "Oh, c'mon, sweety, stop doing this"

    def flip_coin(self, username):
        dice_result = self._get_roll(2)
        return username + ": " + ("орёл" if dice_result == 1 else "решка")

    def execute_search(self, query):
        if query is None or len(query) == 0:
            return "I don't know what you are looking for"
        results = self.dnd_searcher.search(query)
        compendium_results = [r for r in results if not r.breadcrumbs.upper().startswith("FORUM")]
        if len(compendium_results) == 0:
            return "I've found nothing"
        return 'Found ' + str(len(compendium_results)) + ' result(s)\n\n' + \
               self._search_result_short(compendium_results[0]) + '\n' + \
               self._search_result_snippet(compendium_results[0]) + '\n\n' + \
               '\n'.join(self._search_result_short(sr) for sr in compendium_results[1:5] if sr is not None)

    @staticmethod
    def _search_result_snippet(search_result):
        return '\n'.join(str(snippet) for snippet in search_result.snippets)

    @staticmethod
    def _search_result_short(search_result):
        return '<a href="' + search_result.url.replace("’", "%E2%80%99") + '">' + search_result.title + '</a> ' + \
               '(' + search_result.breadcrumbs + ')\n'
