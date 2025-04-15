from bs4 import BeautifulSoup
from .parse_address import parse_address
from .parse_price import parse_price
from .parse_lease_types import parse_lease_types
from .parse_building_type import parse_building_types
from .parse_lease_start_date import parse_lease_start_date

def parse_house(houses):
    rows = []

    for html in houses:
        bsObj = BeautifulSoup(html, features="html.parser")

        address = parse_address(bsObj=bsObj)
        price = parse_price(bsObj=bsObj)
        lease_type = parse_lease_types(bsObj=bsObj)
        building_type = parse_building_types(bsObj=bsObj)
        lease_start_date = parse_lease_start_date(bsObj=bsObj)

        rows.append({
            'address': address,
            'price': price,
            'lease_type': lease_type,
            'building_type': building_type,
            'lease_start_date': lease_start_date
        })

    return rows
