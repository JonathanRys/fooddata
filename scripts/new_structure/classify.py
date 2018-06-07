#!flask/bin/python
from flask import Flask, jsonify, make_response
from classifier.categorize import categorize

app = Flask(__name__)

# Define the endpoints and their respective handlers

# Default method
@app.route('/')
def index():
    return "Please use the endpoint: /fooddata/api/v1.0/tags/ for all requests"


# GET methods
@app.route('/fooddata/api/v1.0/tags/', methods=['GET'])
def tags():
    return "Please provide this API with a comma separated list."

@app.route('/fooddata/api/v1.0/tags/<string:ingredient_list>', methods=['GET'])
def get_tags(ingredient_list):

    # Return the response
    return jsonify(categorize(ingredient_list))


# POST methods
# Accept a JSON array of items via POST
@app.route('/fooddata/api/v1.0/tags/', methods=['POST'])
def post_tags():
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

# Update the data source via their API when a mispelling is found and send alerts when items are unknown to manually update it
# What to do when a product/item is not found?
