import os
import en_core_web_sm

from tokenizer.data import stop_words
from tokenizer.tokenizer import tokenizer, translate_to_en_chars, strip_special_chars

en_nlp = en_core_web_sm.load()

dirname = os.path.dirname(__file__)
data_dir = os.path.join(dirname, "tokenizer/data/ingredients")

# Define constants
INPUT_FILE = os.path.join(data_dir, "all_ingredients.txt")
TOKEN_FILE = os.path.join(data_dir, "tkn_ingredients.txt")
OUTPUT_FILE = os.path.join(data_dir, "srtd_ingredients.txt")

# Define functions


def sentence_tokenize(ingredients):
    print(" Tokenizing sentences...")
    tokenized_ingredients = set()

    tokens = tokenizer(ingredients)
    for token in tokens:
        tokenized_ingredients.add(token)

    return tokenized_ingredients


def translate(ingredients):
    print(" Translating characters...")
    return translate_to_en_chars(ingredients)


def word_tokenize(ingredients):
    print(" Applying the spaCy NLP word tokenizer...")
    nlp_ingredients = {}

    # Tokenize the ingredient list
    for ingredient in ingredients:
        nlp_indredient = en_nlp(ingredient)
        for term in nlp_indredient:
            nlp_ingredients[term.lemma_] = term

    return nlp_ingredients


# Get the values of a list as an array
def make_list(obj):
    return [obj[x] for x in obj]


# Remove non-alpha words
def alpha_only(ingredients):
    # This function works on
    print(" Removing non-alpha words e.g. 1-1/2, **, ->, 74, etc.")
    return [x for x in ingredients if x.is_alpha]


# Remove stop words
def remove_stop_words(ingredients):
    print(" Removing stop words...")
    return[x for x in ingredients if not x.is_stop]


# Remove irrelevant parts of speach
def pos_filter(ingredients):
    print(" Filtering based on part of speech...")
    pos_to_keep = ["NOUN", "PROPN"]
    return [x for x in ingredients if x.pos_ in pos_to_keep]


# Remove items with irrelevant tags
def tag_filter(ingredients):
    print(" Filtering based on tag...")
    tags_to_keep = ["JJ", "NN", "NNP"]
    return [x for x in ingredients if x.tag_ in tags_to_keep]


# Extract the stem?  Do I need a different stemmer?
def stem(ingredients):
    print(" Stemming...")
    return [
        x.lemma_ for x in ingredients if x.lemma_ not in stop_words.stop_words]


# Return the word
def get_word(ingredients):
    print(" Getting words...")
    for x in ingredients:
        print("x:", x, ingredients[x])
        exit(0)


# Remove duplicates and sort
def sorted_set(ingredients):
    print(" Removing duplicates...")
    return sorted(set(ingredients))


# Output to file
def write_data(file, data):
    print("Writing to " + file + "...")
    with open(file, "wt", encoding='utf-8') as f:
        for item in data:
            f.write(item + "\n")


def process_data():
    # Check if the required input exists, otherwise create it
    if not os.path.exists(INPUT_FILE) or not os.path.isfile(INPUT_FILE):
        from tokenizer.data.ingredients.itemize import itemize
        try:
            itemize()
        except:
            print("Could not find or create input file", INPUT_FILE)
            exit(0)

    print("Input OK. Reading data...")
    # Ingest the data
    with open(INPUT_FILE, "rt", encoding='utf-8') as f:
        ingredients = f.read()

    # Process the data
    print("Processing...")

    ingredients = sentence_tokenize(ingredients)
    ingredients = translate(ingredients)
    write_data(TOKEN_FILE, ingredients)

    ingredients = word_tokenize(ingredients)
    ingredients_list = make_list(ingredients)
    ingredients_list = alpha_only(ingredients_list)
    ingredients_list = remove_stop_words(ingredients_list)
    ingredients_list = pos_filter(ingredients_list)
    ingredients_list = tag_filter(ingredients_list)
    get_word(ingredients_list)
    ingredients_list = stem(ingredients_list)
    ingredients_list = sorted_set(ingredients_list)

    print("Finished processing.")

    # Output the result
    write_data(OUTPUT_FILE, ingredients_list)

    print("Done.")


if __name__ == '__main__':
    import time
    start_time = time.time()
    print("Sorter started.")
    print("Checking input...")
    process_data()
    print("--- %s seconds ---" % (time.time() - start_time))
