

# for part c generate a very specific graph which definately my best case for push in array implementation will always hit
#so my fast path will be (1,2).....(k,k+1)...(999,1000)

#generate that weird graph 
from collections import defaultdict
from random import randint, shuffle
from math import ceil 
import xlsxwriter
import gc 
from math import log2
import datetime 
from PQ import Solution
from Solution_Implementation import A,B

def aser(n):return (n*(n+1))//2
def genWeirdGraph(sz):
    edges = []
    ans = sz-1 
    acc = ans+1
    for a in range(sz-2, -1, -1):
        for b in range(sz):
            if a==b: continue
            elif b==a+1:
                edges.append((a,b,1))
                continue
            edges.append((a,b,acc+ans))
            acc+=1
        ans+=1
    hm = defaultdict(list)
    for (a,b,w) in edges:
        hm[a].append((b,w))
    rtn = []
    for k,v in sorted(hm.items()):
        nc = len(v)+1
        weights = sorted([w for (node,w) in v if node!=k+1], reverse=True)
        nodes = [node for node in range(nc) if node not in [k+1,k]]
        tmp = [(nodes[i],weights[i]) for i in range(len(weights))]+[(k+1, 1)]
        hm[k] = tmp 
        for b,w in tmp: rtn.append((k,b,w))
    mat = [[float("inf")]*sz for _ in range(sz)]
    for a,b,w in rtn:
        mat[a][b] = w 
    
    return rtn

def genAvgGraph(sz): 
    allEdges = []
    for a in range(sz):
        for b in range(sz):
            if a==b: continue 
            weight = randint(1,10**6)
            allEdges.append((a,b,weight))
    shuffle(allEdges)
    return allEdges

def writeRow(ws,row,type,obj:Solution,n,edge_count,theory_count,isBad):
    (_,tta) = obj.getDist(0,n-1) if not isBad else obj.getDist_bad(0,n-1)
    ws.write(row,0,type)
    ws.write(row,1,n)
    ws.write(row,2,edge_count)
    ws.write(row,3,obj.getSinks())
    ws.write(row,4,obj.getSwims())
    ws.write(row,5,tta)
    ws.write(row,6,theory_count)
    ws.write(row,7,obj.getTotal())#actual count, Only care about the dstra parts
    
workbook = xlsxwriter.Workbook('dijkstra_analysis.xlsx', {'constant_memory':True})
#for quesiton a and b 
def qab(vstart,vend,vstep):
    global workbook    
    ws = workbook.add_worksheet("AVG_RAW_DATA")
    header = ["Type","Vertices", "Edges", "Sinks","Swims","Timetaken","Theory_complexity","Actual_complexity"]
    for i,e in enumerate(header): ws.write(0,i,e)
    row = 1
    for n in range(vstart,vend+1,vstep):
        #want 5 intervals
        diff = n*(n-2)//5
        edges = genAvgGraph(n)    
        for edge_count in range(n, aser(n-1)*2+1, diff): 
            tmp = edges[:edge_count]
            timeStart = datetime.datetime.now()
            aObj = A(n,tmp)
            bObj = B(n,tmp)
            #theory count for a should be E*E but very hard to hit
            writeRow(ws,row,"A_GOOD",aObj,n,edge_count,edge_count*(edge_count-1)//2,False)#is it just edge**2
            row+=1
            writeRow(ws,row,"A_BAD",aObj,n,edge_count,edge_count*(edge_count-1)//2,True)
            row+=1
            #B is worst case go through all edges O(Elog(E)) # size of my pq could be |E|
            writeRow(ws,row,"B_GOOD",bObj,n,edge_count,edge_count*ceil(log2(edge_count)), False)
            row+=1
            writeRow(ws,row,"B_BAD",bObj,n,edge_count,edge_count*ceil(log2(edge_count)),True)
            row+=1
            del aObj 
            del bObj 
            gc.collect()
            timeEnd = datetime.datetime.now()
            print("QAB: "+str(n)+":"+str(edge_count)+ " timetaken:"+str((timeEnd-timeStart).total_seconds()*1000))

#for quesiton (c)
def qc(vstart,vend,vstep):
    ws = workbook.add_worksheet("HACKED_RAW_DATA")
    header = ["Type","Vertices", "Edges", "Sinks","Swims","Timetaken","Theory_complexity","Actual_complexity"]
    for i,e in enumerate(header): ws.write(0,i,e)
    row = 1
    for n in range(vstart,vend+1,vstep):
        timeStart = datetime.datetime.now()
        edges = genWeirdGraph(n)
        aObj = A(n,edges)
        bObj = B(n,edges)
        writeRow(ws,row,"A",aObj,n,len(edges),len(edges)*(len(edges)-1)//2,False)
        row+=1
        writeRow(ws,row,"B",bObj,n,len(edges),len(edges)*log2(len(edges)),False)
        row+=1
        del aObj 
        del bObj
        gc.collect()
        timeEnd = datetime.datetime.now()
        print("QC: "+str(n)+":"+str(len(edges))+ " timetaken:"+str((timeEnd-timeStart).total_seconds()*1000))

ss= genWeirdGraph(5)
aObj = A(5,ss)
for r in aObj.hm: print(r)
bObj = B(5,ss)
for r in bObj.hm:
    print(r)
"""
start,stop,step = 100 ,500 ,50
qab(start,stop,step)
qc(start,stop,step)
workbook.close()
"""