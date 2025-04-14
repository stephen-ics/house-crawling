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
    price = parse_price(bsObj=bsObj)
    lease_type = parse_lease_types(bsObj=bsObj)
    print(lease_type)

def clean_text(uncleanedText, prefix):
    pattern = rf'{re.escape(prefix)}\s+(.+)'
    match = re.search(pattern, uncleanedText, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def parse_address(bsObj):    
    housingInformation = bsObj.find("div", class_="loaction-container")

    uncleanedStreet = housingInformation.find("span", id="MainContent_Label3").parent.get_text()
    uncleanedCity = housingInformation.find("div", id="MainContent_trCity").get_text()
    uncleanedProvince = housingInformation.find("div", id="MainContent_trProvince").get_text()
    uncleanedCountry = housingInformation.find("div", id="MainContent_trCountry").get_text()
    uncleanedPostalCode = housingInformation.find("div", id="MainContent_trZip").get_text()

    street = clean_text(uncleanedStreet, "Address:")
    city = clean_text(uncleanedCity, "City:")

    province = clean_text(uncleanedProvince, "State/Province:")
    if province == "Ontario":
        province = "ON"

    country = clean_text(uncleanedCountry, "Country:")
    postalCode = clean_text(uncleanedPostalCode, "Zip/Postal Code:")

    address = f"{street}, {city}, {province} {postalCode}, {country}"
    return address

def format_price(unformattedPrice):
    match = re.search(r'From:\s*\$([\d,]+\.\d{2})\s*to:\s*\$([\d,]+\.\d{2})', unformattedPrice)

    if match:
        price_from = match.group(1)
        price_to = match.group(2)

        if(price_from == price_to):
            price = price_from
        else:
            price = price_from + " - " + price_to

        return price

    return None

def parse_price(bsObj):
    uncleanedPrice = bsObj.find("div", id="MainContent_trRental").get_text()
    cleanedPrice = clean_text(uncleanedPrice, "Rental Rate:")
    price = format_price(cleanedPrice)

    return price

def parse_lease_types(bsObj):
    uncleanedLeaseType = bsObj.find("div", id="MainContent_trLeaseType").get_text()
    leaseType = clean_text(uncleanedLeaseType, "Lease Type(s) Offered:")
    
    return leaseType


response = get_places4students_listings()
html = parse_listings(response)
parse_house(html)

# 4 Month Sublet,Apartment/Condo