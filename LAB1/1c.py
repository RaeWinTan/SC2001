from random import randint
import datetime 
import xlsxwriter
from Sortable import HybridSort
import gc 
genArr = [-1]*(10*10**6)
def generateArray(sz,x):
    for i in range(sz):  genArr[i] = randint(1,x)
    



workbook = xlsxwriter.Workbook('threshold analysis.xlsx', {'constant_memory':True})
X = 10*10**6
from math import ceil, log2

def theory_func(sz,threshold): return sz*threshold + (sz)*ceil(log2(sz/threshold))

def diff_size_threshold(szstart,szend,szstep,tstart,tend):
    global workbook,genArr
    ws = workbook.add_worksheet("Raw Data")
    header = ["Threshold","Size","Theory key comparison", "Actual Key Comparison","Timetaken (milliseconds)"]
    for i,e in enumerate(header): ws.write(0,i,e)
    row =1 
    for sz in range(szstart,szend+1, szstep):
        generateArray(sz,X)
        arr = genArr
        print("Sz test: ",(sz-szstart)//szstep + 1)
        a = datetime.datetime.now()
        for threshold in range(tstart, tend+1):
            obj = HybridSort(arr[:sz],threshold)
            starttime = datetime.datetime.now()
            obj.sort()
            endtime = datetime.datetime.now()
            timetaken = (endtime-starttime).total_seconds()*1000 # in millieseonds
            ws.write(row,0,threshold)
            ws.write(row,1,sz)
            ws.write(row,2,theory_func(sz,threshold))
            ws.write(row,3,obj.getKeycmp())
            ws.write(row,4,timetaken)
            print("SIZE: ",sz,"Threshold: ",threshold," time taken:",timetaken)
            row+=1
            del obj #must be explicit with the deletion of objects 
            if threshold%15==0:gc.collect()
        b = datetime.datetime.now()
        print("Time taken for sz ",sz, (b-a).total_seconds()*1000)
diff_size_threshold(10**3,10*10**6,9999*10**2,1,20)
workbook.close()