import requests
from bs4 import BeautifulSoup
import re

from utils import getHousingID
from parse_house import parse_house
from format_data import write_houses_csv

LISTINGS_URL = "https://www.places4students.com/Places/PropertyListings"
SCHOOL_ID = "VBThwOQPAX4="
COOKIES = {
    "ASP.NET_SessionId":        "qmxwdtlxlffde1t3e4s0bff5",
    "Places4StudentDisclaimer": "Agree",
    "__AntiXsrfToken":          "e24d51e2de26447ca1d222b78e0085b2"
}
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_places4students_listings(page=1):
    session = requests.Session()
    session.headers.update(HEADERS)
    session.cookies.update(COOKIES)

    if page == 1:
        resp = session.get(LISTINGS_URL, params={"SchoolID": SCHOOL_ID})
    else:
        init = session.get(LISTINGS_URL, params={"SchoolID": SCHOOL_ID})
        init.raise_for_status()
        soup = BeautifulSoup(init.text, "html.parser")
        form = soup.find("form", id="form1") or soup.find("form")

        payload = {
            inp["name"]: inp.get("value", "")
            for inp in form.find_all("input", type="hidden")
            if inp.get("name")
        }

        payload.update({
            "__EVENTTARGET":   "ctl00$MainContent$gvListingDirectory",
            "__EVENTARGUMENT": f"Page${page}",
            "__LASTFOCUS":     ""
        })

        resp = session.post(
            LISTINGS_URL,
            params={"SchoolID": SCHOOL_ID},
            data=payload
        )

    resp.raise_for_status()
    return resp.text


def parse_listings(html):
    bsObj = BeautifulSoup(html, "html.parser")
    table = bsObj.find("table", class_="StdTable")

    if table == None:
        return None
        
    houses = []

    tds = table.find_all("td", class_="listing-occupancy-date")

    for td in tds:
        link = td.find("a", href=True)

        if not link:
            continue

        match = re.search(r'HousingID=([^&]+)', link["href"])

        if not match:
            continue

        houseID = match.group(1)

        response = get_places4students_house(houseID)
        houses.append(response.text)

    return houses

def call_places4students_house_api(params, cookies):
    url = "https://www.places4students.com/Places/Details"
    return requests.get(url, params=params, cookies=cookies, headers=HEADERS)


def get_places4students_house(housingID):
    params = {"SchoolID": SCHOOL_ID, "HousingID": housingID}
    return call_places4students_house_api(params, COOKIES)


if __name__ == "__main__":
    all_houses = []

    for p in range(1, 6):
        html = get_places4students_listings(page=p)
        all_houses.extend(parse_listings(html))

    data_rows = parse_house(all_houses)
    write_houses_csv(data_rows, "places4students.csv")