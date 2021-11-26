import telebot
import json
import os


def send_warning(message):
    fileDir = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(fileDir, 'teletoken.json')
    with open(filename) as key:
        information = json.load(key)
        api_key = information['api_key']
        bot = telebot.TeleBot(api_key)
    bot.send_message(1886956707, message)
