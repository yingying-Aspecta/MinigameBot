"""
MinigameBot: Discord bot with different mini games.

Selena Zhou, May 2023
"""

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

"""CONFIGURATIONS"""

# .env
load_dotenv()

# Discord
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True  # important!!
intents.reactions = True
client = commands.Bot(command_prefix='mini ', intents=intents)

TOKEN = os.environ.get('TOKEN')

# Firebase
PATH_TO_JSON = os.environ.get('PATH_TO_JSON')
cred = credentials.Certificate(PATH_TO_JSON)
firebase_admin.initialize_app(cred)

db = firestore.client()

"""FUNCTIONS"""

"""FIRESTORE FUNCTIONS"""


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


"""LOG-IN"""


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


"""COMMANDS"""


# mini help

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


class MiniHelp(commands.HelpCommand):

    async def send_bot_help(self, mapping):
        update_cmd_count(self.context.message.author)
        embed = embed_mini_help()
        await self.context.send(embed=embed)


client.help_command = MiniHelp()

# mini cc

def embed_mini_cc(user):
    embed = discord.Embed(title=f":computer: {user.name}'s command count",
                          description=f"You have sent me {get_cmd_count(user)} commands!",
                          colour=discord.Colour.from_rgb(106, 13, 255))
    return embed


@client.command(name="cc")
async def mini_cc(ctx):
    update_cmd_count(ctx.message.author)
    embed = embed_mini_cc(ctx.message.author)
    await ctx.send(embed=embed)


"""GAMES"""

# Endless Runner

# Blackjack

"""HELPER FUNCTIONS"""


def embed_mini_construction():
    embed = discord.Embed(title=":construction: This command is under construction... :construction:",
                          description="Come back soon :)",
                          colour=discord.Colour.from_rgb(106, 13, 255))
    return embed






def embed_mini_coins(user):
    embed = discord.Embed(title=f":money_with_wings: {user.name}'s Bank Account",
                          description=f"{user.mention} - Earn more coins by playing mini games!",
                          colour=discord.Colour.from_rgb(106, 13, 255))
    embed.add_field(name="Your balance:", value=f"{get_coin_count(user)} :coin:", inline=False)
    return embed


def embed_leaderboard(guild):
    embed = discord.Embed(title=f":trophy: {guild.name}'s Coin Leaderboard",
                          color=discord.Colour.from_rgb(106, 13, 255))
    max_members = 10
    leaderboard_list = ""

client.run(TOKEN)
