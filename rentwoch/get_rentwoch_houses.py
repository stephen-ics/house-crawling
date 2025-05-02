import requests
from bs4 import BeautifulSoup
from dateutil import parser

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

def parseHouse(html):
    bsObj = BeautifulSoup(html, "html.parser")
    
    housingDetails = bsObj.find("div", class_="details")

    parseLeaseStartDate(housingDetails)
    
def parseLeaseStartDate(bsObj):
    title_text_element = bsObj.find("h1", class_="title_text")

    if not title_text_element:
        return None

    title_text = title_text_element.text
    lease_start_date_unformatted = title_text.split("-")[0].strip(" ")
    lease_start_date = formatDate(lease_start_date_unformatted)

    print(lease_start_date)

def formatDate(date_str):
    try:
        if date_str.lower() == "immediately":
            return "Immediately"
        elif "contact" in date_str.lower():
            return "Contact for more details"

        parsed_date = parser.parse(date_str)
        return parsed_date.date()
    except (ValueError, TypeError):
        return None

html = get_rentwoch_listings()
links = parse_listing_links(html=html)

link_1 = links[0]
html = call_listing_api(link_1)
parseHouse(html)

# for link in links:
#     html = call_listing_api(link)
#     parseHouse(html)
