from bs4 import BeautifulSoup

def parse_address(bsObj):
    address_text_element = bsObj.find("h2", class_="location_build_up")

    if not address_text_element:
        return None

    address = address_text_element.text

    return address


