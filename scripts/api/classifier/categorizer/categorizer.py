import os
import platform

from nltk.stem import PorterStemmer
from nltk import word_tokenize
from nltk.corpus import stopwords
# from sympound import sympound

from tokenizer.spell_checker import SpellChecker
from tokenizer.data.whitelists import whitelists
from tokenizer.data.stop_words import stop_words
from tokenizer.tokenizer import tokenizer

"""Use the platform-specific version of the Damerau-Levenshtein distance formula"""
dam_lev_distance = None

if platform.system() != "Windows":
    from pyxDamerauLevenshtein import damerau_levenshtein_distance
    dam_lev_distance = damerau_levenshtein_distance
else:
    from jellyfish import levenshtein_distance
    dam_lev_distance = levenshtein_distance

"""Set initial values"""
dirname = os.path.dirname(__file__)
PS = PorterStemmer()
DISTANCE_THRESHHOLD = 4
STEMS_BY_CATEGORY = whitelists["categories"]

"""Combine the "stop words" libraries"""
NLTK_STOP_WORDS = set(stopwords.words('english'))
for x in stop_words:
    NLTK_STOP_WORDS.add(x)

"""Preload the categorization data"""
ROOTS = {}
for x in STEMS_BY_CATEGORY:
    file_name = STEMS_BY_CATEGORY[x]

    if not os.path.exists(file_name) or not os.path.isfile(file_name):
        print("Unable to load file", file_name)
        continue

    print("Loading", file_name)

    with open(file_name, "rt", encoding='utf-8') as f:
        ROOTS[x] = f.read().split("\n")


"""Preload the spell checkers"""
spell_checkers = {}
for x in whitelists["spelling"]:
    print("Loading", whitelists["spelling"][x])
    spell_checkers[x] = SpellChecker(whitelists["spelling"][x])


### Define functions ###

"""Function to find the best match in a list"""


def closest_match(ingredient, root, roots):
    ingredient_stem = PS.stem(ingredient)
    best_match = [(DISTANCE_THRESHHOLD, "", "")]

    for root_stem in roots:
        if ingredient_stem == None or root_stem == None:
            continue

        """Calculate distance"""
        lev_distance = dam_lev_distance(ingredient_stem, root_stem)

        if (lev_distance == 0):
            return (lev_distance, ingredient, root)
        """Compare distance with previous best match"""
        if (lev_distance < best_match[0][0]):
            best_match = [(lev_distance, ingredient, root)]
        elif (lev_distance == best_match[0][0]):
            best_match.append((lev_distance, ingredient, root))

    return best_match


"""Function to categorize a list of ingredients"""


def categorize(ingredient_list):
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

    """Iterate through this list and find matching tags"""
    classified_products = {}
    """Filter the ingredient to make sure it's just the most significant term"""
    for ingredient in iterable_list:
        corrected_ingredient = spell_checkers["all"].correct(ingredient)
        ingredient_phrase = ingredient_map[ingredient]
        ingredient_stem = PS.stem(corrected_ingredient)
        nearest = [(DISTANCE_THRESHHOLD, "", "")]

        """Iterate through the categories"""
        for root in ROOTS:
            corrected_ingredient = spell_checkers[root].correct(ingredient)

            """If the ingredient is a direct match add or append it to the list"""
            if ingredient_stem in ROOTS[root]:
                ingredient = ingredient_phrase.replace(
                    ingredient, corrected_ingredient)

                classified_products = add_or_append(
                    classified_products, root, ingredient)

                nearest = []
                break
            else:
                """Find the closest match in the nearest category"""
                closest = closest_match(ingredient_stem, root, ROOTS[root])

                if closest[0][0] < nearest[0][0]:
                    nearest = closest
                elif closest[0][0] == nearest[0][0]:
                    nearest.append(closest[0])

        final_ingredients = correct_ingredient(nearest, ingredient_phrase)

        classified_products = put_in_category(
            final_ingredients, classified_products)

    return classified_products


"""Add or append a value to a dictionary"""


def add_or_append(base_dict, key, value, conditional=True):
    new_dict = {x: base_dict[x] for x in base_dict}
    """Check if the key already exists"""
    if key in new_dict:
        if conditional:
            """Append the value to the existing array"""
            new_dict[key].append(value)
    else:
        """Add the new value"""
        new_dict[key] = [value]

    return new_dict


def correct_ingredient(nearest, ingredient_phrase):
    corrected_ingredients = []

    for tag in nearest:
        category = tag[2]
        product = tag[1]

        corrected_product = spell_checkers[category].correct(product)
        corrected_phrase = ingredient_phrase.replace(
            product, corrected_product)
        corrected_ingredients.append((tag[0], corrected_phrase, category))

    return corrected_ingredients


def put_in_category(tags, categories):
    new_categories = {x: categories[x] for x in categories}

    for tag in tags:
        category = tag[2]
        product = tag[1]

        corrected_product = spell_checkers[category].correct(product)
        stemmed_product = PS.stem(corrected_product)
        if category in new_categories:
            category_exists = not stemmed_product in new_categories[category]

        print("Calling add_or_append(pic):", new_categories, category, product)
        new_categories = add_or_append(
            new_categories, category, product, category_exists)

    return new_categories


def test():
    result = categorize("aplles, celert, banana, fried calms")
    print("Result:", result)


if __name__ == '__main__':
    test()
