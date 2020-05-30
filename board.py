import numpy as np, constants, pieces

empty = constants.BOARD_FILL_VALUE
rows = constants.ROW_COUNT
cols = constants.COLUMN_COUNT
class Board:

    def __init__(self):
        self.board = np.array([[empty for i in range(rows)] for j in range(cols)])
        self.turn_number = 0
        #Useful for AIs
        self.board_copy = []
    
    #Fit a given piece at a given position on the board
    def fit_piece(self, piece, coords, player, opponent_player):
        x, y = coords[0], coords[1]
        
        if player.is_1st_move:
            if player.number == constants.PLAYER1_VALUE:
                pos = constants.STARTING_PTS["player1"]
            elif player.number == constants.PLAYER2_VALUE:
                pos = constants.STARTING_PTS["player2"]
            
            is_within_starting_pos = False
            for i in range(piece.shape[0]):
                for j in range(piece.shape[1]):
                    if piece[i][j] == 1 and self.board[x][y] == empty:
                        self.board[x][y] = player.number * piece[i][j]
                    if (x, y) == pos:
                        is_within_starting_pos = True
                    y += 1
                x += 1
                y = coords[1]
            if not is_within_starting_pos:
                return False
            player.is_1st_move = False
        else:
            if check_is_move_valid(piece, coords):
                for i in range(piece.shape[0]):
                    for j in range(piece.shape[1]):
                        if piece[i][j] == 1:
                            self.board[x][y] = player.number * piece[i][j]
                        y += 1
                    x += 1
                    y = coords[1]
            else:
                return False
        
        pieces.discard_piece(piece, player)
        player.empty_current_piece()
        update_board_corners(player, opponent_player)
        self.turn_number += 1
        player.update_score()
        if constants.VERBOSITY > 0:
            print("At turn number",self.turn_number,"board is:","\n",self.board)
        return True
    
    """We check the corners of a certain coordinate on the board as such:
    tl   0   tr
    0  (i,j) 0
    bl   0   br
    """
    def update_board_corners(self, player, opponent_player):
        #Updates the available corners for each player. For that, we need to empty
        #the corners first
        player.board_corners = {"bl":[],"br":[],"tl":[],"tr":[]}
        opponent_player.board_corners = {"bl":[],"br":[],"tl":[],"tr":[]}
        for p in [player, opponent_player]:
            for i in range(self.board.shape[0]):
                for j in range(self.board.shape[1]):
                    if self.board[i][j] == p.number:
                        tl, tr, bl, br = check_surrounding_piece_coords(i, j)
                        if tl:
                            p.board_corners["tl"].append([i-1,j-1])
                        if bl:
                            p.board_corners["bl"].append([i+1,j-1])
                        if tr:
                            p.board_corners["tr"].append([i-1,j+1])
                        if br:
                            p.board_corners["br"].append([i+1,j+1])
    
    def check_surrounding_piece_coords(self, i, j):
        tl, tr, bl, br = True, True, True, True
        if i+1 > rows or self.board[i+1][j] != empty:
            bl, br = False, False
        if i+1 > rows or j+1 > cols or self.board[i+1][j+1] != empty:
            br = False
        if j+1 > cols or self.board[i][j+1] != empty:
            tr, br = False, False
        if i-1 < 0 or j+1 > cols or self.board[i-1][j+1] != empty:
            tr = False
        if i-1 < 0 or self.board[i-1][j] != empty:
            tl, tr = False, False
        if i-1 < 0 or j-1 < 0 or self.board[i-1][j-1] != empty:
            tl = False
        if j-1 < 0 or self.board[i][j-1] != empty:
            tl, bl = False, False
        if i+1 > rows or j-1 < 0 or self.board[i+1][j-1] != empty:
            bl = False
        return tl, tr, bl, br
    
    #Piece is the array of the piece being placed
    #Board is the array of the current state of the board
    #player is the player making the move
    #coords are the coordinates of the top left corner of the array of the move being made
    def check_is_move_valid(self, piece, player, coords):
        is_allowed = False
        is_corner_exists = False
        i, j = 0, 0
        x, y = coords[0], coords[1]
        for i in range(piece.shape[0]):
            for j in range(piece.shape[1]):
                if piece[i][j] == 1 and board[x][y] == empty:
                    tl, tr, bl, br = get_corners_of_piece(piece, i, j)
                    if tl:
                        if (x+1, y+1) in player.board_corners["br"]:
                            is_corner_exists = True
                    if bl:
                        if (x-1, y+1) in player.board_corners["tr"]:
                            is_corner_exists = True
                    if tr:
                        if (x+1, y-1) in player.board_corners["bl"]:
                            is_corner_exists = True
                    if br:
                        if (x-1, y-1) in player.board_corners["tl"]:
                            is_corner_exists = True
                elif piece[i][j] == 1 and board[x][y] != empty:
                    return False
        if is_corner_exists:
            is_allowed = True
        return is_allowed
    
    #Copy the board state and the player state. Useful for AIs like Minimax
    def retain_board(self, ai_player, opponent_player):
        self.board_copy = self.board
        self.player1_corners_copy = self.player1_corners
        self.player2_corners_copy = self.player2_corners
        ai_player.remaining_pieces_copy = ai_player.remaining_pieces
        opponent_player.remaining_pieces_copy = opponent_player.remaining_pieces
        ai_player.discarded_pieces_copy = ai_player.discarded_pieces
        opponent_player.discarded_pieces_copy = opponent_player.discarded_pieces

   #Restore the board and player state properties. Useful for AIs like Minimax 
    def restore_board(self, ai_player, opponent_player):
        self.board = self.board_copy
        self.player1_corners = self.player1_corners_copy
        self.player2_corners = self.player2_corners_copy
        ai_player.remaining_pieces = ai_player.remaining_pieces_copy
        opponent_player.remaining_pieces = opponent_player.remaining_pieces_copy
        ai_player.discarded_pieces = ai_player.discarded_pieces_copy
        opponent_player.discarded_pieces = opponent_player.discarded_pieces_copy

