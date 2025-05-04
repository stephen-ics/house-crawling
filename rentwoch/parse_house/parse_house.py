from bs4 import BeautifulSoup
from .parse_title import parse_title
from .parse_lease_start_date import parse_lease_start_date
from .parse_price import parse_price
from .parse_address import parse_address

def parse_house(html):
    rows = []

    bsObj = BeautifulSoup(html, "html.parser")
    
    housingDetails = bsObj.find("div", class_="details")

    title = parse_title(bsObj)
    price = parse_price(housingDetails)
    address = parse_address(housingDetails)
    lease_start_date = parse_lease_start_date(housingDetails)

    rows.append({
        'title': title,
        'address': address,
        'price': price,
        'lease_start_date': lease_start_date
    })

    print(rows)

