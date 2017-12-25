'''
Created on Oct 14, 2017

@author: ishan
'''

from __future__ import print_function
from Tkinter import Tk, Label, Button, Frame, PhotoImage
from random import randint
from collections import OrderedDict

class envVar():
    gridSize = 0
    fruitTypes = 0
    timeLeft = 300.0
    gridOriginal = []
    agentScore = 0
    humanScore = 0
    agentPlay = False

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

class AIagent():
    humanScore = 0
    agentScore = 0
    def selectBestMove(self, grid, gridSize, timeLeft):
        
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
        depth = self.calculateDepth(bFactor, gridSize, timeLeft)
        
        for key in range(len(sortedClusters)):
            
            tempGrid = [ list(i) for i in grid ]
            keyVal = sortedClusters.popitem()
            agentScore = eatFruits(tempGrid, gridSize, gridClusters[keyVal[0]])
            oppnScore = self.maxValue(tempGrid, gridSize, utilVal, keyVal[1] * keyVal[1], depth)
            
            newUtilVal = agentScore - oppnScore
            
            if newUtilVal > utilVal:
                utilVal = newUtilVal
                utility = keyVal[0]
                             
        return utility
    
    def maxValue(self, grid, gridSize, alpha, parent, depth):
        
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
            oppnScore = self.maxValue(tempGrid, gridSize, utilVal, keyVal[1] * keyVal[1], depth - 1)
            
            newUtilVal = agentScore - oppnScore
                    
            if newUtilVal > utilVal:
                utilVal = newUtilVal
                         
            if parent - utilVal <= alpha:
                return utilVal
                    
        return utilVal
    
    def calculateDepth(self, bFactor, gridSize, timeLeft):
    
        #default
        depth = 2
        
        if timeLeft < 15.0:
            return 0
        
        if bFactor <= 10:
            if timeLeft > 100.0:
                depth = 12
                
            elif timeLeft > 50.0:
                depth = 6
            else:
                depth = 2
            
        elif bFactor <= 16:
            if timeLeft > 180.0:
                if gridSize <= 12:
                    depth = 8
                else:
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
        elif bFactor <= 48:
            if timeLeft > 70.0: 
                depth = 2
            else:
                depth = 0
        else:
            depth = 0           
        
        print("Depth: ",depth )
        print("BranchingFactor: ", bFactor )
        return depth

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

def generateRanGrid():
    
    for r in range(envVar.gridSize):
        for c in range(envVar.gridSize):
            envVar.gridOriginal[r][c] = randint(0,2)
    
    return ""

class buildUI(object):
    
    def __init__(self, gridSize):
        self.top = Tk()
        self.top.geometry('{}x{}'.format(530, 550))
        
        self.topLeft = Frame(self.top, height = 100, width = 550, background="white").grid(row=0, rowspan = 10, column = 0, columnspan=55)        
        self.bottomLeft = Frame(self.top, height = 450, width = 400, background="bisque").grid(row=10, rowspan = 40,  column = 0, columnspan=40)
        self.bottomRight = Frame(self.top, height = 450, width = 150, background="white").grid(row=10, rowspan = 40,  column = 40, columnspan=15)
        self.buttons = []
        self.packButtons(gridSize)
        self.agentBut = Button(self.bottomRight, height = 2 , width = 8, text = "Agent Play", command = lambda: self.agentCallBack()).grid(row=10, rowspan = 1,  column = 45, columnspan=1)
        
        scoreHuman = "Your Score: " + str(AIagent.humanScore)
        self.labelScoreH = Label(self.bottomRight,  height = 2 , width = 16, text = scoreHuman).grid(row=11, rowspan = 1,  column = 45, columnspan=1)
        
        scoreAgent = "Agent Score: " + str(AIagent.agentScore)
        self.labelScoreA = Label(self.bottomRight,  height = 2 , width = 16, text = scoreAgent).grid(row=12, rowspan = 1,  column = 45, columnspan=1)
        self.agentBut = Button(self.bottomRight, height = 2 , width = 8, text = "Restart", command = lambda: self.restartGame()).grid(row=15, rowspan = 1,  column = 45, columnspan=1)
        
        self.top.mainloop() 
    
    def packButtons(self, gridSize): 
        self.pic1 = PhotoImage(file="1.gif").subsample(6, 6)
        self.pic2 = PhotoImage(file="2.gif").subsample(6, 6)   
        self.pic3 = PhotoImage(file="3.gif").subsample(6, 6)   
        for r in range(gridSize):
            for c in range(gridSize):
                pos = gridSize*r + c
                b = Button(self.bottomLeft, command = lambda pos=pos: self.helloCallBack(pos))
                if envVar.gridOriginal[r][c] == 0:                    
                    b.config(image=self.pic1)
                elif envVar.gridOriginal[r][c] == 1:                  
                    b.config(image=self.pic2)
                elif envVar.gridOriginal[r][c] == 2:                  
                    b.config(image=self.pic3)
                else:
                    b.config(text = "-1")                    
                    
                self.buttons.append(b)
                self.buttons[pos].grid(row = 10 + r,  column = c)
                
    def helloCallBack(self, i):            
