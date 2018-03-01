#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import logging
from bot import PurpleBot
import re

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARN)
logger = logging.getLogger(__name__)


class BotCommandWrapper:
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

    @classmethod
    def hi_command(cls, bot, update):
        cls.purple_bot.send_hi_message(bot, update.message.chat_id, cls._extract_username(update))

    @classmethod
    def help_command(cls, bot, update):
        cls.purple_bot.send_help_message(bot, update.message.chat_id)

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
        cls.purple_bot.generate_init(bot, update.message.chat_id, res_tuples)

    @classmethod
    def roll_command(cls, bot, update):
        msg_text = update.message.text.strip()
        ndx = msg_text.find(' ')
        if ndx == -1:
            cls.purple_bot.roll_msg(bot, update.message.chat_id, cls._extract_username(update), "1d20")
        else:
            msg = msg_text[ndx:]
            cls.purple_bot.roll_msg(bot, update.message.chat_id, cls._extract_username(update), msg)

    @classmethod
    def roll_percent(cls, bot, update):
        cls.purple_bot.roll_msg(bot, update.message.chat_id, cls._extract_username(update), "1d100")

    @classmethod
    def search_command(cls, bot, update):
        msg_text = update.message.text[8:].strip()
        cls.purple_bot.execute_search(bot, update.message.chat_id, msg_text)

    @classmethod
    def error(cls, bot, update, error):
        logger.warning('Update "%s" caused error "%s"' % (update, error))
