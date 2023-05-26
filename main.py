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


# HELPER EMBEDS

def embed_mini_construction():
    embed = discord.Embed(title=":construction: This command is under construction... :construction:",
                          description="Come back soon :)",
                          colour=discord.Colour.from_rgb(106, 13, 255))
    return embed


def embed_mini_help():
    embed = discord.Embed(title=":dart: MinigameBot Command Guide",
                          description="Here is a complete list of all MinigameBot's commands!",
                          colour=discord.Colour.from_rgb(106, 13, 255))
    embed.add_field(name=":question: Need help?", value="`mini help`: A complete list of our features.")
    embed.add_field(name=":zap: Get stats!", value="`mini cc`: How many commands have you sent?")
    embed.add_field(name=":coin: Your balance.", value="`mini bal`: Tells you your coin balance.")
    embed.add_field(name=":person_running: Endless Runner", value="`mini run`: The Endless Runner game.")
    embed.add_field(name=":black_joker: Blackjack", value="`mini bj`: Play Blackjack with us.")
    embed.add_field(name='\u200B', value='\u200B')
    return embed


def embed_mini_cc(user):
    embed = discord.Embed(title=f":computer: {user.name}'s command count",
                          description=f"You have sent me {get_cmd_count(user)} commands!",
                          colour=discord.Colour.from_rgb(106, 13, 255))
    return embed


def embed_mini_coins(user):
    embed = discord.Embed(title=f":money_with_wings: {user.name}'s Bank Account",
                          description=f"{user.mention} - Earn more coins by playing mini games!",
                          colour=discord.Colour.from_rgb(106, 13, 255))
    embed.add_field(name="Your balance:", value=f"{get_coin_count(user)} :coin:", inline=False)
    return embed


# FIRESTORE: Count commands

def get_cmd_count(user):
    if not user.bot:
        doc_ref = db.collection('leaderboard').document(str(user.id))
        cmd_count_ref = doc_ref.get({'cmd_count'}).to_dict()
        if cmd_count_ref is not None:
            return cmd_count_ref.get('cmd_count')
        return 0


def update_cmd_count(user):
    if not user.bot:
        doc_ref = db.collection('leaderboard').document(str(user.id))
        curr_count = get_cmd_count(user)
        doc_ref.set({
            'cmd_count': curr_count + 1
        })


# FIRESTORE: Count coins

def get_coin_count(user):
    if not user.bot:
        doc_ref = db.collection('leaderboard').document('{}'.format(user.id))
        coin_count_ref = doc_ref.get({'coins'}).to_dict()
        if coin_count_ref.get('coins') is not None:
            return coin_count_ref.get('coins')
        return 0


def update_coin_count(user, addCoins):
    if not user.bot:
        doc_ref = db.collection('leaderboard').document('{}'.format(user.id))
        curr_coins = get_coin_count(user)
        doc_ref.set({
            'coins': curr_coins + addCoins
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

        if msg.startswith("mini"):

            update_cmd_count(message.author)

            if msg.startswith("mini help"):
                embed = embed_mini_help()
                await message.channel.send(embed=embed)
            elif msg.startswith("mini cc"):
                embed = embed_mini_cc(message.author)
                await message.channel.send(embed=embed)
            elif msg.startswith("mini bal"):
                embed = embed_mini_coins(message.author)
                await message.channel.send(embed=embed)
                # coin_count = get_coin_count(message.author)
                # await message.channel.send(f"Your balance is {coin_count} coins, {message.author}!")
            elif msg.startswith("mini run"):
                embed = embed_mini_construction()
                await message.channel.send(embed=embed)
            elif msg.startswith("mini bj"):
                embed = embed_mini_construction()
                await message.channel.send(embed=embed)


client.run(TOKEN)
