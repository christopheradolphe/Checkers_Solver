# Checkers_Solver
I have implemented a program that can solve a Checkers endgame puzzle using alpha-beta pruning and node ordering for optimization.

**About Checkers:**
Checkers is a two-player board game played on an eight by eight chess board. One player's pieces
are black, and the other player's pieces are red. The players take turns moving pieces on the board.
The red player moves first.

**Move Rules**
There are two different ways to move.
1. Simple move: 
A simple move involves moving a piece one square diagonally to an adjacent unoccupied dark square. 
Normal pieces can move diagonally forward only; kings can move in any diagonal direction. (For
the black player, forward is down. For the red player, forward is up.) 

2. Jump:
A jump consists of moving a piece diagonally adjacent to an opponent's piece to an empty 
square immediately beyond it in thesame direction (thus "jumping over" the opponent's piece front and back.) 
Normal pieces canjump diagonally forward only; kings can jump in any diagonal direction. A jumped piece is
"captured" and removed from the game. Any piece, king or normal, can jump a king.
Jumping is mandatory. If a player has the option to jump, they must make it, even if doing
so results in a disadvantage for the jumping player.

3. Multiple jumps:
After one jump, if the moved piece can jump another opponent's piece, it must keep jumping until
no more jumps are possible, even if the jump is in a different diagonal direction. If more than one
multi-jump is available, the player can choose which piece to jump with and which sequence of jumps to
make. The sequence chosen is not required to be the one that maximizes the number of jumps in turn.
However, a player must make all the available jumps in the sequence chosen.

**Kings:**
If a piece moves into the last row on the opponent's side of the board, it becomes a king and
can move both forward and backward. A red piece becomes king when it reaches the top row,
and a black piece becomes king when it reaches the bottom row.
If a piece becomes a king, the current move terminates; The piece cannot jump back as in a
multi-jump until the next move.

**End of Game**
A player wins by capturing all the opponent's pieces or when the opponent has no
legal moves left.

**State Representation**
I have represented  each state in the following format:
Each state is a grid of 64 characters. The grid has eight rows with eight characters per row.
’ . ’ (the period character) denotes an empty square.
’ r ’ denotes a red piece,
’ b ’ denotes a black piece,
’ R ’ denotes a red king,
’ B ’ denotes a black king.

eg. 
........
....b...
.......R
..b.b...
...b...r
........
...r....
....B...

**Input and Output Files**
Each input file contains one state. Your program controls the red pieces, and it is your turn to make a
move.

Each output file contains the sequence of states until the end of the game. The first state is the same
as the state in the input file. The last state is a state denoting the end of the game. There is one
empty line between any two consecutive states.

**Process to Solve Puzzles**
My program controls both players. Both players use alpha-beta pruning with the same
depth limit to determine their best move at their turn.

The game proceeds as follows:
- Start by specifying a depth limit.
- The red player runs alpha-beta pruning with the depth limit to determine their move. Then, the red player carries out the move.
- Next, the black player runs alpha-beta pruning with the depth limit to determine their move.
Then, the black player carries out the move.
- This process continues until the game ends.

**Program Design Considerations**

**How does the program calculate the utility of each terminal state?**
If the red player has won the game, utility is infinity. If the black player has won the game, utility is negative infinity.

**How does the program estimate the utility of each non-terminal state?**
My program estimates the utility using a number of factors that play a role in determining who has the advantage in checkers. 
Firstly, the number of pieces is counted as players typically want more pieces. Kings are given an additional half a point 
(1.5 points in total) as they have twice the mobility of regular pieces. As the centre four slots are advantageous, an additional 
0.25 points is given for having a piece in one of these positions. Given the closer a piece is to the end, the more likely it is 
to become a king, a fraction of the piece’s advancement to the end is additionally awarded to the regular pieces. Pieces touching 
an edge are unabled to be captured and this defensive ability gives them an additional 0.01 points. Pieces on the home line are 
given an additional 0.25 points for being on an edge as they limit the ability of the opponent to get a King.

**Node Ordering**
My program performs node ordering to increase the number of pruned states as we traverse the tree. In the MAX_VALUE function, 
the possible moves from a state are first found and then sorted in decreasing order (largest to smallest) of the evaluation 
function for that possible move. This ordering is achieved via a priority queue which contains tuples of three values: the evaluation 
function for the board; a hash of the board to serve as a tiebreaker; and the board itself. The MIN_VALUE function implements a similar 
procedure except the moves are sorted in increasing order (smallest to largest).
