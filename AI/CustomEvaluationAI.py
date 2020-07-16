#Custom evaluation function that evaluates the board position and returns a move
import copy, random, constants, pieces, numpy as np
from board import scoring_fn, return_all_pending_moves

def main(gameboard, ai_player, opponent_player):
    best_score = constants.M_INFINITY
    best_move = None

    if ai_player.is_1st_move:
        best_move = do_first_move(ai_player)
    else:
        board_copy = copy.deepcopy(gameboard)
        ai_copy = copy.deepcopy(ai_player)
        opponent_copy = copy.deepcopy(opponent_player)
        for move in return_all_pending_moves(board_copy, ai_copy):
            simulate_move(board_copy, move, ai_copy, opponent_copy)
            score = eval_fn(ai_player.board_corners, ai_player.remaining_pieces)
            if score > best_score:
                best_score = score
                best_move = move
            undo_move(board_copy, move, ai_copy, opponent_copy)
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

def eval_fn(corners, remaining_pieces):
    score = 0
    for _, val in corners.items():
        score += len(val)
    for _, val in remaining_pieces.items():
        for x in range(val["arr"].shape[0]):
            for y in range(val["arr"].shape[1]):
                if val["arr"][x][y] == 1:
                    score -= 1
    return score

def simulate_move(gameboard, piece, player, opponent_player):
    rows = constants.ROW_COUNT
    cols = constants.COLUMN_COUNT
    piece_x_rng = range(piece["arr"].shape[0])
    piece_y_rng = range(piece["arr"].shape[1])
    board_x_rng = range(piece["place_on_board_at"][0], rows)
    board_y_rng = range(piece["place_on_board_at"][1], cols)

    for i, x in zip(piece_x_rng, board_x_rng):
        for j, y in zip(piece_y_rng, board_y_rng):
            if piece["arr"][i][j] == 1:
                gameboard.board[x][y] = player.number * piece["arr"][i][j]
    pieces.discard_piece(piece["piece"], player)
    gameboard.turn_number += 1
    player.turn_number += 1
    #player.update_score()
    gameboard.update_board_corners(player, opponent_player)

def undo_move(gameboard, piece, player, opponent_player):
    rows = constants.ROW_COUNT
    cols = constants.COLUMN_COUNT
    piece_x_rng = range(piece["arr"].shape[0])
    piece_y_rng = range(piece["arr"].shape[1])
    board_x_rng = range(piece["place_on_board_at"][0], rows)
    board_y_rng = range(piece["place_on_board_at"][1], cols)

    for i, x in zip(piece_x_rng, board_x_rng):
        for j, y in zip(piece_y_rng, board_y_rng):
            if piece["arr"][i][j] == 1:
                gameboard.board[x][y] = constants.BOARD_FILL_VALUE
    player.remaining_pieces[piece["piece"]] = pieces.get_pieces()[piece["piece"]]
    del player.discarded_pieces[piece["piece"]]
    gameboard.turn_number -= 1
    player.turn_number -= 1
    #player.update_score()
    gameboard.update_board_corners(player, opponent_player)