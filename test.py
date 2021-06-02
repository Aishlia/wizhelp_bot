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

import requests
from bs4 import BeautifulSoup

url = 'http://www.wizard101central.com/wiki/Creature:' + 'marcio'
resp = requests.get(url)
page_info = BeautifulSoup(resp.text, 'html.parser')
general_info = page_info.find('div', {'id': 'relative-top'})
general_info = general_info.findAll('tr')
health = general_info[3].findAll('td')[1].get_text()

boosts_info = page_info.find('td', text='Inc. Boost').parent()[2]
boosts = boosts_info.text.strip()
boost_classes = boosts_info.findAll('a')
for i in boost_classes:
    output = i['title']
    output = output[9:]
    print(output)
