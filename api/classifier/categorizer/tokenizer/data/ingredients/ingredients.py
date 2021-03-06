import csv
import requests
import os

csv.field_size_limit(2147483647)

possible_ingredients = set()

BASE_URL = "https://world.openfoodfacts.org"
INPUT_FILE = 'en.openfoodfacts.org.products.csv'
OUTPUT_FILE = 'raw_ingredients.txt'
COUNTRIES = ['United Kingdom',
             'United States',
             'United-states-of-america',
             'European Union',
             'Canada']

""" Open a data stream to download the massive data file"""
def get_data_stream(url):
    return requests.get(BASE_URL + url, stream=True)

"""Extract the ingredients from the CSV file and save it to disk"""
def get_source_data():
    print(" >> Downloading data...")
    off_data = get_data_stream("/data/en.openfoodfacts.org.products.csv")

    f = open(INPUT_FILE, 'wb')
    # chunk_size = 100MB chunks
    for data in off_data.iter_content(chunk_size=10240 * 10240):
        f.write(data)
        f.flush()
    f.close()

    print(" >> done.\n")
    print(" >> Processing data...")

    if not os.path.exists(INPUT_FILE) or not os.path.isfile(INPUT_FILE):
        # Raise an exception here instead
        return False

    """Read CSV file"""
    with open(INPUT_FILE, 'rt', encoding="utf-8") as csvfile:
        """Iterate through the rows in the CSV file"""
        filereader = csv.DictReader(
            csvfile, delimiter='\t', quoting=csv.QUOTE_NONE)
        for product in filereader:
            """get the list of ingredients from the product row"""
            ingredients_text = product['ingredients_text']
            country = product['countries_en']

            """Only save ingredients for the countries specified"""
            if ingredients_text is not None and country in COUNTRIES:
                possible_ingredients.add(ingredients_text)

    """Save the data to disk"""
    with open(OUTPUT_FILE, 'wt', encoding="utf-8") as outputfile:
        for ingredient in possible_ingredients:
            outputfile.write(ingredient + "\n")

    """Delete the CSV file"""
    os.remove(INPUT_FILE)

    print(" >> Writing to", OUTPUT_FILE, "\n")
    return True

# print or return stats? # [(# of ingredients, # of products, # words removed), etc...]


if __name__ == '__main__':
    get_source_data()
