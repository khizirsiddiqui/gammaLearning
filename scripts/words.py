import json
from random import randint


def rand_word():
    with open('scripts/word_list.json', encoding="utf8") as f:
        jsonData = json.load(f)
        word = jsonData[randint(0, len(jsonData)-1)]
        return word
