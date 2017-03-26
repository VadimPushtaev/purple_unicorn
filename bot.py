#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import logging
import os
import sys
import telebot

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARN)
logger = logging.getLogger(__name__)

def talk(bot, update):
    logger.info('Update [%s]' % (update))
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm crazy purple unicorn!!!!!")

def roll(bot, update):
    logger.info('Update [%s]' % (update))
    update.message.reply_text(update.message)

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
    dispatcher.add_handler(CommandHandler("talk", talk))
    dispatcher.add_handler(MessageHandler(Filters.text, get_input))

    dispatcher.add_error_handler(error)

    updater.idle()

