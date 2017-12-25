'''
Created on Oct 15, 2017
@author: ishank mishra

Game State: A game state is represented by a square grid. 
            Each element in the grid holds an integer value or the character '*'. 
            A non-negative integer represents a fruit of type its value
            Character '*' represents an empty cell. (represented by value -1 in the implementation)
            e.g.    ******
                    ******
                    3**15*
                    26034*
                    36444*
                    133665
            
Input: 
    The file input.txt in the current directory of your program will be formatted as follows:
        First line:     integer n, the width and height of the square board (0 < n <= 26)
        Second line:    integer p, the number of fruit types (0 < p <= 9)
        Third line:     strictly positive floating point number, remaining time in seconds
        Next n lines:   the n x n board, with one board row per input file line, and n characters (plus endof-
                        line marker) on each line. Each character can be either a digit from 0 to p-1, or
                        a * to denote an empty cell.

Output: 
    The file output.txt which your program creates in the current directory should be formatted as follows:
    
    First line:     Selected move, represented as two characters: A letter from A to Z representing the 
                    column number (where A is the leftmost column, B is the next one to the right, etc), and
                    a number from 1 to 26 representing the row number (where 1 is the top row, 2 is
                    the row below it, etc).
    Next n lines:   the n x n board just after the move and after gravity has been applied to make
                    any fruits fall into holes created by the move taking away some fruits
'''

from __future__ import print_function
from time import time
from collections import OrderedDict

# Data Structure used to find connected components in a grid
# Weighted Union Find with path compression
# Uses a 1D Array
class UnionFind(object):
    
    def __init__(self, size):
        self.id = []    # Stores the index of the root element
        self.sz = []    # Size of the subtree with current element as the root
        # Initialize every element in grid as its own root and subtree size 1
        for i in range(size):   
            self.id.append(i)
            self.sz.append(1)
    
    # Return the root of the element i
    def root(self, i):        
        while self.id[i] != i:  # The root element has its id same as the index
            self.id[i] = self.id[self.id[i]]    # Condensing the tree
            i = self.id[i]
        return i
    
    def getRoot(self, i):
        return self.id[i]
    
    # Join two connected components p and q
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
    
    # Check the connectivity of two components
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
   
# Create clusters of connected components 
# i.e. group elements that are adjacent (horizontally and vertically) and have the same value 
def createClusters(grid, gridSize):
    
    # clusters/ connected components indexed by root
    gridClusters = {}
    
    # Create an Union Find object
    ufGrid = UnionFind(gridSize*gridSize)
    
    # For every element check if the elements above and to the left of it has the same value
    for i in range(gridSize):
        for j in range(gridSize):           
            
            # The element has no fruit
            if grid[i][j] == -1:
                continue
            
            if i != 0:
                # Does the element above have the same value
                if grid[i - 1][j] == grid[i][j]:
                    # Connect the two components
                    ufGrid.union(gridSize*(i - 1) + j, gridSize*i + j)
                
            if j != 0:
                # Does the element to the left have the same value
                if grid[i][j - 1] == grid[i][j]:
                    # Connect the two components
                    ufGrid.union(gridSize*(i) + j - 1, gridSize*i + j)
            
    # Store the clusters/connected components in the dictionary
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

# Place all the elements with value greater than zero below the elements with value -1 while maintaining the order
def applyGravity(grid, gridSize):
    
    # Traverse vertically (column-wise)
    for i in range(gridSize):
        
        # Count the number of elements with value -1 in every column
        emptySpots = 0        
        # Store the values other than -1 in an array (so that the order is maintained)
        gridCol = []
        
        # Check each element in a column bottom-up
        for j in range(gridSize):
            if grid[gridSize - j - 1][i]!= -1:
                gridCol.append(grid[gridSize - j - 1][i])
            else:
                emptySpots += 1                
        
        # By now all elements with value not equal to -1 are stored in gridCol
        # Fill the array with values -1 such that the size of the array is same as column size
        for _ in range(emptySpots):
            gridCol.append(-1)
        
        # Update the values stored in gridCol to the grid
        for j in range(gridSize):
            grid[j][i] = gridCol.pop()
    
# Set the value of every element in the connected component to -1. Then apply gravity  
def eatFruits(grid, gridSize, positions):
    
    lenP = len(positions)
    
    for p in positions:
        i = p / gridSize
        j = p % gridSize
        grid[i][j] = -1

    applyGravity(grid, gridSize)
    
    return lenP * lenP
  
# Calculates the depth of the search based on Branching Factor, Grid Size and time remaining
def calculateDepth(bFactor, gridSize, timeLeft):
    # The values used here are empirical 
    
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
    
