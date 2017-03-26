#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import sys
import ConfigParser
import telebot

bot = None;

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)

def work_out_args(argv):
    config_name=argv[1];
    config = ConfigParser.ConfigParser()
    config.read(config_name)
    bot_token=config.get('main', 'token')
    global bot
    bot = telebot.TeleBot(bot_token)

if __name__ == '__main__':
    work_out_args(sys.argv)
    bot.polling(none_stop=True)

