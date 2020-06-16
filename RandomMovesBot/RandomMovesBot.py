import numpy as np, random, board, constants
#This computer "player" just keeps playing random moves
#This random moves player serves as a good opponent for our actual AI

def return_random_move(player):
    if player.is_1st_move:
        return return_first_turn_move(player)
    else:
        return random.choice(board.return_all_pending_moves(player))

def return_first_turn_move(player):
    pieces = list(player.remaining_pieces.keys())
    #Lets not use the 1x1 piece in the beginning
    pieces.remove("piece1")
    piece = random.choice(pieces)
    if constants.VERBOSITY > 0:
        print("RandomMovesBot chooses piece: ", piece)
    piece_arr = player.remaining_pieces[piece]["arr"]
    flips = player.remaining_pieces[piece]["flips"] - 1
    if flips > 0:
        flip = random.choice(range(flips))
    else:
        flip = 0
    rots = player.remaining_pieces[piece]["rots"] - 1
    if rots > 0:
        rot = random.choice(range(rots))
    else:
        rot = 0
    if player.number == 1:
        start_x, start_y = constants.STARTING_PTS["player1"][0], \
                           constants.STARTING_PTS["player1"][1]
    elif player.number == 2:
        start_x, start_y = constants.STARTING_PTS["player2"][0], \
                           constants.STARTING_PTS["player2"][1]
    board_x = start_x - random.choice(range(piece_arr.shape[0]))
    board_y = start_y - random.choice(range(piece_arr.shape[1]))
    
    piece_arr = np.rot90(piece_arr, k = rot)
    if flip == 1:
        piece_arr = np.flipud(piece_arr)

    move = {"piece" : piece, "arr" : piece_arr, "rotated" : rot, "flipped" : flip, \
            "place_on_board_at" : [board_x, board_y]}
    return move