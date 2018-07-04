"""
========================
 Spelling List Stripper
========================

A module to take the data from spelling_scraper and spacy_sorter
and combine them into a sorted list of unique items.

Dependencies:
    * SpellChecker

Available public methods:
    * spelling_list_stripper()

"""

import os
from spell_checker import SpellChecker

dirname = os.path.dirname(__file__)
spell_checker = SpellChecker('all')

UNIQUE_FILE = os.path.join(dirname, "data/words_new/_unique.txt")
CORRECTED_FILE = os.path.join(dirname, "data/words_new/corrected.txt")
UNKNOWN_FILE = os.path.join(dirname, "data/words_new/unknown.txt")
FOUND_FILE = os.path.join(dirname, "data/words_new/found.txt")


def read_data(file, delimiter="\n"):
    """Read the data from a file and return a list"""
    with open(file, 'rt', encoding="utf-8") as f:
        data = f.read()

    return data.split(delimiter)


def save_data(file, data):
    """Save the data from an iterable to file"""
    with open(file, 'wt', encoding="utf-8") as f:
        f.write("\n".join(data))


def get_data():
    """
    Read the data from input files

    :returns: The list of all words
    :rtype: list
    """

    # This should be read from config somewhere; OK for now
    OFF_DATA = os.path.join(dirname, "data/ingredients/srtd_ingredients.txt")
    WIKI_DATA = os.path.join(dirname, "data/spelling_scraper/foods.txt")

    return read_data(OFF_DATA)
    return read_data(OFF_DATA) + read_data(WIKI_DATA, " ")


def filter_unique(items):
    """
    Filter out stop words and return only unique values

    :param items: A list of items to filter
    :type items: list
    :returns: A unique sorted list from the list passed in
    :rtype: list
    """

    unique_words = set()
    print("    removing", len(spell_checker.stopwords), "stop words...")
    for item in items:
        if not item in spell_checker.stopwords:
            if item.capitalize() in spell_checker.stopwords:
                unique_words.add('~' + item)
            else:
                unique_words.add(item)

    print("    removing duplicates...")

    return sorted([x for x in unique_words])


def spelling_list_stripper():
    """
    A function to take a list of ingredients and
    attempt to identify every word.  This function
    outputs to four files referenced by these variables:
        * UNIQUE_FILE    - Unique set of every word sans stopwords
        * CORRECTED_FILE - Any words that were corrected
        * UNKNOWN_FILE   - Words the spell checker doesn't know
        * FOUND_FILE     - Words that are correctly spelled

    :param: None
    :returns: None
    """

    print("Starting: ")
    print("  ingesting data...")
    data = get_data()
    print("  filtering data...")
    filtered_data = filter_unique(data)
    # Save results
    print("  saving filtered data...")
    save_data(UNIQUE_FILE, filtered_data)

    corrected = []
    unknown = []
    found = []
    print("  checking spelling...")
    for x in filtered_data:
        if len(x) == 0:
            continue
        corrected_word = spell_checker.correct(x)
        if corrected_word == x:
            found.append(x)
        elif corrected_word == None:
            unknown.append(x)
        else:
            corrected.append(x + ": " + corrected_word)

    print("  saving results...")
    save_data(CORRECTED_FILE, corrected)
    save_data(UNKNOWN_FILE, unknown)
    save_data(FOUND_FILE, found)
    print("done.")


if __name__ == '__main__':
    spelling_list_stripper()
