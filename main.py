"""
MinigameBot: Discord bot with different mini games.

Selena Zhou, May 2023
"""

import discord
import os
from dotenv import load_dotenv

"""CONFIGURATIONS"""

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True
client = discord.Client(intents=intents)

TOKEN = os.environ.get('TOKEN')

"""EVENTS"""


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):

    if message.guild is not None:

        if message.author == client.user:
            return

        msg = message.content.lower()
        print(msg)

        if msg.startswith("mini"):
            if msg.startswith("mini hi"):
                await message.channel.send("Hello!")
            else:
                await message.channel.send("I don't recognize that command.")

client.run(TOKEN)