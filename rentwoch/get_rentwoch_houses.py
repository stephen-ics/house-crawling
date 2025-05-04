import requests
from bs4 import BeautifulSoup
from dateutil import parser
from parse_house import parse_house

def call_rentwoch_api(params):
    url = "https://rentwoch.com/?limit=100&wplpage=1"
    
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mawc OS X 10_15_7) "
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

    response = call_rentwoch_api(params=params)  
    return response.text

def parse_listing_links(html):
    bsObj = BeautifulSoup(html, "html.parser")
    property_list = bsObj.find("div", class_ = "wpl_property_listing_listings_container")
    properties = property_list.find_all("div", class_="wpl-column")
    links = []

    for property in properties:
        a = property.find("a", class_="view_detail", href=True)
        link = a["href"]
        links.append(link)
    
    return links

def call_listing_api(listing_url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/134.0.0.0 Safari/537.36",
    }

    response = requests.get(listing_url, headers=headers)
    return response.text

html = get_rentwoch_listings()
links = parse_listing_links(html=html)

link_1 = links[0]
html = call_listing_api(link_1)
parse_house(html)
