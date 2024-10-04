import os
import telebot
from Controller.discordBotResponses import get_respone, create_event, check_24_hours
from dotenv import load_dotenv
import threading
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
def create_reminders(message="", auto=False, id="", Auto_date=""):
    # message = message.split(" ")[1]
    # if auto == True:
    #     bot.send_message(id, Auto_date)
    # else:
    response = message.text.split(" ")[1]
    date = create_event(message.chat.id, response, "telegram")
    if date == "brak":
        bot.send_message(message.chat.id, "nieznalezniono komisji")
    elif date == "brak posiedzeń":
        bot.send_message(message.chat.id, date)
    else:
        bot.send_message(message.chat.id, f" {date}")


def telegramCheck():
    while True:
        list = check_24_hours("./Data/time.txt", "telegram")
        if list is not False:
            # firstSplit=list.split("\n")
            for row in list.itertuples(index=False):
                print(row)
                # create_reminders("",True)
                date = create_event(
                    row.chanelId, row.committee, row.platform)
                # to bardzo istotna część kodu z jakiegoś powodu bez tego nie dizłało
                print("huuuuuuuuj")
                print(date)

                if date == "brak":
                    bot.send_message(row.chanelId, "nieznalezniono komisji")
                elif date == f"brak posiedzeń komisji {row.committee}":
                    bot.send_message(row.chanelId, date)
                else:
                    bot.send_message(row.chanelId, f" {date}")


def start_telegram_bot():
    checkingThread = threading.Thread(target=telegramCheck)
    checkingThread.start()
    bot.infinity_polling()
