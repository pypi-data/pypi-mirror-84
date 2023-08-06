class Stl:

    def __init__(self, arr):
        self.arr = arr

    def find(self, arr):
        biggest = arr[0] 
        biggest_index = 0

        for i in range(1, len(arr)):
            if arr[i] > biggest:
                biggest = arr[i]
                biggest_index = i

        return biggest_index

    def sort(self):
        new_arr = []

        for i in range(len(self.arr)):
            biggest = self.find(self.arr)
            new_arr.append(self.arr.pop(biggest))

        return new_arr