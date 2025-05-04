from dateutil import parser

def parse_lease_start_date(bsObj):
    title_text_element = bsObj.find("h1", class_="title_text")

    if not title_text_element:
        return None

    title_text = title_text_element.text
    lease_start_date_unformatted = title_text.split("-")[0].strip(" ")
    lease_start_date = format_date(lease_start_date_unformatted)

    return lease_start_date

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