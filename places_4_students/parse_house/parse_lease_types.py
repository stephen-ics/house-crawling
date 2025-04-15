from utils import clean_text

def parse_lease_types(bsObj):
    uncleanedLeaseType = bsObj.find("div", id="MainContent_trLeaseType").get_text()
    leaseType = clean_text(uncleanedLeaseType, "Lease Type(s) Offered:")
    
    return leaseType