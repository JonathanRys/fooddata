import os
import collections
import re

dirname = os.path.dirname(__file__)

whitelist = {
    "spelling":{
        "alcohol": os.path.join(dirname, 'data/dictionaries/spelling_alcohol.txt'),
        "artificial": os.path.join(dirname, 'data/dictionaries/spelling_artificial.txt'),
        "carcinogens": os.path.join(dirname, 'data/dictionaries/spelling_carcinogens.txt'),
        "dairy": os.path.join(dirname, 'data/dictionaries/spelling_dairy.txt'),
        "eggs": os.path.join(dirname, 'data/dictionaries/spelling_eggs.txt'),
        "fish": os.path.join(dirname, 'data/dictionaries/spelling_fish.txt'),
        "fruits": os.path.join(dirname, 'data/dictionaries/spelling_fruits.txt'),
        "grains": os.path.join(dirname, 'data/dictionaries/spelling_grains.txt'),
        "insects": os.path.join(dirname, 'data/dictionaries/spelling_insects.txt'),
        "legumes": os.path.join(dirname, 'data/dictionaries/spelling_legumes.txt'),
        "mushrooms": os.path.join(dirname, 'data/dictionaries/spelling_mushrooms.txt'),
        "non_vegan": os.path.join(dirname, 'data/dictionaries/spelling_non_vegan.txt'),
        "nuts": os.path.join(dirname, 'data/dictionaries/spelling_nuts.txt'),
        "oil": os.path.join(dirname, 'data/dictionaries/spelling_oil.txt'),
        "pork": os.path.join(dirname, 'data/dictionaries/spelling_pork.txt'),
        "poultry": os.path.join(dirname, 'data/dictionaries/spelling_poultry.txt'),
        "processed": os.path.join(dirname, 'data/dictionaries/spelling_processed.txt'),
        "red_meat": os.path.join(dirname, 'data/dictionaries/spelling_red_meat.txt'),
        "rennet": os.path.join(dirname, 'data/dictionaries/spelling_rennet.txt'),
        "seeds": os.path.join(dirname, 'data/dictionaries/spelling_seeds.txt'),
        "shellfish": os.path.join(dirname, 'data/dictionaries/spelling_shellfish.txt'),
        "spices": os.path.join(dirname, 'data/dictionaries/spelling_spices.txt'),
        "vegetables": os.path.join(dirname, 'data/dictionaries/spelling_vegetables.txt'),
        "wheat": os.path.join(dirname, 'data/dictionaries/spelling_wheat.txt'),
        "all": os.path.join(dirname, 'data/dictionaries/spelling.dict'),
    }
}

class SpellChecker:

    def __init__(self, dict_file):
        with open(dict_file) as f:
            self.words = collections.Counter(self.get_words(f.read()))

    def P(self, word):
        N = sum(self.words.values())
        "Probability of `word`."
        return self.words[word] / N

    def correct(self, word):
        "Most probable spelling correction for word."
        return max(self.candidates(word), key=self.P)

    def candidates(self, word):
        sig = self.case_signature(word)
        word = word.lower()
        return [self.apply_signature((self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word]), sig)]

    def known(self, words):
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self.words)

    def edits1(self, word):
        "All edits that are one edit away from `word`."
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))

    def get_words(self, text): return re.findall(r'\w+', text.lower())

    def case_signature(self, word):
        signature = ""

        for letter in word:
            code = ord(letter)
            if code in [32]:
                signature += " "
            elif code > 64:
                if code < 91:
                    signature += "X"
                elif code > 96 and code < 123:
                    signature += "x"
                else:
                    signature += "_"
            else:
                signature += "_"

        return signature

    def apply_signature(self, words, signature):
        for word in words:
            if len(word) > len(signature):
                for i in range(len(signature), len(word)):
                    signature += signature[-1]
            temp = word.lower()
            output = ""

            for letter, token in zip(temp, signature):
                if token == "X":
                    output += letter.upper()
                else:
                    output += letter

        return output


def test():
    fruit_test = SpellChecker(whitelist['spelling']['fruits'])
    mush_test = SpellChecker(whitelist['spelling']['mushrooms'])
    veg_test = SpellChecker(whitelist['spelling']['vegetables'])

    assert(fruit_test.correct("Appil") == "Apple")
    assert(mush_test.correct("Portabella") == "Portobello")
    assert(veg_test.correct("celry") == "celery")
    assert(veg_test.correct("celeryz") == "celery")
    assert(veg_test.correct("cElryz") == "cElery")

    print("All tests passed.\n")

    spell_checker = SpellChecker(whitelist['spelling']['all'])
    
    while True:
        input_word = input("Enter a word to correct, 'z' for option[z] or 'q' to [q]uit: ")

        if input_word == 'q':
            break
        elif input_word == 'z':
            while True:
                dictionary = input("Enter dictionary name or 'all' for default:")
                if dictionary in whitelist['spelling']:
                    spell_checker = SpellChecker(whitelist['spelling'][dictionary])
                    break;
                else:
                    print("\nERROR: Dictionary not found.")
                    print("Please choose one of:\n    alcohol\n    artificial\n    carcinogens\n    dairy\n    eggs\n    fish\n    fruits\n    grains\n    insects\n    legumes\n    mushrooms\n    non_vegan\n    nuts\n    oil\n    pork\n    poultry\n    processed\n    red_meat\n    rennet\n    seeds\n    shellfish\n    spices\n    vegetables\n    wheat\n")
            continue            
        elif " " in input_word or not len(input_word):
            print("Please enter a single word.")
            continue;

        corrected_word = spell_checker.correct(input_word)

        print("Corrected word:", corrected_word)

if __name__ == '__main__':
    test()


    
