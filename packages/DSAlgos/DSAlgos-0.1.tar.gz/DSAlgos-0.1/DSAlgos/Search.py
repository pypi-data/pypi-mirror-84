class Searching:
        
    def LinearSearch(self, list, value):
        self.list1 = list
        self.value = value
        if len(self.list1) == 0:
            return False
        else:
            for i in range(0, len(self.list1)):
                if self.list1[i] == self.value:
                    return True
            return False
    
    def BinarySearch(self, list, value):
        self.list1 = list
        self.value = value
        if len(self.list1) == 0:
            return False
        else:
            mid = len(self.list1)//2
        if mid == self.value:
            return True
        else:
            if self.value < self.list1[mid]:
                return BinarySearch(self.list1[:mid], value)
            else:
                return BinarySearch(self.list1[mid+1:], value)
