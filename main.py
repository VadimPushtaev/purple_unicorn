#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import os
from telegram.ext import CommandHandler, Updater
from bot_wrapper import BotCommandWrapper as bot

if __name__ == '__main__':
    TOKEN = os.environ['bot_token']
    PORT = int(os.environ.get('PORT', '5000'))
    updater = Updater(TOKEN)

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.setWebhook("https://punic.herokuapp.com/" + TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("help", bot.help_command))
    dispatcher.add_handler(CommandHandler("init", bot.init_command))
    dispatcher.add_handler(CommandHandler("roll", bot.roll_command))
    dispatcher.add_handler(CommandHandler("r", bot.roll_command))
    dispatcher.add_handler(CommandHandler("percent", bot.roll_percent))
    dispatcher.add_handler(CommandHandler("fc", bot.flip_coin))
    dispatcher.add_handler(CommandHandler("hi", bot.hi_command))
    dispatcher.add_handler(CommandHandler("search", bot.search_command))

    dispatcher.add_error_handler(bot.error)

    updater.idle()
