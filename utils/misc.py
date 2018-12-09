
def convert_items_in_list_to_lower(list_to_convert):
    """ 
    Creates a new list of strings lowercased
    """
    new_list = []
    for item in list_to_convert:
        new_list.append(item.lower())
        
    return new_list
    
def convert_items_in_list_to_capitalized(list_to_convert):
    """ 
    Creates a new list of strings capitalized
    """
    new_list = []
    for item in list_to_convert:
        new_list.append(item.capitalize())
        
    return new_list
    
def set_number_to_skip(number_to_display, page_number):
    """ 
    Used for pagination, takes in the number of items 
    to be displayed on a page and the current page number
    and calculates the amount of items to skip each page.
    E.g if number of items is equal to 9, skips 0 on the first
    page, 9 on the second, 18 on the third etc.
    """
    skip = number_to_display * (page_number - 1)
    return skip

def calculate_number_of_pagination_links(limit, number_of_items):
    """ 
    Used for pagination, takes in the total number of items and
    the limit of how many are meant to appear on a page. 
    Calculates how many links will appear on the page. If the total 
    divided by the limit does not equal 0 then its rounded up.
    """
    number_of_links = int(number_of_items / limit) + (number_of_items % limit > 0)
    
    return number_of_links
    
def set_prev_and_next_page_number(page_number, number_of_links):
    """ 
    Used for pagination, takes in the current page number and
    the total number of pagination links. Sets the previous and
    next page number so that the previous can never point to a page 
    number less than 1 and next can never go past the last page.
    """
    prev_page = page_number - 1
    if prev_page < 1:
        prev_page = 1
    next_page = page_number + 1
    if next_page > number_of_links:
        next_page = number_of_links
        
    return (prev_page, next_page)
    

        
    