from copy import deepcopy
from heapq import heappush, heappop
import heapq  
import argparse

#====================================================================================
depth_limit = 8
char_red_king = 'R'
char_red_basic = 'r'
char_black_king = 'B'
char_black_basic = 'b'
valid_black = ['b', 'B']
valid_red = ['r', 'R']
empty_slot = '.'
valid_positions = [0, 1, 2, 3, 4, 5, 6, 7]
stalemate = False
centre_slots = [(2,3), (3,4), (4,3), (5,4)]
utility = float('inf')
neg_utility = float('-inf')


class Piece:
    """
    This represents a piece on the Hua Rong Dao puzzle.
    """

    def __init__(self, is_red, is_king, coord_x, coord_y):
        """
        :param is_goal: True if the piece is the goal piece and False otherwise.
        :type is_goal: bool
        :param is_single: True if this piece is a 1x1 piece and False otherwise.
        :type is_single: bool
        :param coord_x: The x coordinate of the top left corner of the piece.
        :type coord_x: int
        :param coord_y: The y coordinate of the top left corner of the piece.
        :type coord_y: int
        :param orientation: The orientation of the piece (one of 'h' or 'v') 
            if the piece is a 1x2 piece. Otherwise, this is None
        :type orientation: str
        """

        self.is_red = is_red
        self.is_king = is_king
        self.coord_x = coord_x
        self.coord_y = coord_y

    def __repr__(self):
        return '{} {} {} {}'.format(self.is_red, self.is_king, \
            self.coord_x, self.coord_y)

