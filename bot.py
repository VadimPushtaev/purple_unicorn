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
               '<code>/fc</code> - roll 1d2 and translate results in "head or tails"\n' + \
               '<code>/init</code> - roll dices for initiative (or any saves), result will be sorted; you may also pass your bonuses with your names, e.g.: /init barbarian=2 cleric=0 orc1=1 orc2=1\n' + \
               '<code>/search</code> - look for given query on dndbeyond.com\n' + \
               '<code>/help</code> - this message'
            
    def get_current_help(self, command):
        if command == 'hi':
            return '<code>/hi</code> - as an answer to this command bot will send random message OR random sticker from \'Unicorn Stella\'-pack'
        elif command == 'roll' or command == 'r':
            return '<code>/' + command + ' [expression - optional]</code> - bot will try to execute given expression.\n' + \
                   'Examples:\n' + \
                   '<code>/' + command + '</code> - roll 1d20\n' + \
                   '<code>/' + command + ' 3d6</code> - roll 1d6 die 3 times and summarize the result\n' + \
                   '<code>/' + command + ' (2+5)*3*(14-2)</code> - just calculate this expression\n' + \
                   '<code>/' + command + ' (2+1)d(17+4) + 2</code> - roll 1d21 die 3 times and add 2 to the sum\n' + \
                   '<code>/' + command + ' 3d6H2</code> - roll 1d6 die 3 times and get only 2 highest results (and sum them)\n' + \
                   '<code>/' + command + ' 4d8L1</code> - roll 1d8 die 4 times and get only 1 lowest result\n' + \
                   '<code>/' + command + ' d</code> - roll 1d20\n' + \
                   '<code>/' + command + ' (1d3)d(5d4H2)L(1d3+1)</code> - any allowed expressions can be combined\n'
        elif command == 'percent':
            return '<code>/percent</code> - roll 1d100'
        elif command == 'init':
            return '<code>/init [list of characters - required, their bonuses - optional]</code> - roll initiative and sort results\n' + \
                   'Examples:\n' + \
                   '<code>/init player1 player2</code> - roll initiative (1d20) for each, initiative bonus is 0 for both\n' + \
                   '<code>/init player1=5 player2 player3=-1</code> - roll initiative (1d20) for each, add initiative bonus: 5 for player1, 0 for player2 and -1 for player3\n' + \
                   'Results look like this:\n' + \
                   '<code>player4 : 23 (18 5 [2])</code> - it means that total result for <code>player4</code> is <code>23</code>: <code>18</code> was rolled and <code>5</code> is a bonus. <code>[2]</code> is additional roll for cases when 2 or more players have similar results and we need just to order them.'
        elif command == 'search':
            return '<code>/search [query - required]</code> - go to dndbeyond.com and look for results'
        elif command == 'help':
            return '<code>/help [command - optional]</code> - get help\n' + \
                   'Examples:\n' + \
                   '<code>/help</code> - get list of all commands with tiny descriptions\n' + \
                   '<code>/help roll</code> - get more help about \'/roll\' command (you can use any of allowed command names)'
        else:
            return 'Nobody can help you, you are doomed. [' + command + '] is wrong command.'

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
