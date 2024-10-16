from abc import ABC, abstractmethod

#default to a minimizing PQ, (weight, vector name)
class PriorityQueue(ABC):#it should be returning back a tuple 
    @abstractmethod
    def put(self,x): return 0 #return:swim counts
    @abstractmethod
    def size(self): return 0
    @abstractmethod
    def pop(self): return ((0,0),0) #return:lightest_object + sink counts

class ArrayPQ(PriorityQueue):
    def __init__(self):
        self.arr = []
    def put(self, x):
        ops = 0
        self.arr.append(x)
        for i in range(len(self.arr)-1, 0,-1):#insert sort sink function
            if self.arr[i] > self.arr[i-1]:
                ops+=1
                self.arr[i],self.arr[i-1] = self.arr[i-1],self.arr[i]
            else:
                break 
        return ops
    def size(self): 
        return len(self.arr)
    def pop(self):
        return (self.arr.pop(), 0)
    def __del__(self):
        del self.arr

class HeapPQ(PriorityQueue):
    def __init__(self): 
        self.arr = [(0,0)]
        self.sz = 0 
        
    def put(self, x):#performing swim up operation from added leaf
        ops = 0
        self.arr.append(x)
        self.sz+=1
        H = self.sz 
        while True:
            parent = H//2
            if parent==0: break 
            if self.arr[parent]>self.arr[H]:
                ops+=1
                self.arr[parent],self.arr[H] = self.arr[H],self.arr[parent]
            else: break 
            H = parent
        return ops
    def size(self): 
        return self.sz
    def pop(self):
        ops = 0
        def sink(H,k):#performing sink down opereation from root
            nonlocal ops
            while True:
                left = self.arr[H*2] if H*2<=self.sz else (float("inf"), float("inf"))
                right = self.arr[H*2+1] if H*2+1<=self.sz else (float("inf"), float("inf"))
                if k<=left and k <=right: return
                ops+=1
                if left>=right:
                    self.arr[H*2+1],self.arr[H] =  self.arr[H],self.arr[H*2+1]
                    H = H*2+1
                else:
                    self.arr[H*2],self.arr[H] =  self.arr[H],self.arr[H*2]
                    H = H*2
        rtn = self.arr[1]
        self.sz-=1
        k = self.arr.pop()
        if self.sz==0: return (rtn, ops) 
        self.arr[1] = k 
        sink(1, k)
        return (rtn, ops)
    def __del__(self):
        del self.arr

class Solution(ABC):
    @abstractmethod
    def getDist(self,a,b): return (0,0)#dist and time 
    @abstractmethod 
    def getDist_bad(self, a,b): return (0,0)
    @abstractmethod
    def getSinks(self): return 0
    @abstractmethod
    def getSwims(self): return 0
    @abstractmethod
    def getTotal(self): return 0#this includes all iterations
    






