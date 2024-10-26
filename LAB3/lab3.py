"""

P(C,i) #C: capacity, #i: index of the object  
P(C,i) = 
    if i==len(profits): return 0
    if C<weights[i]:
        return P(C,i+1)
    else:
        #take the maximum between taking the current object and not taking the current object 
        return max(profits[i] + P(C-weights[i], i+1), P(C,i+1))
        
"""
from functools import cache
#top down approach
def solution_topDown(C, weights, profits):
    @cache
    def P(C, i):
        if i==len(profits): return 0 
        if C < weights[i]: return P(C,i+1)
        return max(profits[i] + P(C-weights[i], i+1), P(C,i+1))
    return P(C,0)

#time complexity : O(C*N), Space Complexity O(C*N)
def solution_bottom_up(C,weights,profits):
    dp = [[0]*(len(weights) + 1) for _ in range(C+1)]
    for i in range(len(weights)-1, -1, -1):
        for c in range(C+1):
            if c<weights[i]: dp[c][i] = dp[c][i+1]
            else: dp[c][i] = max(profits[i] + dp[c-weights[i]][i+1], dp[c][i+1])
    return dp[C][0] 

#time complexity : O(C*N), Space Complexity O(C)
def solution_bottom_up_space_efficient(C,weights,profits):
    dp = [0]*(C+1)#O(C)
    for i in range(len(weights)-1, -1, -1):
        nxt = []
        for c in range(C+1):
            if c<weights[i]: nxt.append(dp[c])
            else:  nxt.append(max(profits[i] + dp[c-weights[i]], dp[c]))
        dp = nxt 
    return dp[C]

def online_solution(C,weights, profits):
    #https://khambud.medium.com/maximum-profit-dp-238c4fc4c2c
    W=C
    n = len(weights)
    dp = [[-1 for _ in range(W+1)] for _ in range(n+1)]
    for i in range(n+1):
        for w in range(W+1):
            if i == 0 or w == 0:
                dp[i][w] = 0
            elif weights[i-1] <= w:
                # compute maximum profit by either including the weight[i-1] or not
                dp[i][w] = max(profits[i-1] + dp[i-1][w-weights[i-1]],\
                            dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][W]



from random import randint
import xlsxwriter
workbook = xlsxwriter.Workbook('test_data.xlsx', {'constant_memory':True})
ws = workbook.add_worksheet("RESULTS")
header=  ["weights", "profits", "Capacity", "topDown","bottom up", "bottom up (space efficient)", "Online solution", "isSame"]
for i,e in enumerate(header): ws.write(0,i,e)
row = 1 
for sz in range(10, 101, 10): 
    weights = [randint(30, 350) for _ in range(sz)]
    profits = [randint(20,1000) for _ in range(sz)]
    for C in [randint(30, 100), randint(100,200), randint(500, 1000)]:
        a = solution_topDown(C,weights, profits)
        b = solution_bottom_up_space_efficient(C,weights,profits)
        c = solution_bottom_up_space_efficient(C,weights,profits)
        d = online_solution(C,weights, profits)
        ws.write(row, 0, ",".join(list(map(str,weights))) )
        ws.write(row, 1, ",".join(list(map(str,profits))) )
        ws.write(row, 2, str(C))
        ws.write(row, 3, str(a))
        ws.write(row, 4, str(b))
        ws.write(row, 5, str(c))
        ws.write(row, 6, str(d))
        ws.write(row,7, str(len(set([a,b,c,d]))==1) )
        row+=1

workbook.close()