class Board:
    """
    Board class for setting up the playing board.
    """

    def __init__(self, pieces):
        """
        :param pieces: The list of Pieces
        :type pieces: List[Piece]
        """

        self.width = 8
        self.height = 8

        self.pieces = pieces

        # self.grid is a 2-d (size * size) array automatically generated
        # using the information on the pieces when a board is being created.
        # A grid contains the symbol for representing the pieces on the board.
        self.grid = []
        self.__construct_grid()


    def __construct_grid(self):
        """
        Called in __init__ to set up a 2-d grid based on the piece location information.

        """
        self.grid = []
        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append('.')
            self.grid.append(line)

        for piece in self.pieces:
            if piece.is_red: ## Piece is red
              if piece.is_king:
                self.grid[piece.coord_y][piece.coord_x] = char_red_king
              else:
                self.grid[piece.coord_y][piece.coord_x] = char_red_basic
            else:
              if piece.is_king:
                self.grid[piece.coord_y][piece.coord_x] = char_black_king
              else:
                self.grid[piece.coord_y][piece.coord_x] = char_black_basic
                

    def display(self):
        """
        Print out the current board.

        """
        for i, line in enumerate(self.grid):
            for ch in line:
                print(ch, end='')
            print()

    def red_piece_finder(self):
        coord = [[],[]] ## First list is for king locations, second is for basic pieces
        for piece in self.pieces:
            if piece.is_red and piece.is_king:
                coord[0].append((piece.coord_x, piece.coord_y))
            elif piece.is_red and not piece.is_king:
                coord[1].append((piece.coord_x, piece.coord_y))
        return coord
    
    def black_piece_finder(self):
        coord = [[],[]] ## First list is for king locations, second is for basic pieces
        for piece in self.pieces:
            if not piece.is_red and piece.is_king:
                coord[0].append((piece.coord_x, piece.coord_y))
            elif not piece.is_red and not piece.is_king:
                coord[1].append((piece.coord_x, piece.coord_y))
        return coord
    
    def pieces_on_board(self, colour): ##Change to function that finds all pieces of that colour
        """
        Finds all empty spaces in the board. Returns list of tuples in form of [(x1,y1), (x2,y2)]

        :return: List of tuples containing coordinates of empty piecies
        :rtype: List[Tuples]
        :colour : True if red turn
        """ 
        if colour == True:
            coordinates_of_pieces = self.red_piece_finder()
        else:
            coordinates_of_pieces = self.black_piece_finder()
        return coordinates_of_pieces

    def general_move_check(self, red_turn, x_c, y_c, jumps, regular, x_d, y_d, is_King):
        if len(jumps) == 0 or jumps == None:
            #Check regular moves too
            if ((x_c + x_d) in valid_positions) and ((y_c + y_d) in valid_positions):
                if self.grid[y_c + y_d][x_c + x_d] == empty_slot:
                    new_board = deepcopy(self)
                    new_board.move(x_c, y_c, x_d, y_d, jumps, red_turn, is_King)
                    regular.append(new_board)
        if ((x_c + 2 * x_d) in valid_positions) and ((y_c + 2 * y_d) in valid_positions):
            if red_turn:
                if self.grid[y_c + y_d][x_c + x_d] in valid_black and self.grid[y_c + 2 * y_d][x_c + 2 * x_d] == empty_slot:
                    jumps = self.jump_finder(red_turn, x_c, y_c, x_d, y_d, jumps, is_King)
            else:
                if self.grid[y_c + y_d][x_c + x_d] in valid_red and self.grid[y_c + 2 * y_d][x_c + 2 * x_d] == empty_slot:
                    jumps = self.jump_finder(red_turn, x_c, y_c, x_d, y_d, jumps, is_King)
        return (jumps, regular)
    
    def up_right_move_check(self, red_turn, x_coord, y_coord, jumps, regular, is_King):
        (jumps, regular) = self.general_move_check(red_turn, x_coord, y_coord, jumps, regular, 1, -1, is_King)
        return (jumps, regular)

    def up_left_move_check(self, red_turn, x_coord, y_coord, jumps, regular, is_King):
        (jumps, regular) = self.general_move_check(red_turn, x_coord, y_coord, jumps, regular, -1, -1, is_King)
        return (jumps, regular)
    
    def down_right_move_check(self, red_turn, x_coord, y_coord, jumps, regular, is_King):
        (jumps, regular) = self.general_move_check(red_turn, x_coord, y_coord, jumps, regular, 1, 1, is_King)
        return (jumps, regular)
    
    def down_left_move_check(self, red_turn, x_coord, y_coord, jumps, regular, is_King):
        (jumps, regular) = self.general_move_check(red_turn, x_coord, y_coord, jumps, regular, -1, 1, is_King)
        return (jumps, regular)

    def jump_finder(self, red_turn, x_coord, y_coord, x_change, y_change, jumps, is_King): ##recursive function to find all jumps
        '''
        Keep appending new states to a list which keep going recursively
        0. We know jump is possible so make copy of board and make the move 
        1. Base Case: if end of turn
            a) no more jumps possible
            b) becomes a King
        2. Check if two directions work for normal and if so make copy of board and make the move 
        3. If King check all the directions
        '''
        new_board = deepcopy(self)
        (new_board, new_King) = new_board.move(x_coord, y_coord, x_change, y_change, True, red_turn, is_King)
        count = 0
        x_c = x_coord + 2 * x_change
        y_c = y_coord + 2 * y_change
        
        if new_King:
           jumps.append(new_board) 
           return jumps

        if not red_turn:
            if (x_c + 2) in valid_positions and (y_c + 2) in valid_positions:
                if new_board.grid[y_c + 1][x_c + 1] in valid_red and new_board.grid[y_c + 2][x_c + 2] == empty_slot:
                    jumps = new_board.jump_finder(red_turn, x_c, y_c, 1, 1, jumps, is_King)
                    count += 1
            if (x_c - 2) in valid_positions and (y_c + 2) in valid_positions:
                if new_board.grid[y_c + 1][x_c - 1] in valid_red and new_board.grid[y_c + 2][x_c - 2] == empty_slot:
                    jumps = new_board.jump_finder(red_turn, x_c, y_c, -1, 1, jumps, is_King)
                    count += 1
            if is_King:
                if (x_c + 2) in valid_positions and (y_c - 2) in valid_positions:
                    if new_board.grid[y_c - 1][x_c + 1] in valid_red and new_board.grid[y_c - 2][x_c + 2] == empty_slot:
                        jumps = new_board.jump_finder(red_turn, x_c, y_c, 1, -1, jumps, is_King)
                        count += 1
                
                if (x_c - 2) in valid_positions and (y_c - 2) in valid_positions:
                    if new_board.grid[y_c - 1][x_c - 1] in valid_red and new_board.grid[y_c - 2][x_c - 2] == empty_slot:
                        jumps = new_board.jump_finder(red_turn, x_c, y_c, -1, -1, jumps, is_King)
                        count += 1
            if count == 0:
                jumps.append(new_board)
                return jumps
        else:
            if (x_c + 2) in valid_positions and (y_c - 2) in valid_positions:
                if new_board.grid[y_c - 1][x_c + 1] in valid_black and new_board.grid[y_c - 2][x_c + 2] == empty_slot:
                    jumps = new_board.jump_finder(red_turn, x_c, y_c, 1, -1, jumps, is_King)
                    count += 1
            if (x_c - 2) in valid_positions and (y_c - 2) in valid_positions:
                if new_board.grid[y_c - 1][x_c - 1] in valid_black and new_board.grid[y_c - 2][x_c - 2] == empty_slot:
                    jumps = new_board.jump_finder(red_turn, x_c, y_c, -1, -1, jumps, is_King)
                    count += 1
            if is_King:
                if (x_c + 2) in valid_positions and (y_c + 2) in valid_positions:
                    if self.grid[y_c + 1][x_c + 1] in valid_black and self.grid[y_c + 2][x_c + 2] == empty_slot:
                        jumps = new_board.jump_finder(red_turn, x_c, y_c, 1, 1, jumps, is_King)
                        count += 1   
                if (x_c - 2) in valid_positions and (y_c + 2) in valid_positions:
                    if new_board.grid[y_c + 1][x_c - 1] in valid_black and new_board.grid[y_c + 2][x_c - 2] == empty_slot:
                        jumps = new_board.jump_finder(red_turn, x_c, y_c, -1, 1, jumps, is_King)
                        count += 1
            if count == 0:
                jumps.append(new_board) 
                return jumps 

        return jumps
    
    def delete(self, x_coord, y_coord, x_change, y_change):
        del_x = x_coord + x_change
        del_y = y_coord + y_change
        
        for piece in self.pieces:
            if piece.coord_x == del_x and piece.coord_y == del_y:
                self.pieces.remove(piece)
                break
        self.__construct_grid()

    def move(self, x_coord, y_coord, x_change, y_change, jump, red_turn, is_King):
        """
        - Need to delete captured pieces from self.pieces
        - Need to move piece to final location
        - Need to update it to King if necessary
        """
        #Find the piece that you want to move based on the x and y coordinate 
        multiplier = 1
        if jump:
            multiplier = 2
            self.delete(x_coord, y_coord, x_change, y_change)
        for piece in self.pieces:
            if piece.coord_x == x_coord and piece.coord_y == y_coord:
                piece.coord_y += multiplier * y_change
                new_height = piece.coord_y
                piece.coord_x += multiplier * x_change
                break
        if red_turn and not is_King and new_height == 0:
            piece.is_king = True
            self.__construct_grid()
            return (self, True)
        if not red_turn and not is_King and new_height == 7:
            piece.is_king = True
            self.__construct_grid()
            return (self, True)
        self.__construct_grid()
        return (self, False)

    def pieces_check_end_game(self):
        black_piece_on_board = False
        red_piece_on_board = False
        for piece in self.pieces:
            if piece.is_red:
                red_piece_on_board = True
            else:
                black_piece_on_board = True
        return not (red_piece_on_board and black_piece_on_board)
    
    def red_pieces_on_board(self):
        red_piece_on_board = False
        for piece in self.pieces:
            if piece.is_red:
                red_piece_on_board = True
        return red_piece_on_board
    
    def black_pieces_on_board(self):
        black_piece_on_board = False
        for piece in self.pieces:
            if not piece.is_red:
                black_piece_on_board = True
        return black_piece_on_board
    
    def opponent_distance(self, x_c, y_c, red):
        if red:
            return self.closest_black(x_c, y_c)
        else:
            return self.closest_red(x_c, y_c)

    def closest_black(self, x_c, y_c):
        minimum = utility
        for piece in self.pieces:
            if not piece.is_red:
                distance = abs(x_c - piece.coord_x) + abs(y_c - piece.coord_y)
                if distance < minimum:
                    minimum = distance
        return minimum

    def closest_red(self, x_c, y_c):
        minimum = utility
        for piece in self.pieces:
            if piece.is_red:
                distance = abs(x_c - piece.coord_x) + abs(y_c - piece.coord_y)
                if distance < minimum:
                    minimum = distance
        return minimum


    def find_avg_distance_red(self):
        distance_sum = 0
        piece_count = 0
        for piece in self.pieces:
            if piece.is_red:
                distance_sum += self.opponent_distance(piece.coord_x, piece.coord_y, True)
                piece_count += 1
        return distance_sum/piece_count
    
    def find_avg_distance_black(self):
        distance_sum = 0
        piece_count = 0
        for piece in self.pieces:
            if not piece.is_red:
                distance_sum += self.opponent_distance(piece.coord_x, piece.coord_y, False)
                piece_count += 1
        return distance_sum/piece_count
    
    def evaluation_fcn(self):
        '''More advanced features to add later:
        1. Better to have pieces further up on the board (Done)
        2. Better to have pieces in centre of board (Done)
        3. Pieces that can't be captured are better
        4. Number of moves both players can make
        5. Extra point if checker on home line
        6. Attack on double corner side
        7. Better if you have more moves available then opponent

        '''

        eval = 0
        if not self.red_pieces_on_board:
            return neg_utility
        if not self.black_pieces_on_board:
            return utility
        red = 0
        black = 0
        for piece in self.pieces:
            if piece.is_red:
                red += 1
                if (piece.coord_x, piece.coord_y) in centre_slots:
                    eval += 0.25
                if piece.is_king:
                    eval += 1.5
                else:
                    advancement = (7 - piece.coord_y)/14
                    eval += 1 + advancement
                if piece.coord_x == 0 or piece.coord_y == 0 or piece.coord_x == 7:
                    eval += 0.01
                if piece.coord_x == 7:
                    eval += 0.25
            else:
                black += 1
                if (piece.coord_x, piece.coord_y) in centre_slots:
                    eval -= 0.25
                if piece.is_king:
                    eval -= 1.5
                else:
                    advancement = piece.coord_y/14
                    eval -= (1 + advancement)
                if piece.coord_x == 7 or piece.coord_y == 0 or piece.coord_x == 7:
                    eval -= 0.01
                if piece.coord_x == 0:
                    eval -= 0.25
        if red>black:
            #Want to move closer to opponent
            self.find_avg_distance_red()
        elif black>red:
            self.find_avg_distance_black()
            eval += 0
        else:
            pass

        return eval

        

