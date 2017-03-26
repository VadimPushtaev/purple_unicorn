#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import ConfigParser
import logging
import os
import sys
import telebot

from telegram.ext import CommandHandler
from telegram.ext import Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

config_name=sys.argv[1];
config = ConfigParser.ConfigParser()
config.read(config_name)

TOKEN = config.get('main', 'token')
PORT = int(os.environ.get('PORT', '5000'))

UPDATER = Updater(token=TOKEN)
DISPATCHER = UPDATER.dispatcher

def start(bot, update):
    logger.info("Update [" + update + "]")
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm crazy purple unicorn!!!!!")

if __name__ == '__main__':
    start_handler = CommandHandler('start', start)
    DISPATCHER.add_handler(start_handler)

    UPDATER.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    UPDATER.bot.setWebhook("https://punic.herokuapp.com/" + TOKEN)
    UPDATER.idle()

