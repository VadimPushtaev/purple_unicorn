#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import os
from telegram.ext import CommandHandler, Updater
from bot import PurpleBot

if __name__ == '__main__':
    TOKEN = os.environ['bot_token']
    PORT = int(os.environ.get('PORT', '5000'))
    updater = Updater(TOKEN)

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.setWebhook("https://punic.herokuapp.com/" + TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("help", PurpleBot.help_command))
    dispatcher.add_handler(CommandHandler("init", PurpleBot.init_command))
    dispatcher.add_handler(CommandHandler("roll", PurpleBot.roll_command))
    dispatcher.add_handler(CommandHandler("r", PurpleBot.roll_command))
    dispatcher.add_handler(CommandHandler("percent", PurpleBot.roll_percent))
    dispatcher.add_handler(CommandHandler("hi", PurpleBot.hi_command))
    dispatcher.add_handler(CommandHandler("search", PurpleBot.search_command))

    dispatcher.add_error_handler(PurpleBot.error)

    updater.idle()
