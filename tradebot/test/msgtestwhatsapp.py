import telebot
import json
from telegram_alert import send_warning


for i in range(0,5):
    if i%2==0:
        send_warning(i)


