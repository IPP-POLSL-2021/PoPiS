import os
import telebot
from discordBotResponses import get_respone
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


bot.infinity_polling()
