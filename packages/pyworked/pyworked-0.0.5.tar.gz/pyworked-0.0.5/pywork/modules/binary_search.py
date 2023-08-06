from pywork.modules import sort_to_high as sth

def binary_search(list, item):
    low = 0
    high = len(list) - 1
    list = sth.selection_sort_to_high(list)

    while low <= high:
        mid = (low + high)
        guess = list[mid]

        if guess == item:
            return mid
        if guess > item:
            high = mid - 1
        else:
            low = mid + 1 

    return None