import re
import operator
import nltk

from nltk.stem import PorterStemmer

FILE_NAME = "roots_MUSHROOMS.txt"

ps = PorterStemmer()

def main():
    f = open(FILE_NAME, "r")
    if f.mode == "r":
        file_contents = f.read()

    f.close()

    # print(file_contents)
    
    all_words = split_on_words(file_contents)
    # Remove whitespace
    all_words = [x for x in all_words if not x in ["", " ", "   "]]

    num_words = len(all_words)
    
    # print(all_words)
    print("processed all_words")
    
    lowercase_words = make_lower_case(all_words)
    # print(lowercase_words)
    print("processed lowercase_words")

    stemmed_words = stem(lowercase_words)
    # print(stemmed_words)
    print("processed stemmed_words")

    unique_words = set(stemmed_words)

    f = open("final_" + FILE_NAME, "w")
    
    for word in unique_words:
        f.write(word + "\n")

    f.close()
    
    print("found", len(unique_words), "unique words in", num_words, "words")

def split_on_words(string):
    return re.split(r'\W+', string)

def make_lower_case(words):
    new_list = []
    
    for word in words:
        new_list.append(word.lower())

    return new_list

def stem(words):
    new_list = []
    
    for word in words:
        new_list.append(ps.stem(word))

    return new_list

def count_instances(list):
    word_counts = {}

    for word in list:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    return sorted(word_counts.items(), key=operator.itemgetter(1))
        

if __name__ == "__main__":
    main();
