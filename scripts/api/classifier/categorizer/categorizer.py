from nltk.stem import PorterStemmer
from nltk import word_tokenize
from nltk.corpus import stopwords
import os

from .tokenizer.spell_correct import correct
from sympound import sympound

import platform
dam_lev_distance = None
if platform.system() != "Windows":
    from pyxdameraulevenshtein import damerau_levenshtein_distance
    dam_lev_distance = damerau_levenshtein_distance
else:
    from jellyfish import levenshtein_distance
    dam_lev_distance = levenshtein_distance

dirname = os.path.dirname(__file__)

ps = PorterStemmer()
distance_threshhold = 4
stop_words = set(stopwords.words('english'))

# Define the tags and their associated stem files
stems_by_category = {
    ('alcohol', os.path.join(dirname, "./tokenizer/data/categories/alcohol.txt")),
    ('carcinogen', os.path.join(dirname, "./tokenizer/data/categories/carcinogens.txt")),
    ('fruit', os.path.join(dirname, "./tokenizer/data/categories/fruits.txt")),
    ('mushroom', os.path.join(dirname, "./tokenizer/data/categories/mushrooms.txt")),
    ('rennet', os.path.join(dirname, "./tokenizer/data/categories/rennet.txt")),
    ('shellfish', os.path.join(dirname, "./tokenizer/data/categories/shellfish.txt")),
    ('vegetable', os.path.join(dirname, "./tokenizer/data/categories/vegetables.txt"))
}

# Preload the data into memory
roots = {}
for x in stems_by_category:
    f = open(x[1], "rt", encoding='utf-8')

    if f.mode == "rt":
        roots[x[0]] = f.read().split("\n")

    f.close()

# This is the categorizer for the API to match against the model


def get_lev_distance(s, t):
    """ 
        iterative_levenshtein(s, t) -> ldist
        ldist is the Levenshtein distance between the strings 
        s and t.
        For all i and j, dist[i,j] will contain the Levenshtein 
        distance between the first i characters of s and the 
        first j characters of t

    """
    rows = len(s)+1
    cols = len(t)+1
    col = 0

    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890_-èñãâï¿"
    w = dict((x, (1, 1, 1)) for x in alphabet + alphabet.upper())

    dist = [[0 for x in range(cols)] for x in range(rows)]
    # source prefixes can be transformed into empty strings
    # by deletions:
    for row in range(1, rows):
        dist[row][0] = dist[row-1][0] + w[s[row-1]][0]
    # target prefixes can be created from an empty source string
    # by inserting the characters
    for col in range(1, cols):
        dist[0][col] = dist[0][col-1] + w[t[col-1]][1]

    for col in range(1, cols):
        for row in range(1, rows):
            deletes = w[s[row-1]][0]
            inserts = w[t[col-1]][1]
            subs = max((w[s[row-1]][2], w[t[col-1]][2]))
            if s[row-1] == t[col-1]:
                subs = 0
            else:
                subs = subs
            dist[row][col] = min(dist[row-1][col] + deletes,
                                 dist[row][col-1] + inserts,
                                 dist[row-1][col-1] + subs)  # substitution

    return dist[row][col]


# Function to find the best match in a list
def closest_match(ingredient, root, roots):
    ingredient_stem = ps.stem(ingredient)
    best_match = [(distance_threshhold, "", "")]

    for root_stem in roots:
        # Calculate distance
        # lev_distance = get_lev_distance(ingredient_stem, root_stem)
        lev_distance = dam_lev_distance(ingredient_stem, root_stem)

        if (lev_distance == 0):
            return (lev_distance, ingredient, root)
        # Compare distance with previous best match
        if (lev_distance < best_match[0][0]):
            best_match = [(lev_distance, ingredient, root)]
        elif (lev_distance == best_match[0][0]):
            best_match.append((lev_distance, ingredient, root))

    return best_match


# Function to categorize a list of ingredients
def categorize(ingredient_list):
    # Move all of this into it's own function once it works so that it can be used by POST

    # iterable_list = [x.strip() for x in ingredient_list.split(",")]
    tokens = word_tokenize(ingredient_list)

    # Lower case the words and remove punctuation
    words = [word.lower() for word in tokens if word.isalpha()]

    # Sort unique words
    iterable_list = sorted(set(words))

    # Iterate through this list and find matching tags
    classified_products = {}

    # Filter the ingredient to make sure it's just the most significant term
    for ingredient in iterable_list:
        ingredient_stem = ps.stem(ingredient)
        nearest = [(distance_threshhold, "", "")]

        # Iterate through the categories
        for root in roots:

            # Split on whitespace then semicolons and find % match(es) in each item:
            # Use Levenshtein distance to find the best match in each group
            #    based on it's distance
            # Return a single match per ingredient unless otherwise specified
            # How to find a best match but still deal with multiple categories?

            # This is the simplest logic
            if ingredient_stem in roots[root]:
                if root in classified_products:
                    classified_products[root].append(ingredient)
                else:
                    classified_products[root] = [ingredient]
                nearest = []
                break
            else:
                closest = closest_match(ingredient_stem, root, roots[root])

                #print("Closest:", closest)

                if closest[0][0] < nearest[0][0]:
                    nearest = closest
                elif closest[0][0] == nearest[0][0]:
                    nearest.append(closest[0])

                #print("Nearest:", nearest)

        for tag in nearest:
            print(tag)
            category = tag[2]
            product = tag[1]
            if category in classified_products:
                if not correct(product) in classified_products[category]:
                    classified_products[category].append(correct(product))
            else:
                classified_products[category] = [correct(product)]

    return classified_products
