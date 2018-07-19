import telepot
from django.conf import settings


token = settings.TELEGRAM_BOT_TOKEN
my_id = settings.TELEGRAM_ADMIN_CHAT_ID

telegramBot = telepot.Bot(token)


def send_message(text, chat_id= my_id):
    telegramBot.sendMessage(chat_id, text, parse_mode="Markdown")
