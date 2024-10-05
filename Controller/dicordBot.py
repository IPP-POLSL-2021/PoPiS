
import asyncio
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
import threading
from Controller.discordBotResponses import get_respone, create_event, check_24_hours
load_dotenv()
# aby wysłąć przypomnienie w  gdzieś musiałbym przetrzymywać cały obiekt message albo przynajmniej podobiekt author
TOKEN = os.getenv('TOKEN')

intents = Intents.default()
intents.messages = True
intents.message_content = True
client = Client(intents=intents)


async def discorCheck():
    while True:
        list = check_24_hours("./Data/time.txt", "discord")
        if list is not False:
            # firstSplit=list.split("\n")
            for row in list.itertuples(index=False):
                print(row)
                # create_reminders("",True)
                date = create_event(
                    row.chanelId, row.committee, row.platform)
                # to bardzo istotna część kodu z jakiegoś powodu bez tego nie dizłało
                print("działa?")
                print(date)

                if date == "brak":
                    await row.chanelId.send("nieznalezniono komisji")
                elif date == "brak posiedzeń":
                    await row.chanelId.send(date)
                else:
                    await row.chanelId.send(f" {date}")


async def send_message(message, user_message):
    if not user_message:
        print('pusto')
        return
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]
    try:
        response = get_respone(user_message)
        responseArray = response.split('\n')
        for responsee in responseArray:
            # print(responsee)
            await message.author.send(responsee) if is_private else await message.channel.send(responsee)
    except Exception as e:
        print(e)


@client.event
async def on_ready():
    print("działa")


@client.event
async def on_message(message, AutoDate, auto=False):
    if message.author == client.user:
        return
    username = str(message.author)
    user_message = message.content

    # print(user_message)
    channel = str(message.channel)
    # print(f'[{channel}] {username} "{user_message}"')
    id = message.channel.id
    channel = client.get_channel(id)
    # print(message.content[0])
    if message.content[0] == '!':

        date = create_event(id, user_message[1:], "discord")

        if date == "brak":
            await channel.send("nieznalezniono komisji")
        elif date == "brak posiedzeń":
            await channel.send(date)
        else:
            await channel.send(f" {date}")
    # await c)

    await send_message(message, user_message)


def star_discord_bot():
    checkingThread = threading.Thread(target=discorCheck)
    checkingThread.start()
    client.run(token=TOKEN)
