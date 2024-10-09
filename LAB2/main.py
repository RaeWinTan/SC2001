

# for part c generate a very specific graph which definately my best case for push in array implementation will always hit
#so my fast path will be (1,2).....(k,k+1)...(999,1000)

#generate that weird graph 
from collections import defaultdict
from random import randint, shuffle

import xlsxwriter
import gc 
from math import log2,floor
from PQ import A,B,Solution

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

def writeRow(ws,row,type,obj:Solution,n,edge_count,theory_count):
    (_,tta) = obj.getDist(0,n-1)
    ws.write(row,0,type)
    ws.write(row,1,n)
    ws.write(row,2,edge_count)
    ws.write(row,3,obj.getSinks())
    ws.write(row,4,obj.getSwims())
    ws.write(row,5,tta)
    ws.write(row,6,theory_count)
    ws.write(row,7,obj.getTotal())#actual count, do not count initialization for edges
    
workbook = xlsxwriter.Workbook('dijkstra_analysis.xlsx', {'constant_memory':True})
#for quesiton a and b 
def qab(vstart,vend,vstep):
    global workbook    
    ws = workbook.add_worksheet("AVG_RAW_DATA")
    header = ["Type","Vertices", "Edges", "Sinks","Swims","Timetaken","Theory_complexity","Actual_complexity"]
    for i,e in enumerate(header): ws.write(0,i,e)
    row = 1
    for n in range(vstart,vend+1,vstep):
        #want 10 intervals
        diff = n*(n-2)//10
        edges = genAvgGraph(n)    
        for edge_count in range(n, aser(n-1)*2+1, diff):  
            tmp = edges[:edge_count]
            aObj = A(n,tmp)
            bObj = B(n,tmp)
            #theory count for a, V+E*N
            writeRow(ws,row,"A",aObj,n,edge_count,n+edge_count*n)
            row+=1
            #B is worst case go through all edges O(V+Elog(V))
            writeRow(ws,row,"B",bObj,n,edge_count,n+edge_count*int(log2(n)))
            row+=1

#for quesiton (c)
def qc(vstart,vend,vstep):
    ws = workbook.add_worksheet("HACKED_RAW_DATA")
    header = ["Type","Vertices", "Edges", "Sinks","Swims","Timetaken","Theory_complexity","Actual_complexity"]
    for i,e in enumerate(header): ws.write(0,i,e)
    row = 1
    for n in range(vstart,vend+1,vstep):
        edges = genWeirdGraph(n)
        aObj = A(n,edges)
        bObj = B(n,edges)
        writeRow(ws,row,"A",aObj,n,len(edges),n+len(edges)*n)
        row+=1
        writeRow(ws,row,"B",bObj,n,len(edges),n+len(edges)*log2(n))
        row+=1
        del aObj 
        del bObj
    gc.collect()

start,stop,step = 10 ,50 ,10
qab(start,stop,step)
qc(start,stop,step)
workbook.close()
