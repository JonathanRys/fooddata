import en_core_web_sm
from tokenizer.tokenizer import list_tokenize
from tokenizer.data.stop_words import stop_words

en_nlp = en_core_web_sm.load()

FILE_NAME = "tokenizer/data/categories/ARTIFICIAL_PRODUCTS.txt"
# FILE_NAME = "ALCOHOL_PRODUCTS.txt"

# Ingest ingredients
with open(FILE_NAME, "rt", encoding='utf-8') as f:
    ingredients = f.read()

ingredients = list_tokenize.list_tokenize(ingredients)
ingredients = list_tokenize.translate_to_en_chars(ingredients)

# Process the data to remove irellevant and useless terms
print("Processing...")

pos_to_keep = ["NOUN", "PROPN"]
tags_to_keep = ["JJ", "NN", "NNP"]

# Tokenize the ingredient list
tokenized_ingredients = {}

for ingredient in ingredients:
    token_list = en_nlp(ingredient)
    for token in token_list:
        tokenized_ingredients[token.lemma_] = token

# Remove non-alpha characters
alpha_only = [tokenized_ingredients[x]
              for x in tokenized_ingredients if tokenized_ingredients[x].is_alpha]

# Remove stop words
no_stop = [x for x in alpha_only if not x.is_stop]

# Remove irrelevant parts of speach
pos_filtered = [x for x in no_stop if x.pos_ in pos_to_keep]

# Remove items with irrelevant tags
tag_filtered = [x for x in pos_filtered if x.tag_ in tags_to_keep]

# Extract the stem?  Do I need a different stemmer?
lemmas_only = [x.lemma_ for x in tag_filtered if x.lemma_ not in stop_words]

# Remove duplicates and sort
sorted_significant_items = sorted(set(lemmas_only))

print("Finished processing.")

# Finish outputing the result
print("Writing to file...")

# Output to file
f = open(FILE_NAME, "wt", encoding='utf-8')
for word in sorted_significant_items:
    f.write(word + "\n")

f.close()

print("Done.")
