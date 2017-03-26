#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import logging
import os
import sys
import random
import re
import telebot

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARN)
logger = logging.getLogger(__name__)

def talk_command(bot, update):
    logger.info('Update [%s]' % (update))
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm crazy purple unicorn!!!!!")

def roll_command(bot, update):
    logger.info('Update [%s]' % (update))
    msg = update.message.text[6:]
    roll_msg(msg, update)

def r_command(bot, update):
    logger.info('Update [%s]' % (update))
    msg = update.message.text[3:]
    roll_msg(msg, update)

def roll_msg(msg, update):
    res=re.sub('(\d+)d(\d+)', dice_roll, msg)
    update.message.reply_text('%s rolls:\n%s = *%s*' % (update.message.from_user.username, res, eval(res)))

def dice_roll(matchobj):
    x,y=map(int,matchobj.groups())
    s = str(random.randint(1, y))
    for each in range(1, x):
        s += '+' + str(random.randint(1, y))
    return '(' + str(s) + ')'

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
    dispatcher.add_handler(CommandHandler("talk", talk_command))
    dispatcher.add_handler(CommandHandler("roll", roll_command))
    dispatcher.add_handler(CommandHandler("r", r_command))
    dispatcher.add_handler(MessageHandler(Filters.text, get_input))

    dispatcher.add_error_handler(error)

    updater.idle()

