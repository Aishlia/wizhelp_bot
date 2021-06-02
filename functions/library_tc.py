import csv
import os

# with open('resources/library_tc_raw.txt', 'r') as f:
#     lines = f.readlines()
#
# with open('resources/library_tc.csv', 'w') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter='|', quoting = csv.QUOTE_MINIMAL)
#
#     library = ''
#     location = ''
#     vendor_name = ''
#
#     for line in lines:
#         if not line.strip():
#             continue
#         elif ('Library' in line or 'The Archivist' in line) and ('Vendor' not in line):
#             library = line.strip()
#         elif 'Vendor Location' in line:
#             location = line.strip()[17:]
#         elif 'Vendor Name' in line:
#             vendor_name = line.strip()[13:]
#         else:
#             card = line.split(' - ')[0]
#             price = str(line.split(' - ')[1].split(' ')[0].strip())
#             spamwriter.writerow([library, location, vendor_name, card, price])

def wtb_tc(tc_name):  # where to buy treasure card
    with open('resources/library_tc.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        # library, location, librarian, spell, cost = ("",)
        tc_info = {
           "library": 'Not available for purchase',
           "location": '',
           "librarian": '',
           "spell": '',
           "cost": '',
        }

        for row in reader:
            if ' '.join(tc_name).lower() == row['spell'].lower():
                library = row['library']
                location = row['location']
                librarian = row['librarian']
                spell = row['spell']
                cost = row['cost']

                tc_info = {
                    "library": library,
                    "location": location,
                    "librarian": librarian,
                    "spell": spell,
                    "cost": cost,
                }
                break

        return tc_info

# print(wtb_tc('ice shield'))
