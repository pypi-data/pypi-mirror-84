from pywork.modules.sort_to_high import Sth

class Bs:

    def __init__ (self, arr, item):
        self.arr = arr
        self.item = item

    def search(self):
        low = 0
        high = len(self.arr) - 1
        list = Sth(self.arr).sort()

        while low <= high:
            mid = (low + high)
            guess = list[mid]

            if guess == self.item:
                return mid
            if guess > self.item:
                high = mid - 1
            else:
                low = mid + 1 

        return None