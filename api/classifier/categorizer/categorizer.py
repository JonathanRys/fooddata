"""
=====================
 Product Categorizer
=====================

The main categorization engine for the classifier API.

Dependencies:
    * nltk
    * pyxDamerauLevenshtein(Windows) or jellyfish(Linux)
    * Tokenizer
    * SpellChecker

Available public methods:
    * categorize(list): categorize a list of ingredients

"""

import os
import platform

from nltk.stem import PorterStemmer
from nltk import word_tokenize
from nltk.corpus import stopwords
# from sympound import sympound

if __name__ == '__main__':
    from tokenizer.spell_checker import SpellChecker
    from tokenizer.data.whitelists import whitelists
    from tokenizer.data.stop_words import stop_words
    from tokenizer.tokenizer import tokenizer
else:
    from .tokenizer.spell_checker import SpellChecker
    from .tokenizer.data.whitelists import whitelists
    from .tokenizer.data.stop_words import stop_words
    from .tokenizer.tokenizer import tokenizer

# Use the platform-specific version of the Damerau-Levenshtein distance formula
dam_lev_distance = None

if platform.system() != "Windows":
    from pyxdameraulevenshtein import damerau_levenshtein_distance
    dam_lev_distance = damerau_levenshtein_distance
else:
    from jellyfish import levenshtein_distance
    dam_lev_distance = levenshtein_distance

# Set initial values
debug = False
dirname = os.path.dirname(__file__)
PS = PorterStemmer()
DISTANCE_THRESHHOLD = 4
STEMS_BY_CATEGORY = whitelists["categories"]

# Combine the "stop words" libraries
NLTK_STOP_WORDS = set(stopwords.words('english'))
for x in stop_words:
    NLTK_STOP_WORDS.add(x)

# Preload the categorization data as CATEGORIES
CATEGORIES = {}
for x in STEMS_BY_CATEGORY:
    file_name = STEMS_BY_CATEGORY[x]

    if not os.path.exists(file_name) or not os.path.isfile(file_name):
        if debug:
            print("Unable to load file", file_name)
        continue

    if debug:
        print("Loading", file_name)

    with open(file_name, "rt", encoding='utf-8') as f:
        CATEGORIES[x] = f.read().split("\n")


# Preload the spell checkers
spell_checkers = {}
for x in whitelists["spelling"]:
    if debug:
        print("Loading", whitelists["spelling"][x])
    spell_checkers[x] = SpellChecker(whitelists["spelling"][x])


### Define functions ###

def closest_match(ingredient, category, categories):
    """
    Function to find the best match in a list

    Args:
        ingredient (string): The ingredient to match
        category (string): Matching category
        categories (dict): List of words in given category

    Returns (list): The best matching word in the given category
    """

    if ingredient == None:
        return

    #ingredient_stem = PS.stem(ingredient)
    best_match = [(DISTANCE_THRESHHOLD, "", "")]

    for word in categories:
        if word == None:
            continue

        """Calculate distance"""
        lev_distance = dam_lev_distance(ingredient, word)

        if (lev_distance == 0):
            return (lev_distance, ingredient, category, word)
        """Compare distance with previous best match"""
        if (lev_distance < best_match[0][0]):
            best_match = [(lev_distance, ingredient, category, word)]
        elif (lev_distance == best_match[0][0]):
            best_match.append((lev_distance, ingredient, category, word))

    return best_match


def categorize(ingredient_list):
    """
    Function to categorize a list of ingredients

    Args:
        ingredient_list (list): A list of ingredients to categorize

    Returns (dict): A dictionary of categories containing lists of matches
    """

    tokens = word_tokenize(ingredient_list)

    """Lower case the words and remove punctuation"""
    words = [word.lower() for word in tokens if word.isalpha()]

    """Sort unique words"""
    iterable_list = sorted(
        set([word for word in words if word not in NLTK_STOP_WORDS]))

    """Create a map of words to identify and their original ingredient"""
    ingredient_map = {}
    for x in iterable_list:
        for y in tokenizer(ingredient_list):
            if x in y:
                ingredient_map[x] = y
                break

    """Iterate through the ingredients and find matching tags in the categories data"""
    classified_products = {}
    possible_matches = []

    # TODO: Filter the ingredient to make sure it's just the most significant term
    for ingredient in iterable_list:
        corrected_ingredient = spell_checkers["unidentified"].correct(
            ingredient)
        ingredient_phrase = ingredient_map[ingredient]
        #ingredient_stem = PS.stem(corrected_ingredient)
        nearest = [(DISTANCE_THRESHHOLD, "", "")]

        """Iterate through the categories"""
        for category in CATEGORIES:
            if debug:
                print("category:", category)
            corrected_ingredient = spell_checkers["unidentified"].correct(
                ingredient)
            if debug:
                print("CI:", corrected_ingredient)

            """If the ingredient is a direct match add or append it to the list"""
            if ingredient in CATEGORIES[category]:
                # This needs to replace the original word in entirety, not just the category
                ingredient = ingredient_phrase.replace(
                    ingredient, corrected_ingredient)

                classified_products = add_or_append(
                    classified_products, category, ingredient)

                nearest = []
                break
            else:
                """Find the closest match in the nearest category"""
                closest = closest_match(
                    ingredient, category, CATEGORIES[category])

                if closest[0][0] < nearest[0][0]:
                    nearest = closest
                elif closest[0][0] == nearest[0][0]:
                    nearest.append(closest[0])

        for match in correct_ingredient(nearest, ingredient, ingredient_phrase):
            possible_matches.append(match)
        # push to an array here and use find_best()

    final_ingredients = find_best(possible_matches)

    classified_products = put_in_category(
        final_ingredients, classified_products)

    if debug:
        print("Classified Products:", classified_products)

    return classified_products


