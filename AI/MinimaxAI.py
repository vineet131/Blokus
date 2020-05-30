import copy, random
from ..board import scoring_fn, return_all_pending_moves

def main(gameboard, ai_player, opponent_player):
    best_score = constants.M_INFINITY
    best_move = None

    if ai_player.is_1st_move:
        do_first_move(ai_player)
    else:
        board = copy.deepcopy(gameboard)
        ai_copy = copy.deepcopy(ai_player)
        opponent_copy = copy.deepcopy(opponent_player)

        for move in return_all_valid_moves:
            if board.fit_piece(move):
                score = do_minimax(constants.INFINITY, constants.M_INFINITY, \
                               board, ai_copy, opponent_copy, True)
                if score > best_score:
                    best_score = score
                    best_move = move

def do_first_move(player):
    pieces = player.remaining_pieces.keys()
    #Lets not use the 1x1 piece in the beginning
    pieces.remove("piece1")
    piece = random.choice(pieces)
    flip = random.choice(range(player.remaining_pieces[piece]["flips"] - 1))
    rot = random.choice(range(player.remaining_pieces[piece]["rots"] - 1))
    
    player.current_piece["piece"] = piece
    player.current_piece["arr"] = 
    player.current_piece["rotated"] = rot
    player.current_piece["flipped"] = flip

def do_minimax(alpha, beta, board, ai_player, opponent_player, \
               maximizing_player, depth = 3):
    
    if maximizing_player:
        if depth == 0 or len(ai_moves) == 0:
            return scoring_fn(ai_player.remaining_pieces)
        
        return get_max(alpha, beta, available_moves, depth)
    
    else:
        if depth == 0 or len(player_moves) == 0:
            return scoring_fn(opponent_player.remaining_pieces)

        return get_min(alpha, beta, available_moves, depth)

def get_max(alpha, beta, board, ai_player, opponent_player, depth):
    max_eval = constants.M_INFINITY
    ai_moves = return_all_pending_moves(board, ai_player)

    for child in ai_moves:
        board.retain_board(ai_player, opponent_player)
        if board.fit_piece(child, coords, ai_player):
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
    player_moves = return_all_pending_moves(board, opponent_player)

    for child in player_moves:
        board.retain_board(ai_player, opponent_player)
        if board.fit_piece(child):
            eval = do_minimax(alpha, beta, board, ai_player, \
                              opponent_player, True, depth - 1)
            board.restore_board(ai_player, opponent_player)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
    return min_eval