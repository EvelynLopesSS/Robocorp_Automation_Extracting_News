import re

def contains_money(text):
    pattern = r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s?(?:dollars|USD)'

    match = re.search(pattern, text, re.IGNORECASE)
    
    return bool(match)


