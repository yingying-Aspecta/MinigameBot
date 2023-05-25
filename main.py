"""
MinigameBot: Discord bot with different mini games.

Selena Zhou, May 2023
"""

import discord
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

"""CONFIGURATIONS"""

# .env
load_dotenv()

# Discord
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True      # important!!
client = discord.Client(intents=intents)

TOKEN = os.environ.get('TOKEN')

# Firebase
PATH_TO_JSON = os.environ.get('PATH_TO_JSON')
cred = credentials.Certificate(PATH_TO_JSON)
firebase_admin.initialize_app(cred)

db = firestore.client()

"""FUNCTIONS"""

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
