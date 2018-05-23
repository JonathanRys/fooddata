import re
import operator
import nltk

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

FILE_NAME = "SPICES.txt"

ps = PorterStemmer()

print(FILE_NAME)

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

    tagged_words = nltk.pos_tag(all_words)
    # print(tagged_words)
    print("processed tagged_words")
    
    significant_words = [x for x in tagged_words if not x[1] in ["CC", "CD", "DT", "IN"]]
    significant_words = [x[0] for x in significant_words]
    # print(significant_words)
    print("processed significant_words")

    stemmed_words = stem(significant_words)
    # print(stemmed_words)
    print("processed stemmed_words")

    counted_words = count_instances(stemmed_words)

    f = open("counts_" + FILE_NAME, "w")
    
    for word in counted_words:
        f.write(word[0])
        f.write(": ")
        f.write(str(word[1]))
        f.write("\n")

    f.close()
    
    unique_words = set(stemmed_words)

    f = open("unique_" + FILE_NAME, "w")
    
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
