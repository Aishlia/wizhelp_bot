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

import requests
from bs4 import BeautifulSoup
import re

from functions.library_tc import wtb_tc

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'The bot has logged in as {bot.user} and is ready to serve requests of its human overlords.')

@bot.command(name='hello', help='Responds with a hello message to show bot is up. !hello')
async def greeting(context):
    await context.send('Hello there!')

@bot.command(name='boss', help='')
async def find_boss_cheats(context, *boss_name: str):
    url = 'http://www.wizard101central.com/wiki/Creature:' + '_'.join(boss_name)
    print(url)
    resp = requests.get(url)
    page_info = BeautifulSoup(resp.text, 'html.parser')
    general_info = page_info.find('div', {'id': 'relative-top'})
    general_info = general_info.findAll('tr')
    health = general_info[3].findAll('td')[1].get_text()
    await context.send("__**Health: **__" + health)

    starting_pips = page_info.find('td', text='Starting Pips').parent()[2].text.strip()
    starting_pips = [int(word) for word in starting_pips.split() if word.isdigit()]
    starting_pips = str(starting_pips[0])
    await context.send("__**Starting Pips: **__" + starting_pips)

    boosts_info = page_info.find('td', text='Inc. Boost').parent()[2]
    boosts = boosts_info.text.strip()
    boost_classes = boosts_info.findAll('a')
    out = ''
    for i in boost_classes:
        spell_type = i['title'][9:]
        out += spell_type + ' and '
    out = out[:-5]
    await context.send("__**Boosts: **__" + out)

    resists_info = page_info.find('td', text='Inc. Resist').parent()[2]
    resists = resists_info.text.strip()
    resists_classes = resists_info.findAll('a')
    out = ''
    for i in resists_classes:
        spell_type = i['title'][9:]
        out += spell_type + ' and '
    out = out[:-5]
    await context.send("__**Resists: **__" + out)

    await context.send("__**Cheats: **__")
    try:
        cheats = page_info.find('div', text='Cheats').parent()
        await context.send(cheats[1].text)
    except:
        await context.send("This boss has no cheats")

bot.run(os.getenv('BOT_TOKEN'))
