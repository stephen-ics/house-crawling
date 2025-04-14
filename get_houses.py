import requests

def call_bamboo_api(params):
    url = "https://bamboohousing.ca/api/alllistings"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(url, params=params, headers=headers)
    return response


def get_bamboo_houses():
    params = {
        "page": 1,
        "size": 10000,
        "Coed": "",
        "RoomsAvailable": "",
        "UwaterlooDist": "undefined",
        "Price": "",
        "StartTerm": "",
        "LeaseType": "",
        "Sort": "Recent",
        "CityName": "Waterloo"
    }

    response = call_bamboo_api(params=params)
    return response