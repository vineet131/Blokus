import numpy as np
import constants, pieces

empty = constants.BOARD_FILL_VALUE
rows = constants.ROW_COUNT
cols = constants.COLUMN_COUNT

class Board:

    def __init__(self):
        self.board = np.array([[empty for i in range(rows)] for j in range(cols)])
        self.turn_number = 1
    
    #Fit a given piece at a given position on the board
    #For human player: We pass the player.current_piece as the piece parameter
    #For AI: We pass one move from the dict returned by return_all_pending_moves
    #        or a dict in a similar format as the piece parameter
    def fit_piece(self, piece, player, opponent_player):
        piece_x_rng = range(piece["arr"].shape[0])
        piece_y_rng = range(piece["arr"].shape[1])
        board_x_rng = range(piece["place_on_board_at"][0], rows)
        board_y_rng = range(piece["place_on_board_at"][1], cols)
        
        if player.is_1st_move:
            if player.number == constants.PLAYER1_VALUE:
                pos = constants.STARTING_PTS["player1"]
            elif player.number == constants.PLAYER2_VALUE:
                pos = constants.STARTING_PTS["player2"]
            
            is_within_starting_pos = False
            for _, x in zip(piece_x_rng, board_x_rng):
                for _, y in zip(piece_y_rng, board_y_rng):
                    if [x, y] == pos:
                        is_within_starting_pos = True
            if is_within_starting_pos:
                for i, x in zip(piece_x_rng, board_x_rng):
                    for j, y in zip(piece_y_rng, board_y_rng):
                        if piece["arr"][i][j] == 1 and self.board[x][y] == empty:
                            self.board[x][y] = player.number * piece["arr"][i][j]
            else:
                if constants.VERBOSITY > 0:
                    print("Could not fit piece in starting position in 1st move")
                return False
            player.is_1st_move = False
        else:
            if self.check_is_move_valid(piece["arr"], player, piece["place_on_board_at"]):
                for i, x in zip(piece_x_rng, board_x_rng):
                    for j, y in zip(piece_y_rng, board_y_rng):
                        if piece["arr"][i][j] == 1:
                            self.board[x][y] = player.number * piece["arr"][i][j]
            else:
                if constants.VERBOSITY > 0:
                    print("In fit_piece, move turned out to be invalid")
                    print(piece)
                return False
        
        pieces.discard_piece(piece["piece"], player)
        player.empty_current_piece()
        self.turn_number += 1
        player.turn_number += 1
        player.update_score()
        if constants.VERBOSITY > 0:
            print("At turn number", self.turn_number, "board is:", "\n", self.board)
            print("Current player's score is:", player.score, "and opponent's score is", opponent_player.score)
        self.update_board_corners(player, opponent_player)
        return True
    
    """We check the corners of a certain coordinate on the board as such:
    tl   0   tr
    0  (x,y) 0
    bl   0   br
    """
    def update_board_corners(self, player, opponent_player):
        #Updates the available corners for each player. For that, we need to empty
        #the corners first
        player.board_corners = {"bl":[],"br":[],"tl":[],"tr":[]}
        opponent_player.board_corners = {"bl":[],"br":[],"tl":[],"tr":[]}
        for p in [player, opponent_player]:
            for x in range(self.board.shape[0]):
                for y in range(self.board.shape[1]):
                    if self.board[x][y] == p.number:
                        tl, tr, bl, br = self.check_surrounding_piece_coords(x, y)
                        if tl and x-1 >= 0 and y-1 >= 0:
                            p.board_corners["tl"].append([x-1, y-1])
                        if bl and x+1 < rows and y-1 >= 0:
                            p.board_corners["bl"].append([x+1, y-1])
                        if tr and x-1 >= 0 and y+1 < cols:
                            p.board_corners["tr"].append([x-1, y+1])
                        if br and x+1 < rows and y+1 < cols:
                            p.board_corners["br"].append([x+1,y+1])
        if constants.VERBOSITY > 0:
            print("Board corners for current player:", player.board_corners)
            print("Board corners for opponent player:", opponent_player.board_corners)
    
    def check_surrounding_piece_coords(self, x, y):
        tl, tr, bl, br = True, True, True, True
        #Remember, for arrays, negative indexes are permissible, which we need to avoid
        try:
            if self.board[x+1][y] != empty: bl, br = False, False
        except IndexError: bl, br = False, False
        try:
            if self.board[x+1][y+1] != empty: br = False
        except IndexError: br = False
        try:
            if self.board[x][y+1] != empty: tr, br = False, False
        except IndexError: tr, br = False, False
        try:
            if x-1 >= 0 and self.board[x-1][y+1] != empty: tr = False
        except IndexError: tr = False
        try:
            if x-1 >= 0 and self.board[x-1][y] != empty: tl, tr = False, False
        except IndexError: tl, tr = False, False
        try:
            if x-1 >= 0 and y-1 >= 0 and self.board[x-1][y-1] != empty: tl = False
        except IndexError: tl = False
        try:
            if y-1 >= 0 and self.board[x][y-1] != empty: tl, bl = False, False
        except IndexError: tl, bl = False, False
        try:
            if y-1 >= 0 and self.board[x+1][y-1] != empty: bl = False
        except IndexError: bl = False
        return tl, tr, bl, br
    
    """Piece is the array of the piece being placed
    Board is the array of the current state of the board
    player is the player making the move
    coords are the coordinates of the top left corner of the array of the move being made
    
    Check if, for a given piece and board coords, if the move is valid"""
    def check_is_move_valid(self, piece_arr, player, coords):
        is_there_a_pc_on_the_side = False
        is_corner_exists = False
        
        piece_x_rng = range(piece_arr.shape[0])
        piece_y_rng = range(piece_arr.shape[1])
        board_x_rng = range(coords[0], rows)
        board_y_rng = range(coords[1], cols)
        #1. Check if pc lies inside board
        if piece_arr.shape[0] + coords[0] > rows\
           or piece_arr.shape[1] + coords[1] > cols:
           return False

        for i, x in zip(piece_x_rng, board_x_rng):
            for j, y in zip(piece_y_rng, board_y_rng):
                #2. Check if pc is placed on empty squares
                if piece_arr[i][j] == 1 and self.board[x][y] == empty:
                    tl, tr, bl, br = get_corners_of_piece(piece_arr, i, j)
                    #3. Check if pc has a board corner
                    for p, b in zip([tl,tr,bl,br],["br","bl","tr","tl"]):
                        if p:
                            if [x, y] in player.board_corners[b]:
                                is_corner_exists = True
                    #4. Check if no squares already placed on board by player
                    #are on the side of pc being placed (only corner, no left or right)
                    for a, b in zip([x, x, x-1, x+1], [y-1, y+1, y, y]):
                        if a < 0 or b < 0 or a >= rows or b >= cols:
                            pass
                        else:
                            if self.board[a][b] == player.number:
                                is_there_a_pc_on_the_side = True
                elif piece_arr[i][j] == 1 and self.board[x][y] != empty:
                    return False
        if is_corner_exists and not is_there_a_pc_on_the_side:
            return True
        return False
    
    def validate_and_return_move_positions(self, piece_arr, player):
        place_on_board_at = []
        for x in range(self.board.shape[0] - piece_arr.shape[0]):
            for y in range(self.board.shape[1] - piece_arr.shape[1]):
                if self.board[x][y] == empty:
                    if self.check_is_move_valid(piece_arr, player, [x,y]):
                        place_on_board_at.append([x,y])
        return place_on_board_at

