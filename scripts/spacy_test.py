import en_core_web_sm

state = {
    "selected_language": 0
}

languages = ["en", "es", "fr"]

en_nlp = en_core_web_sm.load()

doc = en_nlp(u'After tokenization, spaCy can parse and tag a given Doc. This is where the statistical model comes in, which enables spaCy to make a prediction of which tag or label most likely applies in this context. A model consists of binary data and is produced by showing a system enough examples for it to make predictions that generalise across the language – for example, a word following "the" in English is most likely a noun.')



for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
          token.shape_, token.is_alpha, token.is_stop)

alpha_only_no_stops = [x for x in doc if x.is_alpha and not x.is_stop]

print("\n")
for token in alpha_only_no_stops:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
          token.shape_, token.is_alpha, token.is_stop)
