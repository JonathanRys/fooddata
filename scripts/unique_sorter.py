# Ingest ingredients
INPUT_FILE_NAME = "lowercased_ARTIFICIAL_PRODUCTS.txt"
OUTPUT_FILE_NAME = "unique_sorted_ARTIFICIAL_PRODUCTS.txt"

f = open(INPUT_FILE_NAME, "r", encoding='utf-8')

if f.mode == "r":
    raw_ingredients = f.read().split("\n")
    
f.close()

unique_sorted_ingredients = sorted(set(raw_ingredients.strip()))

f = open(OUTPUT_FILE_NAME, "w", encoding='utf-8')

for word in unique_sorted_ingredients:
    f.write(word + "\n")

f.close()



