"""
========================
 Spelling to categories
========================

"""

from spacy_sorter import process_data
from tokenizer.data.whitelists import whitelists


def spell_to_category():
    whitelists["categories"]["all"] = whitelists["spelling"]["all"].replace("dictionaries", "categories")

    for x in whitelists["spelling"]:
        print("Converting", whitelists["spelling"][x], "=>", whitelists["categories"][x])
        process_data(whitelists["spelling"][x], whitelists["categories"][x])


if __name__ == '__main__':
    spell_to_category()
