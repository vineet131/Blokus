import copy, random, constants, numpy as np
from board import scoring_fn, return_all_pending_moves

def main(gameboard, ai_player, opponent_player):
    best_score = constants.M_INFINITY
    best_move = None

    if ai_player.is_1st_move:
        best_move = do_first_move(ai_player)
    else:
        board = copy.deepcopy(gameboard)
        ai_copy = copy.deepcopy(ai_player)
        opponent_copy = copy.deepcopy(opponent_player)

        for move in return_all_pending_moves(ai_copy):
            board.retain_board(ai_copy, opponent_copy)
            if board.fit_piece(move, ai_copy, opponent_copy):
                score = do_minimax(constants.INFINITY, constants.M_INFINITY, board, \
                                   ai_copy, opponent_copy, False)
                board.restore_board(ai_copy, opponent_copy)
                if score > best_score:
                    best_score = score
                    best_move = move
    return best_move

def do_first_move(player):
    pieces = list(player.remaining_pieces.keys())
    #Lets not use the 1x1 piece in the beginning
    pieces.remove("piece1")
    piece = random.choice(pieces)
    if constants.VERBOSITY > 0:
        print("MinimaxAI chooses piece: ", piece)
    
    piece_arr = player.remaining_pieces[piece]["arr"]

    flips = player.remaining_pieces[piece]["flips"]
    flip = random.choice(range(flips))
    
    rots = player.remaining_pieces[piece]["rots"]
    rot = random.choice(range(rots))
    
    if player.number == 1:
        start_x, start_y = constants.STARTING_PTS["player1"]
    elif player.number == 2:
        start_x, start_y = constants.STARTING_PTS["player2"]
    
    piece_arr = np.rot90(piece_arr, k = rot)
    if flip == 1:
        piece_arr = np.flipud(piece_arr)
    
    choice_x = random.choice(range(piece_arr.shape[0]))
    choice_y = random.choice(range(piece_arr.shape[1]))
    #The unit sq randomly selected for the piece must be a valid unit sq 
    while piece_arr[choice_x][choice_y] != 1:
        choice_x = random.choice(range(piece_arr.shape[0]))
        choice_y = random.choice(range(piece_arr.shape[1]))
    board_x = start_x - choice_x
    board_y = start_y - choice_y

    first_move = {"piece" : piece, "arr" : piece_arr, "rotated" : rot, "flipped" : flip, \
                "place_on_board_at" : [board_x, board_y]}
    if constants.VERBOSITY > 0:
        print("Chosen first move for MinimaxAI:", first_move)
    return first_move

def do_minimax(alpha, beta, board, ai_player, opponent_player, \
               maximizing_player, depth = 3):
    
    if maximizing_player:
        if depth == 0 or len(return_all_pending_moves(ai_player)) == 0:
            return scoring_fn(ai_player.remaining_pieces)
        
        return get_max(alpha, beta, board, ai_player, opponent_player, depth)
    
    else:
        if depth == 0 or len(return_all_pending_moves(opponent_player)) == 0:
            return scoring_fn(opponent_player.remaining_pieces)

        return get_min(alpha, beta, board, ai_player, opponent_player, depth)

def get_max(alpha, beta, board, ai_player, opponent_player, depth):
    max_eval = constants.M_INFINITY
    ai_moves = return_all_pending_moves(ai_player)

    for move in ai_moves:
        board.retain_board(ai_player, opponent_player)
        if board.fit_piece(move, ai_player, opponent_player):
            eval = do_minimax(alpha, beta, board, ai_player, \
                              opponent_player, False, depth - 1)
            board.restore_board(ai_player, opponent_player)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
    return max_eval

def get_min(alpha, beta, board, ai_player, opponent_player, depth):
    min_eval = constants.INFINITY
    player_moves = return_all_pending_moves(opponent_player)

    for move in player_moves:
        board.retain_board(ai_player, opponent_player)
        if board.fit_piece(move, opponent_player, ai_player):
            eval = do_minimax(alpha, beta, board, ai_player, \
                              opponent_player, True, depth - 1)
            board.restore_board(ai_player, opponent_player)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
    return min_eval