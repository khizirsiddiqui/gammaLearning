import requests
from random import randint

API_KEY = 'c3de6e8138da4d3793ad348e53597a71'

url = ('https://newsapi.org/v2/top-headlines?'
       'country=in&'
       'apiKey='+API_KEY)


def get_news():
    articles = []
    response = requests.get(url).json()
    if response['status'] == 'ok':
        results_len = response['totalResults']
        for i in range(0, results_len):
            article = dict()
            article = {'title': response['articles'][i]['title'], 'source': response['articles'][i]['source']['name'], 'url': response['articles'][i]['url']}
            articles.append(article)
            if i == 6:
                break
    return articles

