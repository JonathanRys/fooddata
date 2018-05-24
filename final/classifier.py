#!flask/bin/python
from flask import Flask, jsonify, make_response

app = Flask(__name__)

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
    f = open(x[1], "r")
    
    if f.mode == "r":
        roots[x[0]] = f.read().split("\n")
        
    f.close()

# Define the endpoints and their respective handlers

# Default method
@app.route('/')
def index():
    return "Please use the endpoint: /fooddata/api/v1.0/tags/ for all requests"


# GET methods
@app.route('/fooddata/api/v1.0/tags/', methods=['GET'])
def tags():
    return "Please provide this API with a comma separated list."

@app.route('/fooddata/api/v1.0/tags/<string:ingr_list>', methods=['GET'])
def get_tags(ingredient_list):
    iterable_list = [x.strip() for x in ingredient_list.split(",")]
    # Iterate through this list and find matching tags

    # Return the response
    return jsonify({'ingredients': iterable_list})


# POST methods
# Accept a JSON array of items via POST
@app.route('/fooddata/api/v1.0/tags/', methods=['POST'])
def post_tags(ingr_list):
    if not request.json or not 'ingredients' in request.json:
        abort(400)


# Error handling
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)


# accept input as list or array

# use naive Bayes to classify

# find similar words using Levenshtein distance

# return JSON response

