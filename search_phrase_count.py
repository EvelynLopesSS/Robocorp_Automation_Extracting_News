def count_search_phrase(search_phrase:str, title, description):
    title_count = title.lower().count(search_phrase.lower())
    description_count = description.lower().count(search_phrase.lower())
    return title_count + description_count