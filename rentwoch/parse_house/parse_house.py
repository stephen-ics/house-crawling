from bs4 import BeautifulSoup
from .parse_lease_start_date import parse_lease_start_date

def parse_house(html):
    bsObj = BeautifulSoup(html, "html.parser")
    
    housingDetails = bsObj.find("div", class_="details")
    
    lease_start_date = parse_lease_start_date(housingDetails)