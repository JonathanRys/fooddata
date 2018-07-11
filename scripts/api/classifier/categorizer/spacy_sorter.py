import os
import en_core_web_sm

from tokenizer.data import stop_words
from tokenizer.tokenizer import tokenizer, translate_to_en_chars, strip_special_chars
from tokenizer.spell_checker import SpellChecker

en_nlp = en_core_web_sm.load()

dirname = os.path.dirname(__file__)
data_dir = os.path.join(dirname, "tokenizer/data/ingredients")

spell_checker = SpellChecker('all')

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
    """Translate non-English letters to English"""
    print(" Translating characters...")
    return translate_to_en_chars(ingredients)


def word_tokenize(ingredients):
    """Tokenizes on words"""
    print(" Applying the spaCy NLP word tokenizer...")
    nlp_ingredients = {}

    """Tokenize the ingredient list"""
    for ingredient in ingredients:
        nlp_indredient = en_nlp(ingredient)
        for term in nlp_indredient:
            nlp_ingredients[term.lemma_] = term

    return nlp_ingredients


def make_list(obj):
    """Gets the values of a list as an array"""
    return [obj[x] for x in obj]


def alpha_only(ingredients):
    """Removes non-alpha words"""
    print(" Removing non-alpha words e.g. 1-1/2, **, ->, 74, etc.")
    return [x for x in ingredients if x.is_alpha]


def remove_stop_words(ingredients):
    """Removes stop words"""
    print(" Removing stop words...")
    return[x for x in ingredients if not x.is_stop]


def pos_filter(ingredients):
    """Removes irrelevant parts of speach"""
    print(" Filtering based on part of speech...")
    pos_to_keep = ["NOUN", "PROPN"]
    return [x for x in ingredients if x.pos_ in pos_to_keep]


def tag_filter(ingredients):
    """Removes items with irrelevant tags"""
    print(" Filtering based on tag...")
    tags_to_keep = ["JJ", "NN", "NNP"]
    return [x for x in ingredients if x.tag_ in tags_to_keep]


def stem(ingredients):
    """Extract the stem?  Do I need a different stemmer?"""
    print(" Stemming...")
    return [
        x.lemma_ for x in ingredients if x.lemma_ not in stop_words.stop_words]


def no_stem(ingredients):
    """Extract the stem?  Do I need a different stemmer?"""
    print(" Stemming...")
    return [
        x.text for x in ingredients if x.text not in stop_words.stop_words]



def get_word(ingredients):
    """Returns the word"""
    print(" Getting words...")
    counter = 0
    for x in ingredients:
        counter += 1
        print("x:", x, ingredients[x])
        if counter > 250:
            exit(0)

def get_token(ingredients):
    """Returns the word"""
    print(" Getting words...")
    counter = 0
    for x in ingredients:
        counter += 1
        print("x:", x)
        if counter > 250:
            exit(0)
        


def sorted_set(ingredients):
    """Removes duplicates and sort"""
    print(" Removing duplicates...")
    return sorted(set(ingredients))


def write_data(file, data):
    """Outputs to file"""
    print("Writing to " + file + "...")
    with open(file, "wt", encoding='utf-8') as f:
        for item in data:
            f.write(item + "\n")


def process_data(input_file, output_file):
    """Process """
    # Check if the required input exists, otherwise create it
    if not os.path.exists(input_file) or not os.path.isfile(input_file):
        from .tokenizer.data.ingredients.itemize import itemize
        try:
            itemize()
        except:
            print("Could not find or create input file", input_file)
            exit(0)

    print("Input OK. Reading data...")
    # Ingest the data
    with open(input_file, "rt", encoding='utf-8') as f:
        ingredients = f.read()

    # Process the data
    print("Processing...")

    ingredients = sentence_tokenize(ingredients)
    ingredients = translate(ingredients)
    #write_data(TOKEN_FILE, ingredients)

    ingredients = word_tokenize(ingredients)
    # get_word(ingredients)
    
    ingredients_list = make_list(ingredients)
    ingredients_list = alpha_only(ingredients_list)
    ingredients_list = remove_stop_words(ingredients_list)
    #get_token(ingredients_list)
    #ingredients_list = pos_filter(ingredients_list)
    #ingredients_list = tag_filter(ingredients_list)
    #get_token(ingredients_list)

    #ingredients_list = stem(ingredients_list)
    ingredients_list = no_stem(ingredients_list)
    ingredients_list = [x for x in ingredients_list if len(x) > 2]
    ingredients_list = [spell_checker.correct(x) for x in ingredients_list]
    ingredients_list = sorted_set(ingredients_list)
    
    # get_word(ingredients)
    
    print("Finished processing.")

    # Output the result
    write_data(output_file, ingredients_list)

    print("Done.")


if __name__ == '__main__':
    import time
    start_time = time.time()
    print("SpaCy Sorter started.")
    print("Checking input...")
    process_data(INPUT_FILE, OUTPUT_FILE)
    print("--- %s seconds ---" % (time.time() - start_time))
