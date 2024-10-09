from abc import ABC, abstractmethod
class Sortable(ABC):
    @abstractmethod
    def getKeycmp(self):
        return 0 
    
    @abstractmethod
    def sort(self):
        return []
    

class MergeSort(Sortable):
    
    def __init__(self,arr):
        self.__arr = arr.copy()
        self.__keycmp = 0 
        self.obj = HybridSort(self.__arr,1)
    
    def sort(self):
        rtn = self.obj
        self.__arr = rtn.sort()
        self.__keycmp = rtn.getKeycmp()   
        return self.__arr
    
    def getKeycmp(self): 
        return self.__keycmp

#done inplace to prevent time taken for array copy operation
class InsertSort(Sortable):
    def __init__(self,arr):
        self.__arr = arr 
        self.__keycmp = 0 
    
    def sort(self):
        n = len(self.__arr)
        for i in range(1, n):
            for j in range(i, 0,-1):
                if self.__arr[j]< self.__arr[j-1]:
                    self.__keycmp+=1
                    self.__arr[j-1],self.__arr[j] = self.__arr[j],self.__arr[j-1]
                else: break 
        return self.__arr

    def getKeycmp(self): 
        return self.__keycmp

class HybridSort(Sortable):
    def __init__(self, arr, threshold):
        if threshold<1: raise Exception("Threshold cannot be below 1")
        self.__threshold = threshold
        self.__arr = arr.copy()
        self.__keycmp = 0
    #override method
    def sort(self):
        def hysort(arr):
            if len(arr)<=self.__threshold: 
                rtn = InsertSort(arr)
                rtnarr = rtn.sort()
                self.__keycmp+=rtn.getKeycmp()
                return rtnarr 
            l = 0 
            r = len(arr)-1
            mid = l+(r-l)//2
            left = hysort(arr[:mid+1])
            right = hysort(arr[mid+1:])
            return self.merge(left, right)
        self.__arr = hysort(self.__arr)
        return self.__arr
    def merge(self, l,r):
        rtn = []
        i = 0 
        j = 0 
        while i < len(l) and j < len(r):
            self.__keycmp+=1 
            if l[i]<=r[j]:
                rtn.append(l[i])
                i+=1 
            else:
                rtn.append(r[j])
                j+=1 
        #this part not need to do key compare anymore 
        if i < len(l): rtn.extend(l[i:])
        else:rtn.extend(r[j:]) #this still have to process keys in right array 
        return rtn 
    def getKeycmp(self):
        return self.__keycmp
    def __del__(self): #for garbage collection
        del self.__arr

