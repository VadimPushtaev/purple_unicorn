#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import logging
import random

from dice_parser import DiceParser
from dndbeyond_websearch import Searcher
from telegram.parsemode import ParseMode

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARN)
logger = logging.getLogger(__name__)
dice_parser = DiceParser()
dnd_searcher = Searcher()

MESSAGE_MAX_LENGTH = 4096


class PurpleBot:
    def __init__(self):
        pass

    @staticmethod
    def send_single_message(bot, chat_id, msg, mode=ParseMode.HTML):
        bot.sendMessage(chat_id=chat_id, text=msg, parse_mode=mode)

    @staticmethod
    def send_message(bot, chat_id, message):
        i = 0
        while i*MESSAGE_MAX_LENGTH < len(message):
            PurpleBot.send_single_message(bot,
                                          chat_id,
                                          message[i*MESSAGE_MAX_LENGTH:(i+1)*MESSAGE_MAX_LENGTH])
            i = i + 1

    @staticmethod
    def hi_command(bot, update):
        user = update.message.from_user
        name = user.first_name
        if name is None:
            name = user.username

        msgs = ["I'm crazy purple unicorn!!!!!",
                "Tell me 'bout the raaaaabits",
                "I am fluffy! Fluffy-fluffy-fluffy WOLF!",
                "Let me be a leader and I shall endeavor not to get all of us killed.",
                name + ', why are you talking to me?!']
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
            PurpleBot.send_message(bot, update.message.chat_id, msgs[r])
        else:
            bot.sendSticker(chat_id=update.message.chat_id, sticker=stickers[r-len(msgs)])

    @staticmethod
    def help_command(bot, update):
        PurpleBot.send_message(bot,
                               update.message.chat_id,
                               '<code>/hi</code> - bot will say something\n' +
                               '<code>/roll</code> - roll dices. E.g.: /roll 2d6 + 5\n' +
                               '<code>/r</code> - shortcut for roll command\n' +
                               '<code>/percent</code> - equals to /roll 1d100\n' +
                               '<code>/init</code> - roll dices for initiative (or any saves), result will be sorted; you may also pass your bonuses with your names, e.g.: /init barbarian=2 cleric=0 orc1=1 orc2=1\n' +
                               '<code>/search</code> - look for given query on dndbeyond.com\n' +
                               '<code>/help</code> - this message')

    @staticmethod
    def init_command(bot, update):
        msg = update.message.text[6:]
        parts = msg.split(' ')
        parts_tuples = []
        width = 1
        for p in parts:
            if len(p) > 0:
                pairs = p.split('=')
                if len(pairs) == 2:
                    roll = PurpleBot.roll_d(20)
                    char = (pairs[0], roll+int(pairs[1]), int(pairs[1]), roll, PurpleBot.roll_d(10))
                    parts_tuples.append(char)
                    if len(pairs[0]) > width:
                        width = len(pairs[0])
        res = "Results:"
        for char in sorted(parts_tuples, key=lambda pt: (-pt[1], -pt[2], -pt[4])):
            res += '\n' + \
                   '<code>' + '{0: <{width}}'.format(char[0], width=width) + '</code> : ' + \
                   '<b>' + str(char[1]) + '</b> ' + \
                   '(' + str(char[3]) + ' ' + str(char[2]) + ' [' + str(char[4]) + '])'
            PurpleBot.send_message(bot, update.message.chat_id, res)

    @staticmethod
    def roll_msg(source_msg, bot, update):
        try:
            dice_result = dice_parser.parse(source_msg)
            answer = update.message.from_user.username + ' rolls:\n' + \
                dice_result.string + ' = <b>' + str(dice_result.value) + '</b>'
            PurpleBot.send_message(bot, update.message.chat_id, answer)
        except KeyError:
            PurpleBot.send_message(bot, update.message.chat_id, "I will not follow your commands!")
        except Exception:
            PurpleBot.send_message(bot, update.message.chat_id, "Oh, c'mon, sweety, stop doing this")

    @staticmethod
    def roll_command(bot, update):
        msg_text = update.message.text.strip()
        ndx = msg_text.find(' ')
        if ndx == -1:
            PurpleBot.roll_msg("1d20", bot, update)
        else:
            msg = msg_text[ndx:]
            PurpleBot.roll_msg(msg, bot, update)

    @staticmethod
    def roll_percent(bot, update):
        PurpleBot.roll_msg("1d100", bot, update)

    @staticmethod
    def roll_d(d):
        return random.randint(1, d)

    @staticmethod
    def search_command(bot, update):
        msg_text = update.message.text[8:].strip()
        if len(msg_text) == 0:
            PurpleBot.send_message(bot, update.message.chat_id, "I don't know what you are looking for")
            return
        results = dnd_searcher.search(msg_text)
        compendium_results = [r for r in results if not r.breadcrumbs.upper().startswith("FORUM")]
        if len(compendium_results) == 0:
            PurpleBot.send_message(bot, update.message.chat_id, "I've found nothing")
            return
        result_text = 'Found ' + str(len(compendium_results)) + ' result(s)\n\n' + \
                      str(PurpleBot.format_search_result_full(compendium_results[0])) + '\n\n' + \
                      '\n'.join(PurpleBot.format_search_result_short(sr) for sr in compendium_results[1:5] if sr is not None)
        PurpleBot.send_message(bot, update.message.chat_id, result_text)

    @staticmethod
    def format_search_result_full(search_result):
        return '<b>' + search_result.title + '</b>\n' + \
               search_result.url.replace("’", "%E2%80%99") + '\n' + \
               search_result.breadcrumbs + '\n' + \
               '\n'.join(str(snippet) for snippet in search_result.snippets)

    @staticmethod
    def format_search_result_short(search_result):
        return '<a href="' + search_result.url.replace("’", "%E2%80%99") + '">' + search_result.title + '</a> ' + \
               '(' + search_result.breadcrumbs + ')\n'

    @staticmethod
    def error(bot, update, error):
        logger.warn('Update "%s" caused error "%s"' % (update, error))
