# Ingest ingredients
INPUT_FILE_NAME = "spelling.dict"
OUTPUT_FILE_NAME = "all_spelling.txt"

f = open(INPUT_FILE_NAME, "r", encoding='utf-8')

if f.mode == "r":
    raw_ingredients = f.read().split(" ")
    
f.close()

unique_sorted_ingredients = set()

for x in raw_ingredients:
     unique_sorted_ingredients.add(x.strip())

f = open(OUTPUT_FILE_NAME, "w", encoding='utf-8')

for word in sorted(unique_sorted_ingredients):
    f.write(word + "\n")

f.close()



