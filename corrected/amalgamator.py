import os
import re

dirname = os.path.dirname(__file__)

def strip_special_chars(string):
    return re.sub(r"[^A-z^0-9^ ^\-^_]|\\|\^|\]|\[", " ", string)

def amalgamate():
    files = []

    for file in os.listdir(dirname):
        if file.endswith(".txt"):
            files.append(os.path.join(dirname, file))

    mega_corpus = ""

    for file in files:
        print("Ingesting",  file)
        
        with open(file, "rt", encoding="utf-8") as f:
            mega_corpus = f.read()
            
    mega_corpus = strip_special_chars(mega_corpus)
    mega_corpus = mega_corpus.replace(" ", "\n")

    all_words = mega_corpus.split("\n")

    each_word = set()

    for word in all_words:
        stripped_word = word.strip(r"[\'\" \*\(\{\[\]\}\)\.\:\;\-\_\\\/]")

        each_word.add(stripped_word)
        each_word.add(stripped_word.lower())
        each_word.add(stripped_word.capitalize())


    with open("spelling.dict", "wt", encoding="utf-8") as f:
        for word in sorted(each_word):
            if len(word) > 1:
                f.write(word + "\n")

if __name__ == '__main__':
    amalgamate()

