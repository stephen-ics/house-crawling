import requests
from bs4 import BeautifulSoup

def call_rentwoch_api(params):
    url = "https://rentwoch.com/?limit=100&wplpage=1"
    
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/134.0.0.0 Safari/537.36",
    }
    
    response = requests.get(url, params=params, headers=headers)
    return response


def get_rentwoch_listings():
    params = {
        "limit": 100,
        "wplpage": 1,
    }

    response = call_rentwoch_api(params)  
    return response