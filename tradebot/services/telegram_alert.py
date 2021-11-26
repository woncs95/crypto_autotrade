import telebot


def send_telegram_message(message):
    api_key="1877338163:AAGudRmifqHNRJyMu_GzOnwVZwsmAplVWDw"
    bot = telebot.TeleBot(api_key)
    bot.send_message(1886956707, message)
