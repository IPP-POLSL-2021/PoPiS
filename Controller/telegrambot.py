import os
import telebot
from Controller.discordBotResponses import get_respone, create_event
from dotenv import load_dotenv

load_dotenv()

TELEGRAMTOKEN = os.getenv('TELEGRAMTOKEN')
bot = telebot.TeleBot(TELEGRAMTOKEN)


@bot.message_handler(commands=['komisje', ''])
def send_welcome(message):
    print(message.text)
    # w przypadku telegramu wystarczy w bazie przechować id cztau i date
    response = get_respone(message.text[1:])
    # for responsee in responseArray:

    # print(response)
    bot.reply_to(message, f"oto lista komisji{response}")
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands=['powiadom'])
def create_reminders(message):
    response = get_respone(message.text[1:])
    date = create_event(message.chat.id, response, "telegram")
    if date == "brak":
        bot.send_message(message.chat.id, "nieznalezniono komisji")
    elif date == "brak posiedzeń":
        bot.send_message(message.chat.id, date)
    else:
        bot.send_message(message.chat.id, f"ustwaiono przypomninie na {date}")


def start_telegram_bot():
    bot.infinity_polling()
