import os
import en_core_web_sm

from tokenizer.data import stop_words
from tokenizer.tokenizer import tokenizer, translate_to_en_chars, strip_special_chars

en_nlp = en_core_web_sm.load()

dirname = os.path.dirname(__file__)
dirname = os.path.join(dirname, "tokenizer/data/ingredients")

# Check if this exists
INPUT_FILE = os.path.join(dirname, "all_ingredients.txt")
TOKEN_FILE = os.path.join(dirname, "tkn_ingredients.txt")
OUTPUT_FILE = os.path.join(dirname, "srtd_ingredients.txt")

if not os.path.exists(INPUT_FILE) or not os.path.isfile(INPUT_FILE):
    from tokenizer.data.ingredients.itemize import itemize
    print("File not found: ", INPUT_FILE)
    exit(0)
    #itemize()

print("Input OK. Reading data...")

# Ingest ingredients
with open(INPUT_FILE, "rt", encoding='utf-8') as f:
    ingredients = f.read()

print("Tokenizing ingredients...")
tokenized_ingredients = set()

tokens = tokenizer(ingredients)
for token in tokens:
    tokenized_ingredients.add(token)

# Free this memory up
ingredients = ""

print("Translating characters...")
# Reassign the result to conserve memory
tokenized_ingredients = translate_to_en_chars(tokenized_ingredients)

# Write tokenized_ingredients to file for testing models on
with open(TOKEN_FILE, "wt", encoding='utf-8') as f:
    for ingredient in tokenized_ingredients:
        f.write(ingredient + "\n")

#tokenized_ingredients = {}
nlp_ingredients = {}

# Process the data to remove irellevant and/or useless terms
print("Processing...")

# Tokenize the ingredient list
for ingredient in tokenized_ingredients:
    nlp_indredient = en_nlp(ingredient)
    for term in nlp_indredient:
        nlp_ingredients[term.lemma_] = term
    
tokenized_ingredients = {}

print("Applying the NLP tokenizer...")
# Remove non-alpha characters
nlp_ingredients = [nlp_ingredients[x] for x in nlp_ingredients if nlp_ingredients[x].is_alpha]

print("Removing stop words...")
# Remove stop words
nlp_ingredients = [x for x in nlp_ingredients if not x.is_stop]

print("Filtering based on part of speech...")
# Remove irrelevant parts of speach
pos_to_keep = ["NOUN", "PROPN"]
nlp_ingredients = [x for x in nlp_ingredients if x.pos_ in pos_to_keep]

print("Filtering based on tag...")
# Remove items with irrelevant tags
tags_to_keep = ["JJ", "NN", "NNP"]
nlp_ingredients = [x for x in nlp_ingredients if x.tag_ in tags_to_keep]

print("Stemming...")
# Extract the stem?  Do I need a different stemmer?
nlp_ingredients = [x.lemma_ for x in nlp_ingredients if x.lemma_ not in stop_words.stop_words]

print("Removing duplicates...")
# Remove duplicates and sort
nlp_ingredients = sorted(set(nlp_ingredients))

print("Finished processing.")

# Finish outputing the result
print("Writing to file...")

# Output to file
with open(OUTPUT_FILE, "wt", encoding='utf-8') as f:
    for word in nlp_ingredients:
        f.write(word + "\n")

print("Done.")
