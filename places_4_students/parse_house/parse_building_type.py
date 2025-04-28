from utils import clean_text, getHousingID

def parse_building_types(bsObj):
    uncleanedBuildingType = bsObj.find("span", id="MainContent_Label21")

    if uncleanedBuildingType == None:
        unformattedBuildingType = parse_building_type_check_condo(bsObj)
    else:
        unformattedBuildingType = clean_text(uncleanedBuildingType.parent.get_text(), "Type of Accommodation:")

    buildingType = format_building_type(unformattedBuildingType.lower())
    
    return buildingType

def parse_building_type_check_condo(bsObj):
    uncleanedBuildingType = bsObj.find("span", id="MainContent_rptApartment_lblRoomDes_0")

    if uncleanedBuildingType == None:
        uncleanedBuildingType = bsObj.find("span", id="MainContent_rptApartment_lblRoomDes_1")
    if uncleanedBuildingType == None:
        uncleanedBuildingType = bsObj.find("span", id="MainContent_rptApartment_lblRoomDes_2")

    return uncleanedBuildingType.get_text()

def format_building_type(unformattedBuildingType):
    if "apartment" in unformattedBuildingType and "condo" in unformattedBuildingType:
        return "Apartment/Condo"
    elif "apartment" in unformattedBuildingType:
        return "Apartment"
    elif "condo" in unformattedBuildingType:
        return "Condo"
    elif "townhouse" in unformattedBuildingType:
        return "Townhouse"
    elif "basement apartment" in unformattedBuildingType:
        return "Basement Apartment"
    elif "house" in unformattedBuildingType:
        return "House"
    else:
        return None