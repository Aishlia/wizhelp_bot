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
from functions.reagent_recipes import reagent_recipes_lookup

bot = commands.Bot(command_prefix='!')

@bot.command()
async def embed(ctx):
    embed=discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/", description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
    await ctx.send(embed=embed)

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

@bot.command(name='reagent', help='')
async def wtb_tc(context, *reagent: str):
    reagent_recipes = reagent_recipes_lookup(reagent)
    print(reagent_recipes)
    embed=discord.Embed(title=' '.join(reagent).title(), color=0xFF5733)
    for item in reagent_recipes:
        embed.add_field(name=item[0], value=item[1], inline=True)
        if len(embed) >= 5000:
            await context.send(embed=embed)
            embed=discord.Embed(title=' '.join(reagent).title() + ' cont.', colour=0x0ff1ce)
    await context.send(embed=embed)

bot.run(os.getenv('BOT_TOKEN'))
