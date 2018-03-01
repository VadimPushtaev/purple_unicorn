#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
from unittest.mock import MagicMock, call

from telegram.parsemode import ParseMode
from bot import PurpleBot as PB


class DummyBot:
    def __init__(self):
        pass

    @classmethod
    def sendMessage(cls, chat_id, text, parse_mode):
        pass


class BotTestCase(TestCase):
    bot = None

    def setUp(self):
        self.bot = DummyBot()

    def test_send_short_msg(self):
        self.bot.sendMessage = MagicMock()
        PB.send_message(self.bot, 123, "abc")
        self.bot.sendMessage.assert_called_with(chat_id=123, text="abc", parse_mode=ParseMode.HTML)

    def test_send_long_msg(self):
        self.bot.sendMessage = MagicMock()
        PB.send_message(self.bot, 123, "a" * 5000)
        self.bot.sendMessage.assert_has_calls([call(chat_id=123, text="a" * 4096, parse_mode=ParseMode.HTML)])
        self.bot.sendMessage.assert_called_with(chat_id=123, text="a"*904, parse_mode=ParseMode.HTML)


if __name__ == '__main__':
    unittest.main()
