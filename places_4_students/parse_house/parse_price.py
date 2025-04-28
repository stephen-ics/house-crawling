import re
from utils import clean_text, getHousingID

def parse_price(bsObj):
    prices = parse_price_type_default(bsObj)

    if(prices == None):
        prices = parse_price_type_apartment(bsObj)

    minPrice = prices[0]
    maxPrice = prices[1]

    price = format_price(minPrice, maxPrice)

    return price

def parse_price_type_default(bsObj):
    uncleanedPrice = bsObj.find("div", id="MainContent_trRental")
    
    if uncleanedPrice == None:
        return None

    cleanedPrice = clean_text(uncleanedPrice, "Rental Rate:")

    match = re.search(r'From:\s*\$([\d,]+\.\d{2})\s*to:\s*\$([\d,]+\.\d{2})', cleanedPrice)

    if match:
        minPrice = match.group(1)
        maxPrice = match.group(2)
    else:
        price = extract_single_price(cleanedPrice)
        minPrice = price
        maxPrice = price

    return [minPrice, maxPrice]

def parse_price_type_apartment(bsObj):
    uncleanedMinPrice = bsObj.find("span", id="MainContent_rptApartment_Label4_0")
    if uncleanedMinPrice == None:
        uncleanedMinPrice = bsObj.find("span", id="MainContent_rptApartment_Label4_1")
    if uncleanedMinPrice == None:
        uncleanedMinPrice = bsObj.find("span", id="MainContent_rptApartment_Label4_2")

    uncleanedMaxPrice = bsObj.find("span", id="MainContent_rptApartment_Label8_0")
    if uncleanedMaxPrice == None:
        uncleanedMaxPrice = bsObj.find("span", id="MainContent_rptApartment_Label8_1")
    if uncleanedMaxPrice == None:
        uncleanedMaxPrice = bsObj.find("span", id="MainContent_rptApartment_Label8_2")

    minPrice = clean_text(uncleanedMinPrice.parent.get_text(), "Min Rent")
    maxPrice = clean_text(uncleanedMaxPrice.parent.get_text(), "Max Rent")

    return [minPrice, maxPrice]

def format_price(minPrice, maxPrice):
    if(minPrice == maxPrice):
        price = minPrice
    else:
        price = minPrice + " - " + maxPrice

    return price

def extract_single_price(text):
    prices = re.findall(r"\$([\d,]+\.\d{2})", text)

    if len(prices) == 1:
        return prices[0]
    
    return None