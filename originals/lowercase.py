# Ingest ingredients
INPUT_FILE_NAME = "ARTIFICIAL_PRODUCTS.txt"
OUTPUT_FILE_NAME = "lowercased_ARTIFICIAL_PRODUCTS.txt"

f = open(INPUT_FILE_NAME, "r", encoding='utf-8')

if f.mode == "r":
    raw_ingredients = f.read().split("\n")
    
f.close()

lowercased_ingredients = sorted(set([x.lower().strip() for x in raw_ingredients]))

f = open(OUTPUT_FILE_NAME, "w", encoding='utf-8')

for word in lowercased_ingredients:
    f.write(word + "\n")

f.close()
