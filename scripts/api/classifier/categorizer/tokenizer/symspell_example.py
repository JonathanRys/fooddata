import os

from sympound import sympound

import platform
distancefun = None
if platform.system() != "Windows":
    from pyxdameraulevenshtein import damerau_levenshtein_distance
    distancefun = damerau_levenshtein_distance
else:
    from jellyfish import levenshtein_distance
    distancefun = levenshtein_distance


ssc = sympound(distancefun=distancefun, maxDictionaryEditDistance=3)

def test():

    if ssc.load_dictionary("big.txt"):
        print(ssc.lookup_compound(input_string="brocoli", edit_distance_max=3))

    result = distancefun("crapple", "apple")
    print(result)
    #ssc.save_pickle("symspell.pickle")
    #ssc.load_pickle("symspell.pickle")
    #print(ssc.lookup_compound(input_string="བཀྲ་ཤས་བད་ལེགས། ལ་མ་", edit_distance_max=3))

if __name__ == '__main__':
    test()
