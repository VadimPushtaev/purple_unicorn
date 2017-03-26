#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import sys
import ConfigParser
import telebot

config_name=sys.argv[1];
config = ConfigParser.ConfigParser()
config.read(config_name)
bot_token=config.get('main', 'token')
bot = telebot.TeleBot(bot_token)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)

