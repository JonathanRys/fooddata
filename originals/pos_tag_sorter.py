import en_core_web_sm

en_nlp = en_core_web_sm.load()

# FILE_NAME = "ARTIFICIAL_PRODUCTS.txt"
FILE_NAME = "ALCOHOL_PRODUCTS.txt"

# Ingest ingredients
f = open(FILE_NAME, "r", encoding='utf-8')

if f.mode == "r":
    ingredients = f.read().split("\n")
    
f.close()

# Define output dicts
pos = {}
tag = {}

print("Processing...")

# Process the data to remove irellevant and useless terms
for ingredient in ingredients:
    tokenized_ingredients = en_nlp(ingredient)

    alpha_only = [x for x in tokenized_ingredients if x.is_alpha]

    no_stop = [x for x in alpha_only if not x.is_stop]

    for token in alpha_only_no_stop:
        if token.pos_ not in pos:
            pos[token.pos_] = set()
            
        if token.tag_ not in tag:
            tag[token.tag_] = set()

        pos[token.pos_].add(token.lemma_)
        tag[token.tag_].add(token.lemma_)
            

print("Finished processing.")
print("Writing to pos file...")

for types in pos:
    f = open("spacy_pos_" + types + "_" + FILE_NAME, "w", encoding='utf-8')
    for word in pos[types]:
        f.write(word + "\n")

    f.close()

print("Parts of speach processed.")
print("Writing to tag file...")

for types in tag:
    f = open("spacy_tag_" + types + "_" + FILE_NAME, "w", encoding='utf-8')
    for word in tag[types]:
        f.write(word + "\n")

    f.close()
    
print("Tags processed.")
print("Done.")