def get_corners_of_piece(piece, i, j):
    tl, tr, bl, br = True, True, True, True
    x_lim, y_lim = piece.shape[0], piece.shape[1]
    if i+1 > x_lim or piece[i+1][j] != empty:
        bl, br = False, False
    if i+1 > x_lim or j+1 > y_lim or piece[i+1][j+1] != empty:
        br = False
    if j+1 > y_lim or piece[i][j+1] != empty:
        tr, br = False, False
    if i-1 < 0 or j+1 > y_lim or piece[i-1][j+1] != empty:
        tr = False
    if i-1 < 0 or piece[i-1][j] != empty:
       tl, tr = False, False
    if i-1 < 0 or j-1 < 0 or piece[i-1][j-1] != empty:
        tl = False
    if j-1 < 0 or piece[i][j-1] != empty:
        tl, bl = False, False
    if i+1 > x_lim or j-1 < 0 or piece[i+1][j-1] != empty:
        bl = False
    return tl, tr, bl, br

#For AIs, we get a list of all the possible remaining moves. To do this,
#we get all possible poiece configurations and match them to all the corners
#available on the board
def return_all_pending_moves(board, player):
    pending_moves_list = []

    #Take the dictionary of remaining pieces
    pieces = player.remaining_pieces
    #Iterate over that dictionary of remaining pieces
    for piece in pieces.keys():
        current_piece = pieces[piece]["arr"]
        #Iterate over number of possible flips for each piece
        for flip in range(pieces[piece]["flips"] - 1):
            if flip > 0:
                current_piece = np.flipud(current_piece)
            #Iterate over number of possible rotations for each piece
            for rot in range(pieces[piece]["rots"] - 1):
                current_piece = np.rot90(current_piece, k = rot)
                #Get the corners of current piece configuration
                for i in range(current_piece.shape[0]):
                    for j in range(current_piece.shape[1]):
                        tl, tr, bl, br = get_corners_of_piece(current_piece, i, j)
                        if tl and len(player.board_corners["br"]) > 0:
                            pending_moves_list.append({"piece": piece, "flipped": flip,
                                "rotated": rot, "join_at": [i,j], "board_corner": "br"})
                        if tr and len(player.board_corners["bl"]) > 0:
                            pending_moves_list.append({"piece": piece, "flipped": flip,
                                "rotated": rot, "join_at": [i,j], "board_corner": "bl"})
                        if bl and len(player.board_corners["tr"]) > 0:
                            pending_moves_list.append({"piece": piece, "flipped": flip,
                                "rotated": rot, "join_at": [i,j], "board_corner": "tr"})
                        if br and len(player.board_corners["tl"]) > 0:
                            pending_moves_list.append({"piece": piece, "flipped": flip,
                                "rotated": rot, "join_at": [i,j], "board_corner": "tl"})
    return pending_moves_list

def is_game_over(board, player1, player2):
    #Just started the game, how can it be over so soon?
    if player1.is_1st_move or player2.is_1st_move:
        return False
    #If there are no more remaining pieces, game over
    if not player1.remaining_pieces and not player2.remaining_pieces:
        return True
    #If there are no more possible moves for both players, game over
    if len(return_all_pending_moves(board, player1)) == 0 and \
       len(return_all_pending_moves(board, player2)) == 0:
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
    if len(remaining_pieces) == 1 and "piece1" in remaining_pieces
       and score == 88:
        score = score + 5
    return score