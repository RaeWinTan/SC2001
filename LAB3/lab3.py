from functools import cache
#top down approach
def solution_topDown(C, weights, profits):
    @cache
    def P(C, i):
        if i==len(profits): return 0 
        maxTake = C//weights[i]
        rtn=0
        for take in range(maxTake+1):
            rtn = max(rtn, P(C-weights[i]*take,i+1) + profits[i]*take)
        return rtn         
    return P(C,0)

#time complexity : O(C*N*(C//min(weights))), Space Complexity O(C*N), with the hint
def solution_bottom_up(C,weights,profits):
    n = len(weights)
    dp = [[0 for _ in range(C+1)] for _ in range(n+1)] 
    hint = [[0 for _ in range(C+1)] for _ in range(n+1)]
    for i in range(n-1, -1,-1):
        for c in range(C+1):
            maxTake = c//weights[i]
            for take in range(maxTake+1):
                if c-take*weights[i]>=0:#will diffiniately run at least once per c cuz take 0 is included
                    if dp[i][c] < dp[i+1][c-take*weights[i]] + profits[i]*take:
                        hint[i][c] = take 
                    dp[i][c] = max(dp[i][c], dp[i+1][c-take*weights[i]] + profits[i]*take)
    rtn = [] 
    c = C
    for i in range(n):
        if hint[i][c]>0:
            rtn.append((i,hint[i][c]))
        c-=weights[i]*hint[i][c]
    return (dp[0][C], rtn, sum(profits[i]*c for i,c in rtn))

#time complexity : O(C*N*(C//min(weights))), Space Complexity O(C)
def solution_bottom_up_space_optimised(C,weights,profits):
    n = len(weights)
    prev = [0 for _ in range(C+1)] 
    for i in range(n-1, -1,-1):
        curr = []
        for c in range(C+1):
            maxTake = c//weights[i]
            curr.append(0)
            for take in range(maxTake+1):
                if c-take*weights[i]>=0:
                    curr[-1] = max(curr[-1], prev[c-take*weights[i]] + profits[i]*take)  
        prev = curr
    return prev[C]

#4a
weights = [4,6,8]
profits = [7,6,9]
C= 14
print("WEIGHTS:",weights,", PROFITS:",profits,", C:",C)
sol = solution_bottom_up(C,weights, profits)
print("4(a) top down ", solution_topDown(C, weights, profits))
print("4(a) Bottom up", sol[0])
print("4 (a) Bottom up space efficient", solution_bottom_up_space_optimised(C,weights,profits))
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
print("4 (b) Bottom up space efficient", solution_bottom_up_space_optimised(C,weights,profits))
print(sol[1])

"""
from random import randint
import xlsxwriter
workbook = xlsxwriter.Workbook('test_data.xlsx', {'constant_memory':True})
ws = workbook.add_worksheet("RESULTS")
header=  ["weights", "profits", "Capacity", "topDown","bottom up","Bottom up takes", "bottom up (space efficient)", "isSame","Takes"]
for i,e in enumerate(header): ws.write(0,i,e)
row = 1 
for sz in range(1, 10): 
    weights = [randint(10,20) for _ in range(sz)]
    profits = [randint(30,50) for _ in range(sz)]
    for C in [randint(20,30), randint(31,40), randint(41,50)]:
        a = solution_topDown(C,weights, profits)
        b,takes,b1t = solution_bottom_up(C,weights,profits)
        c = solution_bottom_up_space_optimised(C,weights,profits)
        ws.write(row, 0, ",".join(list(map(str,weights))) )
        ws.write(row, 1, ",".join(list(map(str,profits))) )
        ws.write(row, 2, str(C))
        ws.write(row, 3, str(a))
        ws.write(row, 4, str(b))
        ws.write(row, 5, str(b1t))
        ws.write(row, 6, str(c))
        ws.write(row,7, str(len(set([a,b,c,b1t]))==1) )
        ws.write(row, 8, ",".join(map(str,takes)))
        row+=1

workbook.close()
"""