# Selects the best move at a given Game state
def selectBestMove(grid, gridSize, timeLeft):
    
    utility = -1            # The position with the best possible move
    utilVal = -308915776    # Utility: The difference of scores from the opponent if a move is selected
    
    # Set of possible moves i.e. clusters/connected components
    gridClusters = createClusters(grid, gridSize)
    
    sortedClusters = {}
        
    for key in gridClusters:
        sortedClusters[key] = len(gridClusters[key])
    
    # Order the clusters in decreasing order of size (number of elements in it)
    sortedClusters = OrderedDict(sorted(sortedClusters.items(), key = lambda x: x[1]))
    
    # Return the move if only that move is possible
    if len(sortedClusters) == 1:
        keyVal = sortedClusters.popitem()
        return keyVal[0]
    
    # Decide the depth of search using the calculateDepth function
    bFactor = len(sortedClusters)   # Number of possible moves
    depth = calculateDepth(bFactor, gridSize, timeLeft)
    
    # Iterate for every possible move
    for key in range(len(sortedClusters)):
        
        # Use a copy of the current state, useful for backtracking
        tempGrid = [ list(i) for i in grid ]
        # current move
        keyVal = sortedClusters.popitem()
        
        # Calculate the agent score if this move is selected 
        agentScore = eatFruits(tempGrid, gridSize, gridClusters[keyVal[0]])
        # Calculate the opponent's utility corresponding to this move 
        # The search should confine to a depth limit 
        oppnScore = maxValue(tempGrid, gridSize, utilVal, keyVal[1] * keyVal[1], depth)
        
        # Utility of the move
        newUtilVal = agentScore - oppnScore
        
        # Compare this move to the moves selected till now
        if newUtilVal > utilVal:
            utilVal = newUtilVal
            utility = keyVal[0]
    
    # Return the move with highest utility                     
    return utility

# Similar to the function selectBestMove 
# Except that it returns the Utility value considering the depth of search 
def maxValue(grid, gridSize, alpha, parent, depth):
    # The variable alpha is used for pruning the search
    # alpha stores the value of best possible utility value calculated so far
        
    utilVal = -308915776    # Utility: The difference of scores from the opponent if a move is selected
    
    # Set of possible moves i.e. clusters/connected components
    gridClusters = createClusters(grid, gridSize)
    
    sortedClusters = {}
        
    for key in gridClusters:
        sortedClusters[key] = len(gridClusters[key])
    
    # Order the clusters in decreasing order of size (number of elements in it)
    sortedClusters = OrderedDict(sorted(sortedClusters.items(), key = lambda x: x[1]))
    
    # Return the move if only that move is possible or the maximum depth is reached
    if depth == 0 or len(sortedClusters) == 1:
        keyVal = sortedClusters.popitem()
        return keyVal[1] * keyVal[1]
    
    # Iterate for every possible move
    for key in range(len(sortedClusters)):
        
        # Use a copy of the current state, useful for backtracking
        tempGrid = [ list(i) for i in grid ]
        # current move
        keyVal = sortedClusters.popitem()
        # Calculate the agent score if this move is selected 
        agentScore = eatFruits(tempGrid, gridSize, gridClusters[keyVal[0]])
        # Calculate the opponent's utility corresponding to this move
        # Decrement the depth by 1
        oppnScore = maxValue(tempGrid, gridSize, utilVal, keyVal[1] * keyVal[1], depth - 1)
        
        # Utility of the move
        newUtilVal = agentScore - oppnScore
                
        # Compare this move to the moves selected till now
        if newUtilVal > utilVal:
            utilVal = newUtilVal
        
        # Prune the search if the Utility value is no better than the best so far
        if parent - utilVal <= alpha:
            return utilVal
              
    # Return the move with highest utility     
    return utilVal

def main():
    
    ipFile = open("input.txt")
    opFile = open("output.txt","w")
    
    gridSize = int(ipFile.readline())       # Size of the grid
    _fruitTypes = int(ipFile.readline())    # Unused
    timeLeft = float(ipFile.readline())     # Time limit for the search
    
    # State of the game
    gridOriginal = []
    
    for i in range(gridSize):
        gridOriginal.append([int(s) if s != '*' else int("-1") for s in ipFile.readline().rstrip().strip()])
    
    t0 = time()
    clust = createClusters(gridOriginal, gridSize)
    
    # Check if the board is empty
    if len(clust) != 0:
        
        # Select the best possible move at the current state
        bestMove = selectBestMove(gridOriginal, gridSize, timeLeft)
        
        # Build the next state
        eatFruits(gridOriginal, gridSize, clust[bestMove])
        applyGravity(gridOriginal, gridSize)
           
        # Convert the move to Output format   
        col = (bestMove % gridSize) + 65
        row = (bestMove / gridSize) + 1
        
        # The best move in output format
        bestMoveStr = chr(col) + str(row)
        
        print(bestMoveStr)
        printGrid(gridOriginal)
    
    else:
        bestMoveStr = "NA"
    
    t1 = time()
    print(t1-t0)
    
    # Handling the final result
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
    
if __name__ == "__main__":
    main()