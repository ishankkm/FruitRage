'''
Created on Oct 15, 2017

@author: ishank
'''

from __future__ import print_function
from time import time
from collections import OrderedDict

class UnionFind(object):
    
    def __init__(self,size):
        self.id = []
        self.sz = []
        for i in range(size):
            self.id.append(i)
            self.sz.append(1)
    
    def root(self, i):        
        while self.id[i] != i:
            self.id[i] = self.id[self.id[i]]
            i = self.id[i]
        return i
    
    def getRoot(self, i):
        return self.id[i]
    
    def union(self, p, q):
        
        rootP = self.root(p)
        rootQ = self.root(q)
        
        if rootP == rootQ:
            return
        
        if self.sz[rootP] < self.sz[rootQ]:
            self.id[rootP] = rootQ
            self.sz[rootQ] += self.sz[rootP]
        else:
            self.id[rootQ] = rootP
            self.sz[rootP] += self.sz[rootQ]
        
    def connected(self, p, q):
        return self.root(p) == self.root(q)

def printGrid(grid):
        
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] != -1:
                print(grid[i][j],end = "")
            else:
                print('*',end = "")
        print("")
    print("")
    
def createClusters(grid, gridSize):
    
    gridClusters = {}
    
    ufGrid = UnionFind(gridSize*gridSize)
    
    for i in range(gridSize):
        for j in range(gridSize):           
            
            if grid[i][j] == -1:
                continue
            
            if i != 0:
                if grid[i - 1][j] == grid[i][j]:
                    ufGrid.union(gridSize*(i - 1) + j, gridSize*i + j)
                
            if j != 0:
                if grid[i][j - 1] == grid[i][j]:
                    ufGrid.union(gridSize*(i) + j - 1, gridSize*i + j)
            
    
    for i in range(gridSize):
        for j in range(gridSize):
                        
            if grid[i][j] == -1:
                continue
            
            root = ufGrid.root(gridSize * i + j)
            if gridClusters.has_key(root):
                gridClusters[root].append(gridSize * i + j)
            else:
                gridClusters[root] = [gridSize * i + j]
                
    return gridClusters

def applyGravity(grid, gridSize):
    
    for i in range(gridSize):
        
        emptySpots = 0        
        gridCol = []
        
        for j in range(gridSize):
            if grid[gridSize - j - 1][i]!= -1:
                gridCol.append(grid[gridSize - j - 1][i])
            else:
                emptySpots += 1                
        
        for _ in range(emptySpots):
            gridCol.append(-1)
        
        for j in range(gridSize):
            grid[j][i] = gridCol.pop()
            
def eatFruits(grid, gridSize, positions):
    
    lenP = len(positions)
    
    for p in positions:
        i = p / gridSize
        j = p % gridSize
        grid[i][j] = -1
    
    applyGravity(grid, gridSize)
    
    return lenP * lenP
  
def calculateDepth(bFactor, gridSize, timeLeft):
    
    #default
    depth = 2
    
    if timeLeft < 15.0:
        return 0
    
    if bFactor <= 10:
        if timeLeft > 100.0:
            depth = 8            
        elif timeLeft > 50.0:
            depth = 6
        else:
            depth = 2
        
    elif bFactor <= 16:
        if timeLeft > 180.0:
            depth = 6
        elif timeLeft > 70.0:
            depth = 4
        else:
            depth = 2
    elif bFactor <= 24:
        if timeLeft > 120.0:
            if gridSize <= 8:
                depth = 6
            elif gridSize <= 18:
                depth = 4
            else:
                depth = 2
        else:
            depth = 2
    elif bFactor <= 32:
        if timeLeft > 150.0:
            if gridSize <= 12:
                depth = 4
            else:
                depth = 2
        else:
            depth = 2
    elif bFactor <= 150:
        if timeLeft > 180.0: 
            depth = 2
        else:
            depth = 0
    else:
        depth = 0           
    
#     print("Depth: ",depth )
#     print("BranchingFactor: ", bFactor )
    return depth
    
def selectBestMove(grid, gridSize, timeLeft):
        
    utility = -1
    utilVal = -308915776
    gridClusters = createClusters(grid, gridSize)
    
    sortedClusters = {}
        
    for key in gridClusters:
        sortedClusters[key] = len(gridClusters[key])
    
    sortedClusters = OrderedDict(sorted(sortedClusters.items(), key = lambda x: x[1]))
    
    if len(sortedClusters) == 1:
        keyVal = sortedClusters.popitem()
        return keyVal[0]
    
    bFactor = len(sortedClusters)
    depth = calculateDepth(bFactor, gridSize, timeLeft)
    
    for key in range(len(sortedClusters)):
        
        tempGrid = [ list(i) for i in grid ]
        keyVal = sortedClusters.popitem()
        agentScore = eatFruits(tempGrid, gridSize, gridClusters[keyVal[0]])
        oppnScore = maxValue(tempGrid, gridSize, utilVal, keyVal[1] * keyVal[1], depth)
        
        newUtilVal = agentScore - oppnScore
        
        if newUtilVal > utilVal:
            utilVal = newUtilVal
            utility = keyVal[0]
                         
    return utility

def maxValue(grid, gridSize, alpha, parent, depth):
        
    utilVal = -308915776
    gridClusters = createClusters(grid, gridSize)
    
    sortedClusters = {}
        
    for key in gridClusters:
        sortedClusters[key] = len(gridClusters[key])
    
    sortedClusters = OrderedDict(sorted(sortedClusters.items(), key = lambda x: x[1]))
    
    if depth == 0 or len(sortedClusters) == 1:
        keyVal = sortedClusters.popitem()
        return keyVal[1] * keyVal[1]
    
    for key in range(len(sortedClusters)):
        
        tempGrid = [ list(i) for i in grid ]
        keyVal = sortedClusters.popitem()
        agentScore = eatFruits(tempGrid, gridSize, gridClusters[keyVal[0]])
        oppnScore = maxValue(tempGrid, gridSize, utilVal, keyVal[1] * keyVal[1], depth - 1)
        
        newUtilVal = agentScore - oppnScore
                
        if newUtilVal > utilVal:
            utilVal = newUtilVal
                     
        if parent - utilVal <= alpha:
            return utilVal
                
    return utilVal
    
ipFile = open("input.txt")
opFile = open("output.txt","w")

gridSize = int(ipFile.readline())
fruitTypes = int(ipFile.readline())
timeLeft = float(ipFile.readline())

gridOriginal = []

for i in range(gridSize):
    gridOriginal.append([int(s) if s != '*' else int("-1") for s in ipFile.readline().rstrip().strip()])

t0 = time()
clust = createClusters(gridOriginal, gridSize)


if len(clust) != 0:

    bestMove = selectBestMove(gridOriginal, gridSize, timeLeft)
    eatFruits(gridOriginal, gridSize, clust[bestMove])
    applyGravity(gridOriginal, gridSize)
       
    col = (bestMove % gridSize) + 65
    row = (bestMove / gridSize) + 1
    
    bestMoveStr = chr(col) + str(row)
    
#     print(bestMoveStr)
#     printGrid(gridOriginal)

else:
    bestMoveStr = "NA"

t1 = time()
print(t1-t0)

opFile.write(bestMoveStr+"\n")
for i in range(gridSize):
    for j in range(gridSize):
        if gridOriginal[i][j] == -1:
            opFile.write("*")
        else:
            opFile.write(str(gridOriginal[i][j]))
    opFile.write("\n")
ipFile.close()
opFile.close()