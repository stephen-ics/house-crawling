def parse_title(bsObj):
    title_element = bsObj.title

    if title_element == None:
        return None
    
    title = title_element.string
    
    return title