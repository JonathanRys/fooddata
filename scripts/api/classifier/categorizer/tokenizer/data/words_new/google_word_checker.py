import requests
import json


json_decoder = json.JSONDecoder()

def get_url(query):
    return "https://www.googleapis.com/customsearch/v1?key=AIzaSyDaYXKAxaPYsAFLz4ysVCWTMOht7lRo4SE&cx=009800307687027833122:z4j_j_yubki&q=" + query

def get_data(url):
    return requests.get(url).text

def read_data(file, delimiter="\n"):
    """Read the data from a file and return a list"""
    with open(file, 'rt', encoding="utf-8") as f:
        data = f.read()

    return data.split(delimiter)

def get_correction(word):
    url = get_url(word)
    data = json_decoder.decode(get_data(url))

    if "spelling" in data and "correctedQuery" in data["spelling"]:
        print(word, "=", data["spelling"]["correctedQuery"])

def google_word_checker():
    data = read_data("unknown.txt")
    for x in data:
        get_correction(x)

if __name__ == '__main__':
    #get_correction("acidstarter")
    google_word_checker()
