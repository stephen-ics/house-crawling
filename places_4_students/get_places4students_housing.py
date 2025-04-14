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
    listing = listingsTable.find("tr", class_="featured")

    listingDate = listing.find("td", class_="listing-occupancy-date")
    houseIDElement = listingDate.find("a", href=True)
    
    houseID = re.search(r'HousingID=([^&]+)', houseIDElement["href"]).group(1)

    response = get_places4students_house(houseID)
    return response.text

def parse_house(html):
    bsObj = BeautifulSoup(html, features="html.parser")

    address = parse_address(bsObj=bsObj)

def parse_text(unformattedText, prefix):
    pattern = rf'{re.escape(prefix)}\s+(.+)'
    match = re.search(pattern, unformattedText, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None 

def parse_address(bsObj):
    housingInformation = bsObj.find("div", class_="loaction-container")

    unformattedStreet = housingInformation.find("span", id="MainContent_Label3").parent.get_text()
    street = parse_text(unformattedStreet, "Address:")

    unformattedCity = housingInformation.find("div", id="MainContent_trCity").get_text()
    city = parse_text(unformattedCity, "City:")

    unformattedProvince = housingInformation.find("div", id="MainContent_trProvince").get_text()
    province = parse_text(unformattedProvince, "State/Province:")
    if province == "Ontario":
        province = "ON"

    unformattedCountry = housingInformation.find("div", id="MainContent_trCountry").get_text()
    country = parse_text(unformattedCountry, "Country:")

    unformattedPostalCode = housingInformation.find("div", id="MainContent_trZip").get_text()
    postalCode = parse_text(unformattedPostalCode, "Zip/Postal Code:")

    address = f"{street}, {city}, {province} {postalCode}, {country}"
    print(address)

response = get_places4students_listings()
html = parse_listings(response)
parse_house(html)