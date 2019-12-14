

def filter_six_digits(number) -> bool:
    return len(str(number)) == 6

def filter_adjacent_numbers(number) -> bool:
    #regex to match cases where some alphanumeric char appears atleast twice in row:
    #   ((\d)\2{1,})
    #modified from answer https://stackoverflow.com/a/7147979
    import re
    return re.search(r'((\d)\2{1,})', str(number)) is not None

def filter_two_adjacent_numbers(number) -> bool:

    import re
    match = re.findall(r'((\d)\2{1,})', str(number))
    if match is not None:
        #some matches, return True if any of them has length of 2
        return any(filter(lambda g: len(g[0]) == 2, match) )
    else:
        #no matches
        return False

def filter_never_decrease(number) -> bool:
    num = str(number)
    match = True
    for i in range(1, len(num)):
        if num[i] < num[i-1]: match = False
    return match

def combine_filters(filters, numbers):
    valid_numbers = filter(lambda x: all(f(x) for f in filters), numbers)
    return list(valid_numbers)

"""
from https://stackoverflow.com/a/12386419
    filters = (f1,f2,f3,f4)
    filtered_list = filter( lambda x: all(f(x) for f in filters), your_list )
"""
if __name__ == "__main__":
    """ How many different passwords within the range given in your puzzle input meet these criteria? """

    #Part 1
    puzzle_input = range(278384, 824795)
    filters = (filter_six_digits, filter_adjacent_numbers, filter_never_decrease)
    valid_passwords = combine_filters(filters, puzzle_input)

    print(f'Space of possible passwords matching criteria contains {len(valid_passwords)} elements')

    #Part 2
    puzzle_input = range(278384, 824795)
    filters = (filter_six_digits, filter_two_adjacent_numbers, filter_never_decrease)
    valid_passwords = combine_filters(filters, puzzle_input)

    print(f'Space of possible passwords matching strict criteria contains {len(valid_passwords)} elements')