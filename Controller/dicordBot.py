
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message

from discordBotResponses import get_respone, create_event
load_dotenv()
# aby wysłąć przypomnienie w  gdzieś musiałbym przetrzymywać cały obiekt message albo przynajmniej podobiekt author
TOKEN = os.getenv('TOKEN')

intents = Intents.default()
intents.messages = True
intents.message_content = True
client = Client(intents=intents)


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
            print(responsee)
            await message.author.send(responsee) if is_private else await message.channel.send(responsee)
    except Exception as e:
        print(e)


@client.event
async def on_ready():
    print("działa")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    username = str(message.author)
    user_message = message.content

    print(user_message)
    channel = str(message.channel)
    print(f'[{channel}] {username} "{user_message}"')
    id = message.channel.id
    channel = client.get_channel(id)
    print(message.content[0])
    # if message.content[0] == '!':
    #     create_event(id, user_message[1:])
    # await channel.send('hello')

    await send_message(message, user_message)


def main():
    client.run(token=TOKEN)


main()
