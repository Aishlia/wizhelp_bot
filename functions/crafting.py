import requests
from bs4 import BeautifulSoup
import re
import csv

def item_stats(url):
    resp = requests.get(url)
    page_info = BeautifulSoup(resp.text, 'html.parser')

def recipe_info(url):
    resp = requests.get(url)
    page_info = BeautifulSoup(resp.text, 'html.parser')

    recipe_name = url.split(':')[2].replace('_', ' ')
    if '-' not in recipe_name:
        recipe_name = ''.join([i for i in recipe_name if not i.isdigit()])
    recipe_name = recipe_name.replace('%','')

    try:
        item_link_title = page_info.find('b', text='Item(s) Created:').parent
        item_href = item_link_title.find('a')['href']
        item_url = 'http://www.wizard101central.com' + item_href
    except:
        item_url = 'My sources dunno so I dunno'

    ingredients_section = page_info.find('b', text='Ingredients:').parent.parent.parent
    ingredients = ingredients_section.findAll('td')
    ingredients = ingredients[2:]
    ingredient_names = []
    for ingredient in ingredients:
        if ingredient.find('a'):
            href = ingredient.find('a')['href']
            url = 'http://www.wizard101central.com' + href
            reagent = ingredient.text
            if reagent:
                quant_name = reagent.split(' ', 1)
                quant = quant_name[0]
                name = quant_name[1]
                ingredient_names.append((quant,name))

    recipe_info_section = page_info.find('b', text='Vendor(s):').parent.text
    print(recipe_info_section)
    rank_reg = 'Rank: (.*?)Station:'
    station_reg = 'Station: (.*?)Cooldown Time: '
    cooldown_timer_reg = 'Cooldown Time: (.*?)Half the Time for Subscribing MembersVendor\(s\): '
    vendor_reg = 'Vendor\(s\): (.*?) \('
    gold_reg = '\s\((.*?)\s'
    rank = re.search(rank_reg, recipe_info_section).group(1)
    station = re.search(station_reg, recipe_info_section).group(1)
    try:
        cooldown_timer = re.search(cooldown_timer_reg, recipe_info_section).group(1)
        vendor = re.search(vendor_reg, recipe_info_section).group(1)
        gold = re.search(gold_reg, recipe_info_section).group(1)
    except:
        cooldown_timer = ':('
        vendor = 'This is dumb beastmoon or something'
        gold = 'The wiki makes me sad but still ty to whoever contributes'

    check_lun_crown = recipe_info_section[-20:]
    if 'Lunari' in check_lun_crown:
        gold = gold + ' Lunari'
    elif 'Crown' in check_lun_crown:
        gold = gold + ' Crowns'

    # print(recipe_name, item_url, rank, cooldown_timer, station, vendor, ingredient_names)
    with open('../resources/all_craftable_recipes.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|', quoting = csv.QUOTE_MINIMAL)
        spamwriter.writerow([recipe_name, item_url, rank, cooldown_timer, station, vendor, gold, ingredient_names])

def recipe_type_list(url):
    resp = requests.get(url)
    page_info = BeautifulSoup(resp.text, 'html.parser')
    recipe_section_cols = page_info.find('div', {'class': 'mw-content-ltr'}).findAll('td')
    for col in recipe_section_cols:
        col_recipes = col.findAll('li')
        for recipe in col_recipes:
            href = recipe.find('a')['href']
            url = 'http://www.wizard101central.com' + href
            recipe_info(url)


def recipe_types():
    url = 'http://www.wizard101central.com/wiki/Basic:Crafting'
    resp = requests.get(url)
    page_info = BeautifulSoup(resp.text, 'html.parser')
    recipe_section = page_info.find('div', {'class': 'CategoryTreeSection'})
    recipe_list_section = recipe_section.find('div', {'class': 'CategoryTreeChildren'})
    recipe_list = recipe_list_section.findAll('div', {'class': 'CategoryTreeSection'})

    skip = 25
    ctr = 0

    for recipe_type in recipe_list:
        if ctr < skip:
            ctr  += 1
            continue
        href = recipe_type.find('a')['href']
        url = 'http://www.wizard101central.com/' + href
        print(url)
        if 'Crafted' in url:
            print('SKIP')
            continue
        recipe_type_list(url)

recipe_types()
# recipe_info('http://www.wizard101central.com/wiki/Recipe:Essence_of_Balance_II_(Beastmoon)')
