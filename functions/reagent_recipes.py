import csv

def reagent_recipes_lookup(reagent):
    with open('resources/reagent_table.csv', 'r') as re:
        reader = csv.DictReader(re, delimiter='|')

        for row in reader:
            # print(row)
            if row['reagent'].lower() == ' '.join(reagent).lower():
                return eval(row['items'])
    return [('','This Reagent Does not exist')]
