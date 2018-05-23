import re

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

FILE_NAME = "FRUITS.txt"

ps = PorterStemmer()

def main():
    f = open(FILE_NAME, "r")
    if f.mode == "r":
        contents = f.read()
        # print(contents)

    f.close()
    print(splitOnWords("it's party time!"))
    print(makeLowerCase("TESTING"))
    print(stem("testing"), stem("tested"), stem("tests"))

def splitOnWords(string):
    return re.split(r'\W+', string)

def makeLowerCase(string):
    return string.lower();

def stem(word):
    return ps.stem(word)

if __name__ == "__main__":
    main();
