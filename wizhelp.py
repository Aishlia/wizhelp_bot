from dotenv import load_dotenv
load_dotenv()

import os
import urllib.request
import asyncio
import datetime
import random
import time
import discord
from discord.ext import commands
import random
from pygifsicle import optimize


from functions.library_tc import wtb_tc
from functions.find_boss_info import find_boss_info

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'The bot has logged in as {bot.user} and is ready to serve requests of its human overlords.')

@bot.command(name='hello', help='Responds with a hello message to show bot is up. !hello')
async def greeting(context):
    await context.send('Hello there!')

@bot.command(name='boss', help='')
async def find_boss_cheats(context, *boss_name: str):
    boss_info = find_boss_info(boss_name)
    await context.send("**Health**:  " + boss_info['health'])
    await context.send("**Pips**:    " + boss_info['starting_pips'])
    await context.send("**Boosts**:  " + boss_info['boosts'])
    await context.send("**Resists**: " + boss_info['resists'])
    await context.send("**Cheats**: ")
    await context.send(boss_info['cheats'])

@bot.command(name='tc', help='')
async def wtb_tc(context, *spell: str):
    tc_info = wtb_tc(spell)
    print(tc_info)
    await context.send("**Library:   **" + tc_info['library'])
    await context.send("**Location:  **" + tc_info['location'])
    await context.send("**Librarian: **" + tc_info['librarian'])
    await context.send("**Spell:     **" + tc_info['spell'])
    await context.send("**Cost:      **" + tc_info['cost'])


bot.run(os.getenv('BOT_TOKEN'))