def add_or_append(base_dict, key, value, conditional=True):
    """
    Add or append a value to a dictionary

    Args:
        base_dict (dict): The existing dictionary to modify
        key (string): The key to add or append to
        value (string): The value to give that key
        [Optional] conditional (bool): exclusion parameter

    Returns (dict): A new dictionary with the provided key/value pair added
    """

    new_dict = {x: base_dict[x] for x in base_dict}
    """Check if the key already exists"""
    if key in new_dict:
        if conditional:
            """Append the value to the existing array"""
            if value not in new_dict[key]:
                new_dict[key].append(value)
    else:
        """Add the new value"""
        new_dict[key] = [value]

    return new_dict


def correct_ingredient(tags, ingredient, ingredient_phrase):
    """
    Apply a spelling correction to the entire text of an ingredient.

    Args:
        tags (list): List of tuples containing corrected tags
        ingredient (string): The ingredient to replace
        ingredient_phrase (string): The ingredient to fix

    Returns (list): A list of tuples containing the corrected phrases
    """

    corrected_ingredients = []
    UNKNOWN_WORD = "???"

    for tag in tags:
        if debug:
            print("### Tag:", tag)

        category = tag[2]
        product = tag[1]

        if (category == ''):
            category = "unidentified"
            product = ingredient

        corrected_ingredient = spell_checkers[category].correct(product)

        if debug:
            print("Correcting", product, "in", category)

        corrected_phrase = ingredient_phrase.replace(
            ingredient, product+"("+(UNKNOWN_WORD, corrected_ingredient)[product != corrected_ingredient]+")")
        corrected_ingredients.append((tag[0], corrected_phrase, category))

    return corrected_ingredients


def find_best(tags):
    """
    Find the category that the product matches best

    Args:
        tags (list): List of tags

    Returns (list): A new list containing the best matches
    """
    products = set()
    product_map = {}

    categories = set()
    new_tags = []

    for tag in tags:
        if debug:
            print("tag:", tag)
        category = tag[2]
        product = tag[1]
        rank = tag[0]

        products.add(product)
        categories.add(category)

        if product in product_map:
            if category in product_map[product]:
                if product_map[product][category] > rank:
                    product_map[product]
            else:
                product_map[product][category] = rank
        else:
            product_map[product] = {}
            product_map[product][category] = rank

    for product in products:
        for category in product_map[product]:
            new_tags.append(
                (product_map[product][category], product, category))

    return new_tags


def put_in_category(tags, categories):
    """
    A function to convert an array of product-tag pairs into a dict with categories
    as keys.

    Args:
        tags (list): Categorized tags
        categories (list): List of all available categories

    Returns (dict): A dictionary of categories mapped to ingredients
    """
    new_categories = {x: categories[x] for x in categories}

    for tag in tags:
        # assign values to readable names
        category = tag[2]
        product = tag[1]
        category_exists = False

        corrected_product = spell_checkers[category].correct(product)
        stemmed_product = PS.stem(corrected_product)
        if category in new_categories:
            category_exists = not stemmed_product in new_categories[category]

        new_categories = add_or_append(
            new_categories, category, product, category_exists)

    return new_categories


def test():
    TEST_STRING = "aplles, celert, banana, fried calms"
    print("Categorizing:", TEST_STRING)
    result = categorize(TEST_STRING)
    print("Result:", result)

    TEST_STRING = "celery, chery, bannas, boletus edulis, apple, orange"
    print("Categorizing:", TEST_STRING)
    result = categorize(TEST_STRING)
    print("Result:", result)

# celery,%20chery,%20bannas,%20boletus%20edulis,%20apple,%20orange
# aplles,%20celert,%20banana,%20fried%20calms


if __name__ == '__main__':
    test()
