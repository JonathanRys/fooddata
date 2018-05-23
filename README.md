# foodfacts
Data about ingredients in food

This repo is a data dump and transformation process using NLP to identify and classify ingredients from ingredient lists derived from crowd-sourced data.

The goal of this project is to build an API that can take an ingredient list and identify allergens, carcinogens, and other concerns about ingredients.  The API will take a comma-seperated list or an array of ingredients and return a JSON object in the following format:

{
  tags: ["legume", "gluten", "fruit", "vegetable"],
  legume: ["chickpeas"],
  gluten: ["whole wheat flour"],
  fruit: ["tomato"],
  vegetable: ["tomato", "onion"]
}
