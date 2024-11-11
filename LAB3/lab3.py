from functools import cache
def solution_topDown(C,weights,profits):
    n = len(weights)
    @cache
    def r(C):
        nonlocal n
        if C<=0: return 0 
        rtn = 0 
        for i in range(n):
            if(C-weights[i]>=0):rtn = max(rtn, r(C-weights[i])+profits[i])
        return rtn 
    return r(C)
#time complexity, O(N*C) space complexity O(C)
def solution_bottom_up(C,weights, profits):
    n = len(weights)
    dp = [0]*(C+1)
    hint = [-1]*(C+1) 
    for c in range(C+1):
        for i in range(n):
            if c-weights[i]>=0:
                if dp[c] < dp[c-weights[i]]+profits[i]:
                    hint[c] = i 
                dp[c] = max(dp[c], dp[c-weights[i]]+profits[i])
    takes = [0]*n 
    c = C 
    while hint[c]!=-1:
        takes[hint[c]]+=1 
        c-=weights[hint[c]]       
    rtn = [(i,takes[i]) for i in range(n) if takes[i]>0] 
    return ( dp[C], rtn, sum([profits[i]*e for i,e in rtn]) )
#4a
weights = [4,6,8]
profits = [7,6,9]
C= 14
print("WEIGHTS:",weights,", PROFITS:",profits,", C:",C)
sol = solution_bottom_up(C,weights, profits)
print("4(a) top down ", solution_topDown(C, weights, profits))
print("4(a) Bottom up", sol[0])
print(sol[1])
print("---------------")
#4b 
weights = [5,6,8]
profits = [7,6,9]
C= 14
sol = solution_bottom_up(C,weights, profits)
print("WEIGHTS:",weights,", PROFITS:",profits,", C:",C)
print("4(b) top down ", solution_topDown(C, weights, profits))
print("4(b) Bottom up", sol[0])
print(sol[1])


from random import randint
import xlsxwriter
workbook = xlsxwriter.Workbook('test_data.xlsx', {'constant_memory':True})
ws = workbook.add_worksheet("RESULTS")
header=  ["weights", "profits", "Capacity", "topDown","bottom up","Bottom up takes", "isSame","Takes"]
for i,e in enumerate(header): ws.write(0,i,e)
row = 1 
for sz in range(1, 10): 
    weights = [randint(10,20) for _ in range(sz)]
    profits = [randint(30,50) for _ in range(sz)]
    for C in [randint(20,30), randint(31,40), randint(41,50)]:
        a = solution_topDown(C,weights, profits)
        b,takes,b1t = solution_bottom_up(C,weights,profits)
        ws.write(row, 0, ",".join(list(map(str,weights))) )
        ws.write(row, 1, ",".join(list(map(str,profits))) )
        ws.write(row, 2, str(C))
        ws.write(row, 3, str(a))
        ws.write(row, 4, str(b))
        ws.write(row, 5, str(b1t))
        ws.write(row,6, str(len(set([a,b,b1t]))==1) )
        ws.write(row, 7, ",".join(map(str,takes)))
        row+=1

workbook.close()
