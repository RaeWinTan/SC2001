import datetime 
from PQ import Solution, ArrayPQ,HeapPQ

class A(Solution):#assume it is a simple directed graph
    def __init__(self,n,edges):
        self.n = n 
        self.hm = [[float("inf")]*n for _ in range(n)]
        for a,b,w in edges:
            self.hm[a][b] = w
        self.sink_count = 0
        self.swim_count = 0 
    def getDist(self,a,b):
        self.sink_count = 0
        self.swim_count = 0
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
                if dist+self.hm[node][adj]>=dp[adj]:continue
                dp[adj] = dist+self.hm[node][adj]
                self.swim_count+=pq.put((dp[adj], adj))
        rtn = dp[b]
        endtime = datetime.datetime.now()
        del dp
        del pq
        return (rtn, (endtime-starttime).total_seconds()*1000)
    def getDist_bad(self,a,b):
        self.sink_count = 0
        self.swim_count = 0
        starttime = datetime.datetime.now()
        dp = [float("inf")]*self.n
        dp[a] = 0
        seenEdges = [[True]*self.n for _ in range(self.n)]
        #also say false for those actual edges
        for i in range(self.n):
            for j in range(self.n):
                if self.hm[i][j]!=float("inf"):
                    seenEdges[i][j] = False

        pq = ArrayPQ()
        self.swim_count+=pq.put((0,a))
        while pq.size():
            ((dist,node), skct) = pq.pop()
            self.sink_count+=skct
            for adj in range(self.n):
                if seenEdges[node][adj]: continue 
                seenEdges[node][adj] = True
                dp[adj] = min(dist+self.hm[node][adj], dp[adj])
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
        return self.swim_count+self.sink_count
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
                if dist+w>=dp[adj]:continue #prunes out unnessary computations
                dp[adj] = dist+w
                self.swim_count+=pq.put((dp[adj], adj))
        rtn = dp[b]
        endtime = datetime.datetime.now()
        del dp 
        del pq
        return (rtn, (endtime-starttime).total_seconds()*1000)
    
    def getDist_bad(self,a,b):
        self.sink_count = 0 
        self.swim_count = 0 
        starttime = datetime.datetime.now()
        dp = [float("inf")]*self.n
        dp[a] = 0
        pq = HeapPQ()
        self.swim_count+=pq.put((0,a))
        seenEdges = [[False]*self.n for _ in range(self.n)]
        while pq.size():
            ((dist,node), skct) = pq.pop()
            self.sink_count+=skct
            for (adj,w) in self.hm[node]:
                if seenEdges[node][adj]:continue
                seenEdges[node][adj] = True
                dp[adj] = min(dist+w, dp[adj])
                self.swim_count+=pq.put((dp[adj], adj))
        rtn = dp[b]
        endtime = datetime.datetime.now()
        del dp 
        del pq
        return (rtn, (endtime-starttime).total_seconds()*1000)
    
    def getTotal(self):
        return self.swim_count+self.sink_count
    def getSwims(self):
        return self.swim_count
    def getSinks(self):
        return self.sink_count
    def __del__(self):
        for r in self.hm:del r 
        del self.hm 