#         print( "clicked" + str(i))
        if envVar.agentPlay == True:
            return
        clust = createClusters(envVar.gridOriginal, envVar.gridSize) 
        if not clust:
            return
        sortedClusters = {}            
        for key in clust:
            sortedClusters[key] = key
            for val in clust[key]:
                sortedClusters[val] = key
        sortedClusters = OrderedDict(sorted(sortedClusters.items(), key = lambda x: -x[1]))             
                  
        envVar.humanScore += eatFruits(envVar.gridOriginal, envVar.gridSize, clust[sortedClusters[i]])    
#         printGrid(envVar.gridOriginal)
        self.updateButtons()
        scoreHuman = "Your Score: " + str(envVar.humanScore)
        self.labelScoreH = Label(self.bottomRight,  height = 2 , width = 16, text = scoreHuman).grid(row=11, rowspan = 1,  column = 45, columnspan=1)
        envVar.agentPlay = True
    
    def agentCallBack(self):
        clust = createClusters(envVar.gridOriginal, envVar.gridSize) 
        if envVar.agentPlay == False:
            return
        if not clust:
            return
        sortedClusters = {}            
        for key in clust:
            sortedClusters[key] = len(clust[key])
            
        sortedClusters = OrderedDict(sorted(sortedClusters.items(), key = lambda x: -x[1])) 
         
        agent = AIagent()
        agentMove = agent.selectBestMove(envVar.gridOriginal, envVar.gridSize, envVar.timeLeft)
        AIagent.agentScore += eatFruits(envVar.gridOriginal, envVar.gridSize, clust[agentMove]) 
        self.updateButtons()
        scoreAgent = "Agent Score: " + str(AIagent.agentScore)
        self.labelScoreA = Label(self.bottomRight,  height = 2 , width = 16, text = scoreAgent).grid(row=12, rowspan = 1,  column = 45, columnspan=1)
        envVar.agentPlay = False
        
    def updateButtons(self): 
        self.pic1 = PhotoImage(file="1.gif").subsample(6, 6)
        self.pic2 = PhotoImage(file="2.gif").subsample(6, 6)     
        self.pic3 = PhotoImage(file="3.gif").subsample(6, 6)        
        for r in range(envVar.gridSize):
            for c in range(envVar.gridSize):
                if envVar.gridOriginal[r][c] == 0:                    
                    self.buttons[envVar.gridSize*r + c].config(image=self.pic1)
                elif envVar.gridOriginal[r][c] == 1:                  
                    self.buttons[envVar.gridSize*r + c].config(image=self.pic2)
                elif envVar.gridOriginal[r][c] == 2:                  
                    self.buttons[envVar.gridSize*r + c].config(image=self.pic3)
    
    def restartGame(self):  
#         envVar.agentPlay = True     
        self.top.destroy()
        generateRanGrid()
        AIagent.agentScore = 0
        AIagent.humanScore = 0
        envVar.agentScore = 0
        envVar.humanScore = 0
        _gameUI = buildUI(envVar.gridSize)
        return ""

# ipFile = open("input.txt")
# opFile = open("output.txt","w")

envVar.gridSize = 8
envVar.fruitTypes = 2
envVar.timeLeft = 0.0

envVar.gridOriginal = [[-1 for _ in range(envVar.gridSize) ] for _ in range(envVar.gridSize)]
printGrid(envVar.gridOriginal)
generateRanGrid()
# for i in range(envVar.gridSize):
#     envVar.gridOriginal.append([int(s) if s != '*' else int("-1") for s in ipFile.readline().rstrip().strip()])

envVar.agentScore = 0
envVar.humanScore = 0

printGrid(envVar.gridOriginal)

gameUI = buildUI(envVar.gridSize)

# 