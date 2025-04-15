from utils import clean_text

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