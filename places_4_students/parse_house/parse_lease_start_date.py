from utils import clean_text

from dateutil import parser
from datetime import date

def parse_lease_start_date(bsObj):
    uncleanedLeaseStartDate = parse_lease_start_date_default(bsObj)

    if uncleanedLeaseStartDate == None:
        uncleanedLeaseStartDate = parse_lease_start_date_apartment(bsObj)

    unformattedLeaseStartDate = clean_text(uncleanedLeaseStartDate, "Occupancy Date")

    leaseStartDate = format_date(unformattedLeaseStartDate)

    return leaseStartDate
    
def parse_lease_start_date_default(bsObj):
    uncleanedLeaseStartDate = bsObj.find("span", id="MainContent_Label25")

    if uncleanedLeaseStartDate == None:
        return None
    
    return uncleanedLeaseStartDate.parent.get_text()

def parse_lease_start_date_apartment(bsObj):
    uncleanedLeaseStartDate = bsObj.find("span", id="MainContent_rptApartment_Label24_1")

    if uncleanedLeaseStartDate == None:
        uncleanedLeaseStartDate = bsObj.find("span", id="MainContent_rptApartment_Label24_0")

    if uncleanedLeaseStartDate == None:
        return None
    
    return uncleanedLeaseStartDate.parent.get_text()

def format_date(date_str):
    try:
        if date_str.lower() == "immediately":
            return "Immediately"
        elif "contact" in date_str.lower():
            return "Contact for more details"

        parsed_date = parser.parse(date_str)
        return parsed_date.date()
    except (ValueError, TypeError):
        return None