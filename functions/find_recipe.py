import requests
from bs4 import BeautifulSoup
import re
from googlesearch import search
import csv

def find_recipe(item_name):
    with open('resources/all_craftable_recipes.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')

        for row in reader:
            if ' '.join(item_name).lower().replace("'", '') == row['recipe_name'].lower():
                print(' '.join(item_name).lower().replace("'", ''))
                recipe_info = {
                    "recipe_name": row['recipe_name'],
                    "item_url": row['item_url'],
                    "rank": row['rank'],
                    "cooldown_timer": row['cooldown_timer'],
                    "station": row['station'],
                    "vendor": row['vendor'],
                    "gold": row['gold'],
                    "ingredients": eval(row['ingredient_names']),
                }
                return recipe_info

    with open('resources/all_craftable_recipes.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')

        query = '+'.join(item_name)+' recipe wizard101central'
        search_results = search(query, 10)
        for result in search_results:
            if 'wizard101central' in result and 'Recipe:' in result:
                url = result
                resp = requests.get(url)
                page_info = BeautifulSoup(resp.text, 'html.parser')
                break

        item_name_google = page_info.find('h1', {'id':'firstHeading'}).get_text().replace('Recipe:', '')
        print(item_name_google)
        accept_name = item_name_google.strip().lower().replace("'", '')
        for row in reader:
            if accept_name == row['recipe_name'].lower():
                recipe_info = {
                    "recipe_name": item_name_google,
                    "item_url": row['item_url'],
                    "rank": row['rank'],
                    "cooldown_timer": row['cooldown_timer'],
                    "station": row['station'],
                    "vendor": row['vendor'],
                    "gold": row['gold'],
                    "ingredients": eval(row['ingredient_names']),
                }
                return recipe_info

        recipe_info = {
            "recipe_name": 'Cannot find the recipe',
            "item_url": 'https://google.com',
            "rank": '.',
            "cooldown_timer": '.',
            "station": '.',
            "vendor": '.',
            "gold": '.',
            "ingredients": '.',
        }
        return recipe_info
