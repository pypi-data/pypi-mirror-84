def find_biggest(arr):
    biggest = arr[0] 
    biggest_index = 0

    for i in range(1, len(arr)):
        if arr[i] > biggest:
            biggest = arr[i]
            biggest_index = i

    return biggest_index

def selection_sort_to_low(arr):
    new_arr = []

    for i in range(len(arr)):
        biggest = find_biggest(arr)
        new_arr.append(arr.pop(biggest))

    return new_arr