import re
import operator
import nltk

from sets import Set

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

FILE_NAME = "FRUITS.txt"

ps = PorterStemmer()

test_string = "This is a test string to tokenize"

test_result = word_tokenize(test_string)

#print nltk.pos_tag(test_result)




def main():
    f = open(FILE_NAME, "r")
    if f.mode == "r":
        file_contents = f.read()

    f.close()

    # print file_contents
    
    all_words = split_on_words(file_contents)
    # Remove whitespace
    all_words = [x for x in all_words if not x in ["", " ", "   "]]

    num_words = len(all_words)
    
    # print all_words
    print "processed all_words"
    
    lowercase_words = make_lower_case(all_words)
    # print lowercase_words
    print "processed lowercase_words"

    tagged_words = nltk.pos_tag(all_words)
    for word in tagged_words:
        print word

    print "processed tagged_words"
    
    significant_words = [x for x in tagged_words if x[1] in ["CC", "CD", "DT", "IN"]]
    significant_words = [x[0] for x in significant_words]
    # print significant_words
    print "processed significant_words"

    stemmed_words = stem(significant_words)
    # print stemmed_words
    print "processed stemmed_words"

    #print count_instances(stemmed_words)
    
    unique_words = Set(stemmed_words)

    for word in unique_words:
        print word
    
    print "found", len(unique_words), "unique words in", num_words, "words"

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