class State:
    """
    State class wrapping a Board with some extra current state information.
    Note that State and Board are different. Board has the locations of the pieces. 
    State has a Board and some extra information that is relevant to the search: 
    heuristic function, f value, current depth and parent.
    """

    def __init__(self, board, parent=None, red_turn = True):
        """
        :param board: The board of the state.
        :type board: Board
        :param parent: The parent of current state.
        :type parent: Optional[State]
        """
        self.board = board
        self.parent = parent
        self.red_turn = red_turn
    
    def move_finder(self):
        #Steps
        '''
        1. Find all piece coordinates
        2. For all kings (first list) find all possible moves
                a)Check up right move with function if in bounds
                b)Check up left move with function if in bounds
                c)Check down right move if in bounds with a function
                d)Check down left move if in bounds with a function
        3. For all basic pieces (second list) find all possible moves
                if red:
                    a) Check up (forward) right move
                    b) Check up (forward) left move
                if black:
                    a) Check down (forward) right move
                    b) Check down (forward) left move
        4. With all moves, create the tree by calling alpha-beta pruning decisons with jump moves if it is available or regular moves if no jump moves
            a) This tree should find the path to take or at least move to make
            b) OPTIONAL: Implement node ordering/state caching at end if you have time
        5. With this move, call the move function in board to update the board
        6. Switch turns by setting red_turn to not red_turn

        returns:
        Jump moves with True if there are possible jump moves
        Regular moves with False if there are no jump moves 
                
        '''
        piece_coord = []
        piece_coord = self.board.pieces_on_board(self.red_turn)
        jump_moves = [] #list of new states
        regular_moves = [] #List of new states 
        for piece_loc in piece_coord[0]: ##Locations of the Kings
            (x_coord, y_coord) = piece_loc
            (jump_moves, regular_moves) = self.board.up_right_move_check(self.red_turn, x_coord, y_coord,jump_moves,regular_moves, True)
            (jump_moves, regular_moves) = self.board.up_left_move_check(self.red_turn, x_coord, y_coord,jump_moves,regular_moves, True)
            (jump_moves, regular_moves) = self.board.down_right_move_check(self.red_turn, x_coord, y_coord,jump_moves,regular_moves, True)
            (jump_moves, regular_moves) = self.board.down_left_move_check(self.red_turn, x_coord, y_coord,jump_moves,regular_moves, True)
        for piece_loc in piece_coord[1]:
            (x_coord, y_coord) = piece_loc
            if self.red_turn:
                (jump_moves, regular_moves) = self.board.up_right_move_check(self.red_turn, x_coord, y_coord,jump_moves,regular_moves, False)
                (jump_moves, regular_moves) = self.board.up_left_move_check(self.red_turn, x_coord, y_coord,jump_moves,regular_moves, False)
            else:
                (jump_moves, regular_moves) = self.board.down_right_move_check(self.red_turn, x_coord, y_coord,jump_moves,regular_moves, False)
                (jump_moves, regular_moves) = self.board.down_left_move_check(self.red_turn, x_coord, y_coord,jump_moves,regular_moves, False)
 
        if len(jump_moves) == 0:
            return (regular_moves, False)  
        else:
            return (jump_moves, True)

    def alpha_beta_prune(self):
        (moves, jumping) = self.move_finder()
        if len(moves) == 0:
            stalemate = True
            return self
        if self.red_turn:
            optimal_state = self.MAX_VALUE(float('-inf'), float('inf'), 1)[0]
        else:
            optimal_state = self.MIN_VALUE(float('-inf'), float('inf'), 1)[0]
        next_state = State(optimal_state.board, self, not self.red_turn)
        return next_state
    
    def MAX_VALUE(self, alpha, beta, depth):
        if depth == depth_limit or self.board.pieces_check_end_game():
            return (None, self.board.evaluation_fcn())
        v = float('-inf')
        moves = self.move_finder()[0]
        pq = []
        heapq.heapify(pq)
        for move in moves:
            heappush(pq, (move.evaluation_fcn() * -1, hash(move), move))
        #sort moves based on evals from max to min
        while len(pq) > 0:
            action = heapq.heappop(pq)[2]
        # for action in moves:
            new_state = State(action, None, not self.red_turn)
            min_val = new_state.MIN_VALUE(alpha, beta, depth + 1)[1]
            if v < min_val:
                v = min_val
                best_state = new_state
            if v >= beta:
                return (None, v)
            alpha = max(alpha, v)
        if depth == 1:
            return (best_state, v)
        return (None, v)
    
    def MIN_VALUE(self, alpha, beta, depth):
        if depth == depth_limit or self.board.pieces_check_end_game():
            return (None, self.board.evaluation_fcn())
        v = float('inf')
        moves = self.move_finder()[0]
        #sort moves based on evals
        pq = []
        heapq.heapify(pq)
        for move in moves:
            heappush(pq, (move.evaluation_fcn(), hash(move), move))
        #sort moves based on evals from max to min
        while len(pq) > 0:
            action = heapq.heappop(pq)[2]
        # for action in moves:
            new_state = State(action, None, not self.red_turn)
            max_val = new_state.MAX_VALUE(alpha, beta, depth + 1)[1]
            if v > max_val:
                v = max_val
                best_state = new_state
            if v <= alpha:
                return (None, v)
            beta = min(beta, v)
        if depth == 1:
            return (best_state, v)
        return (None, v)

    def output(self, state, file):
        """
        Prints all parents of a current state to a file.

        :param state: The current state of which we are printing its parents.
        :type filename: State class
        :param file: The name of the given file to print the moves.
        :type filename: str
        :return: Nothing
        :rtype: None
        """

        output_file = open(file, "w")
        # output_file.write("Depth: ")
        # output_file.write(str(state.f))
        # output_file.write("\n\n")
        path = []
        while state != None:
            path.insert(0, state.board.grid)
            state = state.parent
        for step in path:
            for i in range(self.board.height):
                for j in range(self.board.width):
                    output_file.write(step[i][j])
                output_file.write("\n")
            output_file.write("\n")
    
    # def print_board(self):
    #     for i in range(self.board.height):
    #         print(self.board.grid[i])
    #     print('\n')