#For 1 unit square of a given piece, we check to see which corners are empty
def get_corners_of_piece(piece_arr, i, j):
    tl, tr, bl, br = True, True, True, True
    x_lim, y_lim = piece_arr.shape[0], piece_arr.shape[1]
    try:
        if i+1 < x_lim and piece_arr[i+1][j] == 1: bl, br = False, False
    except IndexError: pass
    try:
        if i+1 < x_lim and j+1 < y_lim and piece_arr[i+1][j+1] == 1: br = False
    except IndexError: pass
    try:
        if j+1 < y_lim and piece_arr[i][j+1] == 1: tr, br = False, False
    except IndexError: pass
    try:
        if i-1 >= 0 and j+1 < y_lim and piece_arr[i-1][j+1] == 1: tr = False
    except IndexError: pass
    try:
        if i-1 >= 0 and piece_arr[i-1][j] == 1: tl, tr = False, False
    except IndexError: pass
    try:
        if i-1 >= 0 and j-1 >=0 and piece_arr[i-1][j-1] == 1: tl = False
    except IndexError: pass
    try:
        if j-1 >=0 and piece_arr[i][j-1] == 1: tl, bl = False, False
    except IndexError: pass
    try:
        if i+1 < x_lim and j-1 >=0 and piece_arr[i+1][j-1] == 1: bl = False
    except IndexError: pass
    return tl, tr, bl, br

#For AIs, we get a list of all the possible remaining moves. To do this,
#we get all possible poiece configurations and match them to all the corners
#available on the board
def return_all_pending_moves(gameboard, player, mode = "ai"):
    pending_moves_list = []

    #Iterate over that dictionary of remaining pieces
    for current_piece in pieces.get_all_piece_states(player):
        #Get the corners of 1 unit sq in current piece configuration
        board_positions = gameboard.validate_and_return_move_positions(current_piece["arr"], player)
        for pos in board_positions:
            pending_moves_list.append({"piece": current_piece["piece"], "flipped": current_piece["flipped"],\
                        "arr": current_piece["arr"], "rotated": current_piece["rotated"], "place_on_board_at": pos})
            #If we just want to check if the game is over or not, we dont need to iterate every possibility.
            #Even if a single move is present, the game ain't over yet
            if mode == "is_game_over" and len(pending_moves_list) > 0:
                return pending_moves_list
    if constants.VERBOSITY > 0:
        msg = "Pending moves are"+str(pending_moves_list)
        print("Number of pending moves:", len(pending_moves_list))
        #constants.write_to_log(msg)
    return pending_moves_list

def is_game_over(board, player1, player2):
    #Just started the game, how can it be over so soon?
    if player1.is_1st_move or player2.is_1st_move:
        return False
    #If there are no more remaining pieces, game over
    if not player1.remaining_pieces and not player2.remaining_pieces:
        return True
    #If there are no more possible moves for both players, game over
    if len(return_all_pending_moves(board, player1, "is_game_over")) == 0 and \
       len(return_all_pending_moves(board, player2, "is_game_over")) == 0:
        return True
    return False

#Scoring is based on the official rules of the game. For details,
#refer to the manual in the main directory
def scoring_fn(remaining_pieces):
    score = constants.STARTING_SCORE
    if len(remaining_pieces) == 0:
        score = score + 15
    else:
        for key in remaining_pieces.keys():
            piece = remaining_pieces[key]["arr"]
            for i in range(piece.shape[0]):
                for j in range(piece.shape[1]):
                    if piece[i][j] == 1: #1 means 1 unit sq of that piece
                        score = score - 1
    # If the last pc played is the 1 unit sq pc, we get extra 5 pts
    if len(remaining_pieces) == 1 and "piece1" in remaining_pieces \
       and score == 88:
        score = score + 5
    return score