#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
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

def talk_command(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm crazy purple unicorn!!!!!")
    bot.sendSticker(chat_id=update.message.chat_id, sticker='CAADAgADOgAD7sShCiK3hMJMvtbhAg')

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
                char=(pairs[0], roll+int(pairs[1])+0.01*int(pairs[1]), roll)
                parts_tuples.append(char)
                if len(pairs[0]) > width:
                    width=len(pairs[0])
    sorted(parts_tuples, key=lambda parts: parts[1])
    res="Results:"
    for char in parts_tuples:
        res += '\n' + '<code>' + '{0: <{width}}'.format(char[0], width=width) + '</code> : <b>' + str(char[1]) + '</b> (' + str(char[2]) + ')'
    bot.sendMessage(chat_id=update.message.chat_id, text=res, parse_mode=ParseMode.HTML)

def roll_command(bot, update):
    msg = update.message.text[6:]
    roll_msg(msg, bot, update)

def r_command(bot, update):
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

def get_input(bot, update):
    user = update.message.from_user
    name = user.first_name
    if name is None:
        name = user.username
    update.message.reply_text('%s, why are you talking to me?!' % (name))

if __name__ == '__main__':
    TOKEN = "307626358:AAGZjVmwtIbm3AictFocZJcV6Ps5PAZxofI"
    PORT = int(os.environ.get('PORT', '5000'))
    updater = Updater(TOKEN)

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.setWebhook("https://punic.herokuapp.com/" + TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("init", init_command))
    dispatcher.add_handler(CommandHandler("roll", roll_command))
    dispatcher.add_handler(CommandHandler("r", r_command))
    dispatcher.add_handler(CommandHandler("talk", talk_command))
    dispatcher.add_handler(MessageHandler(Filters.text, get_input))

    dispatcher.add_error_handler(error)

    updater.idle()

