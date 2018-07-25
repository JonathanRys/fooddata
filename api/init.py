# Check for the existence of the data
# and run any steps to fetch/create missing data

# check for classifier/categorizer/tokenizer/data/ingredients/raw_ingredients.txt
# else run ingredients.py -> get_source_data()

# check for classifier/categorizer/tokenizer/data/ingredients/all_ingredients.txt
# else run itemize -> itemize()

# check for classifier/categorizer/tokenizer/data/foods.txt
# else run spelling_scraper -> spelling_scraper()

from classifier.classifier import app
import os

def init():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    init()
