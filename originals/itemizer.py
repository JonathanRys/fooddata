import re

def list_tokenizer(list_of_items):
    return list_of_items

def remove_non_alpha(text_body):
    return 

def split_list(list_to_split):
    return [x.strip() for x in re.split("or|and|[\n,;]+", list_to_split)]

print(split_list("Hi there, do you and your friend want to play; or not?"))
