import json
from random import randint
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


url_1_one_random = 'http://quotes.stormconsultancy.co.uk/random.json'
url_2_complete_list = 'http://quotes.stormconsultancy.co.uk/quotes.json'
url_3_popular = 'http://quotes.stormconsultancy.co.uk/popular.json'


def read_quotes():
    with open('scripts/quotes.json', encoding="utf8") as f:
        lines = (l.strip() for l in f)
        quotes = [json.loads(l) for l in lines if l]
        return (quotes[randint(0, len(quotes)-1)])


img_quotes_file = os.path.join(THIS_FOLDER, 'quotes_img.json')


def img_quotes():
    with open(img_quotes_file, encoding="utf8") as f:
        jsonData = json.load(f)
        quote = jsonData[randint(0, len(jsonData)-1)]
        return quote
