import csv
import requests
import os

csv.field_size_limit(2147483647)

possible_ingredients = set()

BASE_URL = "https://world.openfoodfacts.org"

INPUT_FILE = 'en.openfoodfacts.org.products.csv'
OUTPUT_FILE = 'all_ingredients.csv'
COUNTRIES = ['United Kingdom',
             'United States',
             'United-states-of-america',
             'European Union',
             'Canada']

# Animal flesh
RED_MEAT_PRODUCTS = []
PORK_PRODUCTS = []
POULTRY_PRODUCTS = []
FISH_PRODUCTS = []
SHELLFISH_PRODUCTS = []

# Animal products
DAIRY_PRODUCTS = []
EGG_PRODUCTS = []
INSECT_PRODUCTS = []
OTHER_NON_VEGAN = []
RENNET_PRODUCTS = []

# Allergens
WHEAT_PRODUCTS = []
SOY_PRODUCTS = []
NUT_PRODUCTS = []
LEGUME_PRODUCTS = []

# Health (additives)
CARCINOGENIC_PRODUCTS = []
ARTIFICIAL_PRODUCTS = []
SUGAR_PRODUCTS = []
SALT_PRODUCTS = []
OIL_PRODUCTS = []

# Health/Other
RAW_PRODUCTS = [] # ???
ORGANIC_PRODUCTS = []
NON_GMO_PRODUCTS = []
PROCESSED_FOODS = []
PALM_OIL_PRODUCTS = []
JAIN_PRODUCTS = []

def cleanData(data):
    data = data.strip()
    if len(data) and data[-1] == ".":
        data = data[0:-1]
    if len(data) and data[-1] == ")":
        data = data[0:-1]
    if data.count("(") == 1 and data.count(")") == 0:
        data = data.split("(")[1]
    return data

def get_data_stream(url):
    return requests.get(BASE_URL + url, stream=True)

off_data = get_data_stream("/data/en.openfoodfacts.org.products.csv")

counter = 0
f = open(INPUT_FILE, 'wb')
for data in off_data.iter_content(chunk_size=None):
    f.write(data)
    f.flush()
f.close()

####### GET this url instead of reading from file: https://world.openfoodfacts.org/data/en.openfoodfacts.org.products.csv
with open(INPUT_FILE, 'rt', encoding="utf-8") as csvfile:
####### iterate through the rows in the CSV file

    for product in filereader:
        # get the list of ingredients from the product row
        ingredients_text = product['ingredients_text']
        country = product['countries_en']
        
        if ingredients_text is not None and country in COUNTRIES:
            # split the list into seperate ingredients
            ingredients = ingredients_text.split(',')
            for ingredient in ingredients:
                possible_ingredients.add(cleanData(ingredient))
    csvfile.close()

with open(OUTPUT_FILE, 'wt', encoding="utf-8") as outputfile:
    print(possible_ingredients, file=outputfile)
    outputfile.close()

os.remove(INPUT_FILE)

print("done - output written to", OUTPUT_FILE)
