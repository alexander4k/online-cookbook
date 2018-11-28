def convert_items_in_list_to_lower(list_to_convert):
    new_list = []
    for item in list_to_convert:
        new_list.append(item.lower())
        
    return new_list
    
def convert_items_in_list_to_capitalized(list_to_convert):
    new_list = []
    for item in list_to_convert:
        new_list.append(item.capitalize())
        
    return new_list
    
def set_number_to_skip(number_to_display, page_number):
    skip = number_to_display * (page_number - 1)
    return skip
    
def set_prev_and_next_page_number(page_number, number_of_links):
    prev_page = page_number - 1
    if prev_page < 1:
        prev_page = 1
    next_page = page_number + 1
    if next_page > number_of_links:
        next_page = number_of_links
        
    return (prev_page, next_page)
        
    