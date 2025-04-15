import re 

def getHousingID(bsObj):
    houseIDElement = bsObj.find("a", id="MainContent_lnkIAgree")
    match = re.search(r'HousingID=(.+?)(?:%26|$)', houseIDElement["href"])

    if match == None:
        return None
    
    return match.group(1)

def clean_text(uncleanedText, prefix):
    raw = uncleanedText

    if hasattr(uncleanedText, 'get_text'):
        raw = uncleanedText.get_text()
    else:
        raw = uncleanedText or ''

    text = raw.replace('\xa0', ' ').strip()

    if prefix in text:
        pattern = rf'{re.escape(prefix)}:?\s*(.+)'
        m = re.search(pattern, text, re.DOTALL)
        if m:
            val = m.group(1).strip()
            return val or None

    if prefix.lower().endswith('rent'):
        m = re.search(r'([\$\d,]+\.\d{2})', text)
        return m.group(1) if m else None

    return text