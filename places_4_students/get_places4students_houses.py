import requests
from bs4 import BeautifulSoup

from utils import getHousingID
from parse_house import parse_house
from format_data import write_houses_csv

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

def call_places4students_house_api(params, cookies):
    url = "https://www.places4students.com/Places/Details"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(url, params=params, cookies=cookies, headers=headers)
    return response 

def get_places4students_house(housingID):
    params = {
        "SchoolID": "VBThwOQPAX4="
    }

    params["housingID"] = housingID

    cookies={
        "ASP.NET_SessionId": "qmxwdtlxlffde1t3e4s0bff5",
        "Places4StudentDisclaimer": "Agree",
        "__AntiXsrfToken": "e24d51e2de26447ca1d222b78e0085b2"
    }

    response = call_places4students_house_api(params=params, cookies=cookies)
    return response

def parse_listings(html):
    bsObj = BeautifulSoup(html, features="html.parser")
    listingsTable = bsObj.find("table", class_="StdTable")
    listings = listingsTable.find_all("tr", class_="featured")

    houses = []
    for listing in listings:
        listingDate = listing.find("td", class_="listing-occupancy-date")
        houseIDElement = listingDate.find("a", href=True)

        match = re.search(r'HousingID=([^&]+)', houseIDElement["href"])
        
        if match == None:
            continue

        houseID = match.group(1)
        response = get_places4students_house(houseID)

        houses.append(response.text)

    return houses


response = get_places4students_listings()
html = parse_listings(response)
rows = parse_house(html)
write_houses_csv(rows, "places4students.csv")