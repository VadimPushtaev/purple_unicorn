#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import ConfigParser
import logging
import os
import sys
import random
import re
import telebot

from telegram.parsemode import ParseMode
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARN)
logger = logging.getLogger(__name__)

def hi_command(bot, update):
    if rollD(2) == 1:
        user = update.message.from_user
        name = user.first_name
        if name is None:
            name = user.username
        msgs = ["I'm crazy purple unicorn!!!!!", "Tell me 'bout the raaaaabits", "I am fluffy! Fluffy-fluffy-fluffy WOLF!", "Let me be a leader and I shall endeavor not to get all of us killed.", name + ', why are you talking to me?!']
        bot.sendMessage(chat_id=update.message.chat_id, text=random.choice(msgs))
    else:
        stickers = ['CAADAgADOgAD7sShCiK3hMJMvtbhAg', 'CAADAgADXwAD7sShCnji8rK8rHETAg', 'CAADAgADPgAD7sShChzV1O0OvX5KAg', 'CAADAgADPAAD7sShCkDkzhbVa_89Ag']
        bot.sendSticker(chat_id=update.message.chat_id, sticker=random.choice(stickers))

def help_command(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, 
                    text='<code>/hi</code> - bot will say something\n' +
                         '<code>/roll</code> - roll dices. E.g.: /roll 2d6 + 5\n' +
                         '<code>/r</code> - shortcut for roll command\n' +
                         '<code>/init</code> - roll dices for initiative (or any saves), result will be sorted; you may also pass your bonuses with your names, e.g.: /init barbarian=2 cleric=0 orc1=1 orc2=1', 
                    parse_mode=ParseMode.HTML)

def init_command(bot, update):
    msg = update.message.text[6:]
    parts = msg.split(' ')
    parts_tuples=[]
    width=1
    for p in parts:
        if len(p) > 0:
            pairs=p.split('=')
            if len(pairs) == 2:
                roll=rollD(20)
                char=(pairs[0], roll+int(pairs[1]), int(pairs[1]), roll, rollD(10))
                parts_tuples.append(char)
                if len(pairs[0]) > width:
                    width=len(pairs[0])
    res="Results:"
    for char in sorted(parts_tuples, key=lambda parts: (-parts[1], -parts[2], -parts[4])):
        res += '\n' + '<code>' + '{0: <{width}}'.format(char[0], width=width) + '</code> : <b>' + str(char[1]) + '</b> (' + str(char[3]) + ' ' + str(char[2]) + ' [' + str(char[4]) + '])'
    bot.sendMessage(chat_id=update.message.chat_id, text=res, parse_mode=ParseMode.HTML)

def roll_command(bot, update):
    if len(update.message.text) <= 6:
        roll_msg("1d20", bot, update)
    else:
        msg = update.message.text[6:]
        roll_msg(msg, bot, update)

def r_command(bot, update):
    if len(update.message.text) <= 3:
        roll_msg("1d20", bot, update)
    else:
        msg = update.message.text[3:]
        roll_msg(msg, bot, update)

def roll_msg(msg, bot, update):
    res=re.sub('(\d+)d(\d+)', dice_roll, msg)
    answer=update.message.from_user.username + ' rolls:\n' + res + ' = <b>' + str(eval(res)) + '</b>'
    bot.sendMessage(chat_id=update.message.chat_id, text=answer, parse_mode=ParseMode.HTML)

def dice_roll(matchobj):
    x,y=map(int,matchobj.groups())
    s = str(rollD(y))
    for each in range(1, x):
        s += '+' + str(rollD(y))
    return '(' + str(s) + ')'

def rollD(d):
    return random.randint(1, d)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

if __name__ == '__main__':
    config_name=sys.argv[1];
    config = ConfigParser.ConfigParser()
    config.read(config_name)
    TOKEN=config.get('main', 'token')
    PORT = int(os.environ.get('PORT', '5000'))
    updater = Updater(TOKEN)

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.setWebhook("https://punic.herokuapp.com/" + TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("init", init_command))
    dispatcher.add_handler(CommandHandler("roll", roll_command))
    dispatcher.add_handler(CommandHandler("r", r_command))
    dispatcher.add_handler(CommandHandler("hi", hi_command))

    dispatcher.add_error_handler(error)

    updater.idle()

