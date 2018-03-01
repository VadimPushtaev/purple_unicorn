#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import random

from dice_parser import DiceParser
from dndbeyond_websearch import Searcher
from telegram.parsemode import ParseMode


class PurpleBot:
    MESSAGE_MAX_LENGTH = 4096

    def __init__(self):
        self.dice_parser = DiceParser()
        self.dnd_searcher = Searcher()

    @staticmethod
    def send_single_message(bot, chat_id, msg, mode=ParseMode.HTML):
        bot.sendMessage(chat_id=chat_id, text=msg, parse_mode=mode)

    @classmethod
    def send_message(cls, bot, chat_id, message):
        i = 0
        while i*cls.MESSAGE_MAX_LENGTH < len(message):
            cls.send_single_message(bot,
                                    chat_id,
                                    message[i*cls.MESSAGE_MAX_LENGTH:(i+1)*cls.MESSAGE_MAX_LENGTH])
            i = i + 1

    def send_hi_message(self, bot, chat_id, username):
        msgs = ["I'm crazy purple unicorn!!!!!",
                "Tell me 'bout the raaaaabits",
                "I am fluffy! Fluffy-fluffy-fluffy WOLF!",
                "Let me be a leader and I shall endeavor not to get all of us killed.",
                username + ', why are you talking to me?!']
        stickers = ['CAADAgADOgAD7sShCiK3hMJMvtbhAg',
                    'CAADAgADXwAD7sShCnji8rK8rHETAg',
                    'CAADAgADPgAD7sShChzV1O0OvX5KAg',
                    'CAADAgADPAAD7sShCkDkzhbVa_89Ag',
                    'CAADAgADNAAD7sShCuKlu6OUNCgmAg',
                    'CAADAgADQAAD7sShCgjoFTxdY7vVAg',
                    'CAADAgADpgIAAu7EoQpMlrIZAAFx37kC']
        size = len(msgs) + len(stickers)
        r = random.randint(0, size-1)
        if r < len(msgs):
            self.send_message(bot, chat_id, msgs[r])
        else:
            bot.sendSticker(chat_id=chat_id, sticker=stickers[r-len(msgs)])

    def send_help_message(self, bot, chat_id):
        self.send_message(bot,
                          chat_id,
                          '<code>/hi</code> - bot will say something\n' +
                          '<code>/roll</code> - roll dices. E.g.: /roll 2d6 + 5\n' +
                          '<code>/r</code> - shortcut for roll command\n' +
                          '<code>/percent</code> - equals to /roll 1d100\n' +
                          '<code>/init</code> - roll dices for initiative (or any saves), result will be sorted; you may also pass your bonuses with your names, e.g.: /init barbarian=2 cleric=0 orc1=1 orc2=1\n' +
                          '<code>/search</code> - look for given query on dndbeyond.com\n' +
                          '<code>/help</code> - this message')

    def generate_init(self, bot, chat_id, participants):
        parts_tuples = []
        width = 1
        for p in participants:
            roll = self.dice_parser.parse("1d20").value
            char = (p[0], roll+int(p[1]), int(p[1]), roll, self.dice_parser.parse("1d10").value)
            parts_tuples.append(char)
            if len(p[0]) > width:
                width = len(p[0])

        res = "Results:"
        for char in sorted(parts_tuples, key=lambda pt: (-pt[1], -pt[2], -pt[4])):
            res += '\n' + \
                   '<code>' + '{0: <{width}}'.format(char[0], width=width) + '</code> : ' + \
                   '<b>' + str(char[1]) + '</b> ' + \
                   '(' + str(char[3]) + ' ' + str(char[2]) + ' [' + str(char[4]) + '])'
            self.send_message(bot, chat_id, res)

    def roll_msg(self, bot, chat_id, username, expression):
        try:
            dice_result = self.dice_parser.parse(expression)
            answer = username + ' rolls:\n' + \
                dice_result.string + ' = <b>' + str(dice_result.value) + '</b>'
            self.send_message(bot, chat_id, answer)
        except KeyError:
            self.send_message(bot, chat_id, "I will not follow your commands!")
        except Exception:
            self.send_message(bot, chat_id, "Oh, c'mon, sweety, stop doing this")

    def flip_coin(self, bot, chat_id, username):
        dice_result = self.dice_parser.parse("1d2").value
        self.send_message(bot, chat_id, username + ": " + (u"орёл" if dice_result == 1 else u"решка"))

    def execute_search(self, bot, chat_id, query):
        if query is None or len(query) == 0:
            self.send_message(bot, chat_id, "I don't know what you are looking for")
            return
        results = self.dnd_searcher.search(query)
        compendium_results = [r for r in results if not r.breadcrumbs.upper().startswith("FORUM")]
        if len(compendium_results) == 0:
            self.send_message(bot, chat_id, "I've found nothing")
            return
        result_text = 'Found ' + str(len(compendium_results)) + ' result(s)\n\n' + \
                      self._search_result_short(compendium_results[0]) + '\n' + \
                      self._search_result_snippet(compendium_results[0]) + '\n\n' + \
                      '\n'.join(self._search_result_short(sr) for sr in compendium_results[1:5] if sr is not None)
        self.send_message(bot, chat_id, result_text)

    @staticmethod
    def _search_result_snippet(search_result):
        return '\n'.join(str(snippet) for snippet in search_result.snippets)

    @staticmethod
    def _search_result_short(search_result):
        return '<a href="' + search_result.url.replace("’", "%E2%80%99") + '">' + search_result.title + '</a> ' + \
               '(' + search_result.breadcrumbs + ')\n'
