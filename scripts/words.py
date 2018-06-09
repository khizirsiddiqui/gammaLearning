import json
from random import randint
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
word_file = os.path.join(THIS_FOLDER, 'word_list.json')


def rand_word():
    with open(word_file, encoding="utf8") as f:
        jsonData = json.load(f)
        word = jsonData[randint(0, len(jsonData)-1)]
        return word
