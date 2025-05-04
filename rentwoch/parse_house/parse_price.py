import re

def parse_price(bsObj):
    price_text_element = bsObj.find("div", class_="price_box")

    if not price_text_element:
        return None

    price_text = price_text_element.text
    price = format_price(price_text)

    return price

def format_price(price_str):
    price_str_match = re.search(r"\$(\d+)", price_str)

    if price_str_match == None:
        return None

    price = price_str_match.group(1)

    return price