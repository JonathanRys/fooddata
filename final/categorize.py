from nltk.stem import PorterStemmer

ps = PorterStemmer()
distance_threshhold = 4

# Define the tags and their associated stem files
stems_by_category = {
    ('alcohol', "final_roots_ALCOHOL.txt"),
    ('carcinogen', "final_roots_CARCINOGENS.txt"),
    ('fruit', "final_roots_FRUITS.txt"),
    ('mushroom', "final_roots_MUSHROOMS.txt"),
    ('rennet', "final_roots_RENNET.txt"),
    ('shellfish', "final_roots_SHELLFISH.txt"),
    ('vegetable', "final_roots_VEGETABLES.txt")
}

# Preload the data into memory
roots = {}
for x in stems_by_category:
    f = open(x[1], "r", encoding='utf-8')

    if f.mode == "r":
        roots[x[0]] = f.read().split("\n")
        
    f.close()



# Function to calculate the Levenshtein distance between two words
##def get_lev_distance(word_one, word_two):
##    if word_one == "":
##        return len(word_two)
##    if word_two == "":
##        return len(word_one)
##    if word_one[-1] == word_two[-1]:
##        cost = 0
##    else:
##        cost = 1
##       
##    distance = min([get_lev_distance(word_one[:-1], word_two)+1,
##               get_lev_distance(word_one, word_two[:-1])+1, 
##               get_lev_distance(word_one[:-1], word_two[:-1]) + cost])
##    return distance

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
    # Remove whitespace
    iterable_list = [x.strip() for x in ingredient_list.split(",")]
    # iterable_list = word_tokenize(ingredient_list)


    # Iterate through this list and find matching tags
    tags = {}
    nearest = [(distance_threshhold, "", "")]

    # Filter the ingredient to make sure it's just the most significant term
    for ingredient in iterable_list:
        ingredient_stem = ps.stem(ingredient)

        # Iterate through the categories
        for root in roots:
            
            # Split on whitespace then semicolons and find % match(es) in each item:
            # Use Levenshtein distance to find the best match in each group
            #    based on it's distance
            # return a single match per ingredient unless otherwise dictated
            # How to find a best match but still deal with multiple categories?


            # This is the simplest logic
            if ingredient_stem in roots[root]:
                if root in tags:
                    tags[root].append(ingredient)
                else:
                    tags[root] = [ingredient]
            else:
                closest = closest_match(ingredient_stem, root, roots[root])
                print("Nearest:", closest)
                if closest[0][0] < nearest[0][0]:
                    for tag in closest:
                        if tag in tags:
                            tags[root].append(tag[1])
                        else:
                            tags[root] = [tag[1]]

    return tags
