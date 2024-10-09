from abc import ABC, abstractmethod
import datetime 

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
    def getSinks(self): return 0
    @abstractmethod
    def getSwims(self): return 0
    @abstractmethod
    def getTotal(self): return 0#this includes all iterations
    
class A(Solution):#assume it is a simple directed graph
    def __init__(self,n,edges):
        self.n = n 
        self.hm = [[float("inf")]*n for _ in range(n)]
        for a,b,w in edges:
            self.hm[a][b] = w
        self.sink_count = 0
        self.swim_count = 0
        self.loop_count = 0   
    def getDist(self,a,b):
        self.sink_count = 0
        self.swim_count = 0
        self.loop_count = 0
        starttime = datetime.datetime.now()
        dp = [float("inf")]*self.n
        dp[a] = 0
        pq = ArrayPQ()
        self.swim_count+=pq.put((0,a)) 
        while pq.size():
            ((dist,node), skct) = pq.pop()
            self.sink_count+=skct
            if node==b: break 
            for adj in range(self.n):
                self.loop_count+=1
                if dist+self.hm[node][adj]>=dp[adj]:continue
                dp[adj] = dist+self.hm[node][adj]
                self.swim_count+=pq.put((dp[adj], adj))
        rtn = dp[b]
        endtime = datetime.datetime.now()
        del dp
        del pq
        return (rtn, (endtime-starttime).total_seconds()*1000)
    def getSinks(self):
        return self.sink_count
    def getSwims(self):
        return self.swim_count 
    def getTotal(self):
        return self.loop_count+self.swim_count+self.sink_count+self.n
    def __del__(self):
        for r in self.hm: del r 
        del self.hm

class B(Solution):#assume it is a simple directed graph
    def __init__(self,n,edges):
        self.n = n 
        self.hm = [[] for _ in range(n)]
        for a,b,w in edges:
            self.hm[a].append((b,w))
        self.sink_count = 0 
        self.swim_count = 0 
    
    def getDist(self,a,b):
        self.sink_count = 0 
        self.swim_count = 0 
        self.loop_count = 0
        starttime = datetime.datetime.now()
        dp = [float("inf")]*self.n
        dp[a] = 0
        pq = HeapPQ()
        self.swim_count+=pq.put((0,a))
        while pq.size():
            ((dist,node), skct) = pq.pop()
            self.sink_count+=skct
            if node==b: break 
            for (adj,w) in self.hm[node]:
                self.loop_count+=1
                if dist+w>=dp[adj]:continue
                dp[adj] = dist+w
                self.swim_count+=pq.put((dp[adj], adj))
        rtn = dp[b]
        endtime = datetime.datetime.now()
        del dp 
        del pq
        return (rtn, (endtime-starttime).total_seconds()*1000)
    def getTotal(self):
        return self.swim_count+self.sink_count+self.loop_count+self.n
    def getSwims(self):
        return self.swim_count
    def getSinks(self):
        return self.sink_count
    def __del__(self):
        for r in self.hm:del r 
        del self.hm 





