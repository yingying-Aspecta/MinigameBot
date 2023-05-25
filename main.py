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
intents.message_content = True  # important!!
client = discord.Client(intents=intents)

TOKEN = os.environ.get('TOKEN')

# Firebase
PATH_TO_JSON = os.environ.get('PATH_TO_JSON')
cred = credentials.Certificate(PATH_TO_JSON)
firebase_admin.initialize_app(cred)

db = firestore.client()

"""FUNCTIONS"""


# FIRESTORE: Count commands

def get_cmd_count(user):
    if not user.bot:
        doc_ref = db.collection('leaderboard').document(u'{}'.format(user.id))
        cmd_count_ref = doc_ref.get({u'cmd_count'}).to_dict()
        if cmd_count_ref is not None:
            return cmd_count_ref.get('cmd_count')
        return 0


def update_cmd_count(user):
    if not user.bot:
        doc_ref = db.collection(u'leaderboard').document(u'{}'.format(user.id))  # what is u?
        curr_count = get_cmd_count(user)
        doc_ref.set({
            u'cmd_count': curr_count + 1
        })


# FIRESTORE: Count coins

def get_coin_count(user):
    if not user.bot:
        doc_ref = db.collection('leaderboard').document(u'{}'.format(user.id))
        cmd_count_ref = doc_ref.get({u'coins'}).to_dict()
        if cmd_count_ref is not None:
            return cmd_count_ref.get('coins')
        return 0


def update_coin_count(user, addCoins):
    if not user.bot:
        doc_ref = db.collection(u'leaderboard').document(u'{}'.format(user.id))  # what is u?
        curr_coins = get_coin_count(user)
        doc_ref.set({
            u'coins': curr_coins + addCoins
        })


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

            update_cmd_count(message.author)

            if msg.startswith("mini hi"):
                await message.channel.send("Hello!")
            elif msg.startswith("mini cc"):       # count commands
                command_count = get_cmd_count(message.author)
                await message.channel.send(f"You have sent me {command_count} commands, {message.author}!")

client.run(TOKEN)
