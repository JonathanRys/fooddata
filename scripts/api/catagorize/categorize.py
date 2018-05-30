from nltk.stem import PorterStemmer
from nltk import word_tokenize
from nltk.corpus import stopwords
import os

dirname = os.path.dirname(__file__)

ps = PorterStemmer()
distance_threshhold = 4
stop_words = set(stopwords.words('english'))

# Define the tags and their associated stem files
stems_by_category = {
    ('alcohol', os.path.join(dirname, "../../../final/final_roots_ALCOHOL.txt")),
    ('carcinogen', os.path.join(dirname, "../../../final/final_roots_CARCINOGENS.txt")),
    ('fruit', os.path.join(dirname, "../../../final/final_roots_FRUITS.txt")),
    ('mushroom', os.path.join(dirname, "../../../final/final_roots_MUSHROOMS.txt")),
    ('rennet', os.path.join(dirname, "../../../final/final_roots_RENNET.txt")),
    ('shellfish', os.path.join(dirname, "../../../final/final_roots_SHELLFISH.txt")),
    ('vegetable', os.path.join(dirname, "../../../final/final_roots_VEGETABLES.txt"))
}

# Preload the data into memory
roots = {}
for x in stems_by_category:
    f = open(x[1], "r", encoding='utf-8')

    if f.mode == "r":
        roots[x[0]] = f.read().split("\n")
        
    f.close()

# 
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
    
    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890_-"
    w = dict( (x, (1, 1, 1)) for x in alphabet + alphabet.upper())
    
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
            subs = max( (w[s[row-1]][2], w[t[col-1]][2]))
            if s[row-1] == t[col-1]:
                subs = 0
            else:
                subs = subs
            dist[row][col] = min(dist[row-1][col] + deletes,
                                 dist[row][col-1] + inserts,
                                 dist[row-1][col-1] + subs) # substitution
 
    return dist[row][col]


# Function to find the best match in a list
def closest_match(ingredient, root, roots):
    ingredient_stem = ps.stem(ingredient)
    best_match = [(distance_threshhold, "", "")]
    
    for root_stem in roots:
        # Calculate distance
        lev_distance = get_lev_distance(ingredient_stem, root_stem)

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
    tags = {}
    

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
                if root in tags:
                    tags[root].append(ingredient)
                else:
                    tags[root] = [ingredient]
                nearest = []
                break
            else:
                closest = closest_match(ingredient_stem, root, roots[root])

                print("Closest:", closest)

                if closest[0][0] < nearest[0][0]:
                    nearest = closest
                elif closest[0][0] == nearest[0][0]:
                    nearest.append(closest[0])

                print("Nearest:", nearest)
                    
        for tag in nearest:
            if tag[2] in tags:
                if not tag[1] in tags[tag[2]]:
                    tags[tag[2]].append(tag[1])
            else:
                tags[tag[2]] = [tag[1]]

    return tags
