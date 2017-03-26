#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import ConfigParser
import logging
import os
import sys
import telebot

from telegram.ext import CommandHandler
from telegram.ext import Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARN)
logger = logging.getLogger(__name__)

def talk(bot, update):
    logger.info('Update [%s]' % (update))
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm crazy purple unicorn!!!!!")

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

if __name__ == '__main__':
    # get config info
    config_name=sys.argv[1];
    config = ConfigParser.ConfigParser()
    config.read(config_name)

    TOKEN = config.get('main', 'token')
    updater = Updater(token=TOKEN)

    PORT = int(os.environ.get('PORT', '5000'))

    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.setWebhook("https://punic.herokuapp.com/" + TOKEN)
    
    # get dispatcher
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('talk', talk))
    dispatcher.add_error_handler(error)

    updater.idle()

