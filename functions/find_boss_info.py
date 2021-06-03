import requests
from bs4 import BeautifulSoup
import re
from googlesearch import search

def find_boss_info(boss_name):
    url = 'http://www.wizard101central.com/wiki/Creature:' + str('_'.join(boss_name)).title()
    resp = requests.get(url)
    page_info = BeautifulSoup(resp.text, 'html.parser')
    if page_info.find('div', {'class':'noarticletext'}):
        print('couldn\'t find wiki')
        query = '+'.join(boss_name)+' boss wizard101'
        search_results = search(query, 5)
        for result in search_results:
            if 'wizard101central' in result:
                print(result)
                url = result
                resp = requests.get(url)
                page_info = BeautifulSoup(resp.text, 'html.parser')
                break

    boss_proper_name = page_info.find('h1', {'id':'firstHeading'}).get_text().replace('Creature:', '')

    general_info = page_info.find('div', {'id': 'relative-top'})
    general_info = general_info.findAll('tr')
    health = general_info[3].findAll('td')[1].get_text()

    starting_pips = page_info.find('td', text='Starting Pips').parent()[2].text.strip()
    starting_pips = [int(word) for word in starting_pips.split() if word.isdigit()]
    starting_pips = str(starting_pips[0])

    boosts_info = page_info.find('td', text='Inc. Boost').parent()[2]
    out = boosts_info.text.strip() + ' '
    boost_classes = boosts_info.findAll('a')
    for i in boost_classes:
        spell_type = i['title'][9:]
        out += spell_type + ' and '
    boosts = out[:-5]

    resists_info = page_info.find('td', text='Inc. Resist').parent()[2]
    out = resists_info.text.strip() + ' '
    resists_classes = resists_info.findAll('a')
    for i in resists_classes:
        spell_type = i['title'][9:]
        out += spell_type + ' and '
    resists = out[:-5]

    try:
        cheats = page_info.find('div', text='Cheats').parent()[1].get_text()
    except:
        cheats = 'This boss has no cheats'

    boss_info = {
        'boss_name': boss_proper_name,
        'health': health,
        'starting_pips': starting_pips,
        'boosts': boosts,
        'resists': resists,
        'cheats': cheats,
    }

    return boss_info

# find_boss_info(['gladiatordimachaelus'])
