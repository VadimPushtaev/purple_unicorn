#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import logging
from bot import PurpleBot
from telegram.parsemode import ParseMode
import random
import re

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARN)
logger = logging.getLogger(__name__)


class BotCommandWrapper:
    MESSAGE_MAX_LENGTH = 4096
    purple_bot = PurpleBot()

    def __init__(self):
        pass

    @staticmethod
    def _extract_username(update):
        user = update.message.from_user
        name = user.first_name
        if name is None:
            name = user.username
        return name

    @staticmethod
    def send_single_message(bot, chat_id, msg, mode=ParseMode.HTML):
        bot.sendMessage(chat_id=chat_id, text=msg, parse_mode=mode)

    @classmethod
    def send_message(cls, bot, chat_id, message):
        i = 0
        while i*cls.MESSAGE_MAX_LENGTH < len(message):
            cls.send_single_message(bot,
                                    chat_id,
                                    message[i*cls.MESSAGE_MAX_LENGTH:(i+1)*cls.MESSAGE_MAX_LENGTH])
            i = i + 1

    @classmethod
    def send_sticker(cls, bot, chat_id, sticker):
        cls.send_sticker(bot, chat_id, sticker)

    @classmethod
    def hi_command(cls, bot, update):
        if random.randint(0, 1) == 0:
            cls.send_message(bot, update.message.chat_id, cls.purple_bot.get_random_greetings(cls._extract_username(update)))
        else:
            cls.send_sticker(bot, update.message.chat_id, cls.purple_bot.get_random_sticker())

    @classmethod
    def help_command(cls, bot, update):
        msg_text = update.message.text.strip()
        ndx = msg_text.find(' ')
        if ndx == -1:
            cls.send_message(bot, update.message.chat_id, cls.purple_bot.get_help_message())
        else:
            command = msg = msg_text[ndx:]
            cls.send_message(bot,
                             update.message.chat_id,
                             cls.purple_bot.get_current_help(msg))

    @classmethod
    def init_command(cls, bot, update):
        msg = update.message.text[6:]
        parts = re.split('[\s,]+', msg)
        res_tuples = []
        for part in parts:
            init_parts = re.split('=', part)
            if len(init_parts) >= 2:
                res_tuples.append((init_parts[0], init_parts[1]))
            else:
                res_tuples.append((init_parts[0], 0))
        cls.send_message(bot, update.message.chat_id, cls.purple_bot.generate_init(res_tuples))

    @classmethod
    def roll_command(cls, bot, update):
        msg_text = update.message.text.strip()
        ndx = msg_text.find(' ')
        if ndx == -1:
            cls.send_message(bot,
                             update.message.chat_id,
                             cls.purple_bot.roll_msg(cls._extract_username(update), "1d20"))
        else:
            msg = msg_text[ndx:]
            cls.send_message(bot,
                             update.message.chat_id,
                             cls.purple_bot.roll_msg(cls._extract_username(update), msg))

    @classmethod
    def roll_percent(cls, bot, update):
        cls.send_message(bot, update.message.chat_id, cls.purple_bot.roll_msg(cls._extract_username(update), "1d100"))

    @classmethod
    def flip_coin(cls, bot, update):
        cls.send_message(bot, update.message.chat_id, cls.purple_bot.flip_coin(cls._extract_username(update)))

    @classmethod
    def search_command(cls, bot, update):
        msg_text = update.message.text[8:].strip()
        cls.send_message(bot, update.message.chat_id, cls.purple_bot.execute_search(msg_text))

    @classmethod
    def error(cls, bot, update, error):
        logger.warning('Update "%s" caused error "%s"' % (update, error))
