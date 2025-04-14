import requests
from bs4 import BeautifulSoup

import re

def call_places4students_listings_api(params, cookies):
    url = "https://www.places4students.com/Places/PropertyListings"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(url, params=params, cookies=cookies, headers=headers)
    return response

def get_places4students_listings():
    params = {
        "SchoolID": "VBThwOQPAX4=",
    }

    cookies={
        "ASP.NET_SessionId": "qmxwdtlxlffde1t3e4s0bff5",
        "Places4StudentDisclaimer": "Agree",
        "__AntiXsrfToken": "e24d51e2de26447ca1d222b78e0085b2"
    }

    response = call_places4students_listings_api(params=params, cookies=cookies)
    return response.text


def parse_listings(html):
    bsObj = BeautifulSoup(html, features="html.parser")
    listingsTable = bsObj.find("table", class_="StdTable")
    listing = listingsTable.find("tr", class_="featured")

    listingDate = listing.find("td", class_="listing-occupancy-date")
    houseIDElement = listingDate.find("a", href=True)
    
    houseID = re.search(r'HousingID=([^&]+)', houseIDElement["href"]).group(1)

    response = get_places4students_house(houseID)
    return response.text




