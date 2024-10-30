
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


def discordCheck():
    while True:
        list = check_24_hours("./Data/time.txt", "discord")
        if list is not False:
            # firstSplit=list.split("\n")
            for row in list.itertuples(index=False):
                print(row)
                # create_reminders("",True)
                date = create_event(
                    row.channelId, row.committee, row.platform)
                # to bardzo istotna część kodu z jakiegoś powodu bez tego nie dizłało
                print("działa?")
                print(date)
                channel = client.get_channel(row.channelId)
                if date == "brak":
                    channel.send("nie znaleziono komisji")
                elif date == "brak posiedzeń":
                    channel.send(date)
                else:
                    channel.send(f" {date}")


async def send_message(message, user_message):
    if not user_message:
        print('pusto')
        return
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]
    try:
        response = get_respone(user_message)
        responseArray = response.split('\n')
        for response in responseArray:
            # print(response)
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


@client.event
async def on_ready():
    print("działa")


@client.event
async def on_message(message,  auto=False):
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
            await channel.send("nie znaleziono komisji")
        elif date == "brak posiedzeń":
            await channel.send(date)
        else:
            await channel.send(f" {date}")
    # await c)

    await send_message(message, user_message)


def start_discord_bot():
    checkingThread = threading.Thread(target=discordCheck)
    checkingThread.start()
    client.run(token=TOKEN)
