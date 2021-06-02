import csv
from collections import defaultdict
import pprint

with open('../resources/all_craftable_recipes.csv', 'r') as re, open('../resources/reagent_table.csv', 'w') as wr:
    reader = csv.DictReader(re, delimiter='|')

    reagent_table = defaultdict(list)

    for row in reader:
        reagents = eval(row['ingredient_names'])
        for reagent in reagents:
            reagent = reagent[1]
            reagent_table[reagent].append((row['recipe_name'], row['item_url']))

    fieldnames = ['reagent', 'items']
    writer = csv.DictWriter(wr, delimiter='|', fieldnames=fieldnames)
    writer.writeheader()
    for keys, value in reagent_table.items():
        print(keys, value)
        writer.writerow({'reagent':keys, 'items':value})
