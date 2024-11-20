import os
import telebot
from Controller.discordBotResponses import get_response, create_event, check_24_hours
from dotenv import load_dotenv
import threading
import requests
load_dotenv()


TELEGRAMTOKEN = os.getenv('TELEGRAMTOKEN')
bot = telebot.TeleBot(TELEGRAMTOKEN)


@bot.message_handler(commands=['komisje', ''])
def send_welcome(message):
    print(message.text)
    # w przypadku telegramu wystarczy w bazie przechować id czatu i date
    response = get_response(message.text[1:])
    # for response in responseArray:

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
        bot.send_message(message.chat.id, "Nie znaleziono komisji")
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
                # print(row)
                # create_reminders("",True)
                date = create_event(
                    row.channelId, row.committee, row.platform)
                # to bardzo istotna część kodu z jakiegoś powodu bez tego nie dizłało
                print("działa?")
                # print(date)
                request = requests.get(
                    f"https://api.sejm.gov.pl/sejm/term10/committees/{row.committee}")
                response = request.json()
                # print(response["name"])
                if date == "brak":
                    bot.send_message(row.channelId, "Nie znaleziono komisji")
                elif date == f"brak nowych posiedzeń":
                    date += f" {response['name']}"
                    bot.send_message(row.channelId, date)
                else:
                    date = date.split("%")[1]
                    bot.send_message(row.channelId, f" {date}")


def start_telegram_bot():
    checkingThread = threading.Thread(target=telegramCheck)
    checkingThread.start()
    bot.infinity_polling()
