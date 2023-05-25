"""
MinigameBot: Discord bot with different mini games.

Selena Zhou, May 2023
"""

import discord
import os
from dotenv import load_dotenv

"""CONFIGURATIONS"""

intents = discord.Intents.default()     # not necessary for default, but may be helpful later
intents.members = True
client = discord.Client(intents=intents)
TOKEN = os.environ.get('TOKEN')
load_dotenv()

"""EVENTS"""


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.content.startswith("mini "):
        await message.channel.send("Hello!")

client.run(TOKEN)