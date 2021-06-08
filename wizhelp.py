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


from functions.library_tc import wtb_tc as lib_wtb_tc
from functions.find_boss_info import find_boss_info
from functions.reagent_recipes import reagent_recipes_lookup
from functions.find_recipe  import find_recipe

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'The bot has logged in as {bot.user} and is ready to serve requests of its human overlords.')

@bot.command(name='hello', help='Responds with a hello message to show bot is up. !hello')
async def greeting(context):
    await context.send('Hi bub! My name is Merle Ambrose, but you can call me Ear for short. I\'m the headmaster at Ravenwood. Have fun doing my bidding.')

@bot.command(name='boss', help='Find out boss stats and cheats')
async def find_boss_cheats(context, *boss_name: str):
    boss_info = find_boss_info(boss_name)
    embed=discord.Embed(title=boss_info['boss_name'], color=0xFF5733)
    embed.add_field(name="**Health**", value=boss_info['health'], inline=False)
    embed.add_field(name="**Pips:**", value=boss_info['starting_pips'], inline=False)
    embed.add_field(name="**Boosts:**", value=boss_info['boosts'], inline=False)
    embed.add_field(name="**Resists:**", value=boss_info['resists'], inline=False)
    chunks = len(boss_info['cheats'])
    chunk_size = 1000
    x = boss_info['cheats']
    cheats = [x[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
    for i in cheats:
        embed.add_field(name="**Cheats:**", value=i, inline=False)
    await context.send(embed=embed)

@bot.command(name='tc', help='Find out where to buy a treasure card.')
async def wtb_tc(context, *spell: str):
    tc_info = lib_wtb_tc(spell)
    embed=discord.Embed(title=' '.join(spell).title(), color=0xFF5733)
    embed.add_field(name="**Library:**", value=tc_info['library'], inline=False)
    embed.add_field(name="**Location:**", value=tc_info['location'], inline=False)
    embed.add_field(name="**Librarian:**", value=tc_info['librarian'], inline=False)
    embed.add_field(name="**Spell:**", value=tc_info['spell'], inline=False)
    embed.add_field(name="**Cost:**", value=tc_info['cost'], inline=False)
    await context.send(embed=embed)

@bot.command(name='reagent', help='Find out what recipes a reagent is used for.')
async def wtb_reagent(context, *reagent: str):
    reagent_recipes = reagent_recipes_lookup(reagent)
    print(reagent_recipes)
    embed=discord.Embed(title=' '.join(reagent).title(), color=0xFF5733)
    for item in reagent_recipes:
        embed.add_field(name=item[0], value=item[1], inline=True)
        if len(embed) >= 5000:
            await context.send(embed=embed)
            embed=discord.Embed(title=' '.join(reagent).title() + ' cont.', colour=0x0ff1ce)
    await context.send(embed=embed)

@bot.command(name='recipe', help='Find out the recipe for a craftable.')
async def finding_the_recipe(context, *craftable: str):
    recipe_info = find_recipe(craftable)
    embed=discord.Embed(title=recipe_info['recipe_name'], url = recipe_info['item_url'], color=0xFF5733)
    if recipe_info['ingredients'] != '.':
        embed.add_field(name="**Rank:**", value=recipe_info['rank'], inline=True)
        embed.add_field(name="**Cooldown:**", value=recipe_info['cooldown_timer'], inline=True)
        embed.add_field(name="**Station:**", value=recipe_info['station'], inline=True)
        embed.add_field(name="**Vendor:**", value=recipe_info['vendor'], inline=True)
        embed.add_field(name="**Gold:**", value=recipe_info['gold'], inline=True)
        ingredient_list = ''
        for ingredient in recipe_info['ingredients']:
            ingredient_list += f'{ingredient[0]}  {ingredient[1]}\n'
        embed.add_field(name="**Ingredients:**", value=ingredient_list, inline=False)
    await context.send(embed=embed)

bot.run(os.getenv('BOT_TOKEN'))
