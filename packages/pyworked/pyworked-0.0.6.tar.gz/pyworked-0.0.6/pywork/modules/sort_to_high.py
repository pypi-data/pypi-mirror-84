class Sth:

    def __init__(self, arr):
        self.arr = arr

    def find(self, arr):
        smallest = arr[0]
        smallest_index = 0

        for i in range(1, len(arr)):
            if arr[i] < smallest:
                smallest = arr[i]
                smallest_index = i
    
        return smallest_index

    def sort(self):
        new_arr = []

        for i in range(len(self.arr)):
            smallest = self.find(self.arr)
            new_arr.append(self.arr.pop(smallest))
    
        return new_arr