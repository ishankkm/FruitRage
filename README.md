# FruitRage 
### Minimax game playing AI agent

The Fruit Rage is a two player game in which each player tries to maximize his/her share from a batch of fruits randomly placed in a box. The box is divided into cells and each cell is either empty or filled with one fruit of a specific type.

* At the beginning of each game, all cells are filled with fruits. 
* Players play in turn and can pick a cell of the box in their own turn and claim all fruit of the same type, in all cells that are connected to the selected cell through horizontal and vertical paths. 
* For each selection or move the agent is rewarded a numeric value which is the square of the number of fruits claimed in that move. 
* Once an agent picks the fruits from the cells, their empty place will be filled with other fruits on top of them (which fall down due to gravity), if any. In this game, no fruit is added during game play. Hence, players play until all fruits have been claimed.

##### Time Constraint
* Every agent has a limited amount of time to spend for thinking during the whole game. 
* Spending more than the original allocated time will be penalized harshly. Each player is allocated a fixed total amount of time. 
* When it is your turn to play, you will also be told how much remaining time you have. The time you take on each move will be subtracted from your total remaining time. 
* If your remaining time reaches zero, your agent will automatically lose the game. 
* The overall score of each player is the sum of rewards gained for every turn. 
* The game will terminate when there is no fruit left in the box or when a player has run out of time.

##### Game State
- A game state is represented by a square grid. 
- Each element in the grid holds an integer value or the character '*'. 
- A non-negative integer represents a fruit of type its value
- Character '*' represents an empty cell. (represented by value -1 in the implementation)
- e.g.
    ```******
    ******
    3**15*
    26034*
    36444*
    133665
            
##### Input
The file input.txt in the current directory of your program will be formatted as follows:

    First line:     integer n, the width and height of the square board (0 < n <= 26)
    Second line:    integer p, the number of fruit types (0 < p <= 9)
    Third line:     strictly positive floating point number, remaining time in seconds
    Next n lines:   the n x n board, with one board row per input file line, and n characters (plus endof-
                    line marker) on each line. Each character can be either a digit from 0 to p-1, or
                    a * to denote an empty cell.
    e.g.
        10
        4
        1.276
        3102322310
        0121232013
        3021111113
        0221031132
        0230011012
        0323321010
        2003022012
        2202200021
        0130000020
        2200022231
                    
##### Output
The file output.txt which your program creates in the current directory should be formatted as follows:

    First line:     Selected move, represented as two characters: A letter from A to Z representing the 
                    column number (where A is the leftmost column, B is the next one to the right, etc), and
                    a number from 1 to 26 representing the row number (where 1 is the top row, 2 is
                    the row below it, etc).
    Next n lines:   the n x n board just after the move and after gravity has been applied to make
                    any fruits fall into holes created by the move taking away some fruits
                    
    e.g. 
        G8
        31******10
        010*****13
        3022322*13
        0221232*32
        0221111*12
        0331031310
        2020011012
        2203321121
        0103022120
        2232222231