def read_from_file(filename):
    """
    Load initial board from a given file.

    :param filename: The name of the given file.
    :type filename: str
    :return: A loaded board
    :rtype: Board
    """

    puzzle_file = open(filename, "r")

    line_index = 0
    pieces = []
    
    for line in puzzle_file:

        for x, ch in enumerate(line):

            if ch == char_red_king: # found vertical piece
                pieces.append(Piece(True, True, x, line_index))
            elif ch == char_red_basic: # found horizontal piece
                pieces.append(Piece(True, False, x, line_index))
            elif ch == char_black_king:
                pieces.append(Piece(False, True, x, line_index))
            elif ch == char_black_basic:
                pieces.append(Piece(False, False, x, line_index))
        line_index += 1

    puzzle_file.close()

    board = Board(pieces)
    
    return board

def read_from_input(board_grid):
    """
    Load initial board from a given file.

    :param filename: The name of the given file.
    :type filename: str
    :return: A loaded board
    :rtype: Board
    """

    line_index = 0
    pieces = []
    
    for line in board_grid:

        for x, ch in enumerate(line):

            if ch == char_red_king: # found vertical piece
                pieces.append(Piece(True, True, x, line_index))
            elif ch == char_red_basic: # found horizontal piece
                pieces.append(Piece(True, False, x, line_index))
            elif ch == char_black_king:
                pieces.append(Piece(False, True, x, line_index))
            elif ch == char_black_basic:
                pieces.append(Piece(False, False, x, line_index))
        line_index += 1

    board = Board(pieces)
    
    return board



def checkers_solve(state, output_filename):
    while not state.board.pieces_check_end_game() and not stalemate:
        state = state.alpha_beta_prune()
    state.output(state, output_filename)
    return



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzle."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    board = read_from_file(args.inputfile)
    starting_state = State(board)

    
    checkers_solve(starting_state, args.outputfile)

    # #Debugging
    # board = [
    #             ['.', '.', '.', '.', '.', 'b', '.', 'B'],
    #             ['.', '.', 'R', '.', 'R', '.', 'r', '.'],
    #             ['.', '.', '.', '.', '.', 'R', '.', 'r'],
    #             ['.', '.', '.', '.', '.', '.', '.', '.'],
    #             ['.', '.', '.', '.', '.', 'R', '.', 'B'],
    #             ['.', '.', 'R', '.', '.', '.', 'B', '.'],
    #             ['.', '.', '.', 'r', '.', 'r', '.', '.'],
    #             ['.', '.', '.', '.', 'B', '.', '.', '.']]
    # acc_board = read_from_input(board)
    # # acc_board.evaluation_fcn()
    # starting_state = State(acc_board)

    
    # checkers_solve(starting_state, 'output.txt')
    
