import numpy as np

def get_pieces():
    dict_pieces_5x5={
        "piece1": np.array([[0,0,0,0,0],[0,1,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]),
        "piece2": np.array([[0,0,0,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,0,0,0],[0,0,0,0,0]]),
        "piece3": np.array([[0,0,0,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,0,0,0]]),
        "piece4": np.array([[0,0,0,0,0],[0,1,0,0,0],[0,1,1,0,0],[0,0,0,0,0],[0,0,0,0,0]]),
        "piece5": np.array([[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,0,0,0]]),
        "piece6": np.array([[0,0,0,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,1,1,0,0],[0,0,0,0,0]]),
        "piece7": np.array([[0,0,0,0,0],[0,1,0,0,0],[0,1,1,0,0],[0,1,0,0,0],[0,0,0,0,0]]),
        "piece8": np.array([[0,0,0,0,0],[0,1,1,0,0],[0,1,1,0,0],[0,0,0,0,0],[0,0,0,0,0]]),
        "piece9": np.array([[0,0,0,0,0],[0,1,1,0,0],[0,0,1,1,0],[0,0,0,0,0],[0,0,0,0,0]]),
        "piece10": np.array([[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]]),
        "piece11": np.array([[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,1,1,0,0],[0,0,0,0,0]]),
        "piece12": np.array([[0,0,1,0,0],[0,0,1,0,0],[0,1,1,0,0],[0,1,0,0,0],[0,0,0,0,0]]),
        "piece13": np.array([[0,0,0,0,0],[0,0,1,0,0],[0,1,1,0,0],[0,1,1,0,0],[0,0,0,0,0]]),
        "piece14": np.array([[0,0,0,0,0],[0,1,1,0,0],[0,0,1,0,0],[0,1,1,0,0],[0,0,0,0,0]]),
        "piece15": np.array([[0,1,0,0,0],[0,1,1,0,0],[0,1,0,0,0],[0,1,0,0,0],[0,0,0,0,0]]),
        "piece16": np.array([[0,0,0,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,1,1,1,0],[0,0,0,0,0]]),
        "piece17": np.array([[0,0,0,0,0],[0,1,0,0,0],[0,1,0,0,0],[0,1,1,1,0],[0,0,0,0,0]]),
        "piece18": np.array([[0,0,0,0,0],[0,1,1,0,0],[0,0,1,1,0],[0,0,0,1,0],[0,0,0,0,0]]),
        "piece19": np.array([[0,0,0,0,0],[0,1,0,0,0],[0,1,1,1,0],[0,0,0,1,0],[0,0,0,0,0]]),
        "piece20": np.array([[0,0,0,0,0],[0,1,0,0,0],[0,1,1,1,0],[0,0,1,0,0],[0,0,0,0,0]]),
        "piece21": np.array([[0,0,0,0,0],[0,0,1,0,0],[0,1,1,1,0],[0,0,1,0,0],[0,0,0,0,0]]),
    }
    dict_pieces={
        "piece1": {"arr":np.array([[1]]),"rots":1,"flips":1},
        "piece2": {"arr":np.array([[1],[1]]),"rots":2,"flips":1},
        "piece3": {"arr":np.array([[1],[1],[1]]),"rots":2,"flips":1},
        "piece4": {"arr":np.array([[1,0],[1,1]]),"rots":4,"flips":1},
        "piece5": {"arr":np.array([[1],[1],[1],[1]]),"rots":2,"flips":1},
        "piece6": {"arr":np.array([[0,1],[0,1],[1,1]]),"rots":4,"flips":2},
        "piece7": {"arr":np.array([[1,0],[1,1],[1,0]]),"rots":4,"flips":1},
        "piece8": {"arr":np.array([[1,1],[1,1]]),"rots":1,"flips":1},
        "piece9": {"arr":np.array([[1,1,0],[0,1,1]]),"rots":2,"flips":2},
        "piece10": {"arr":np.array([[1],[1],[1],[1],[1]),"rots":2,"flips":1},
        "piece11": {"arr":np.array([[0,1],[0,1],[0,1],[1,1]]),"rots":4,"flips":2},
        "piece12": {"arr":np.array([[0,1],[0,1],[1,1],[1,0]]),"rots":4,"flips":2},
        "piece13": {"arr":np.array([[0,1],[1,1],[1,1]]),"rots":4,"flips":2},
        "piece14": {"arr":np.array([[1,1],[0,1],[1,1]]),"rots":4,"flips":1},
        "piece15": {"arr":np.array([[1,0],[1,1],[1,0],[1,0]]),"rots":4,"flips":2},
        "piece16": {"arr":np.array([[0,1,0],[0,1,0],[1,1,1]]),"rots":4,"flips":1},
        "piece17": {"arr":np.array([[1,0,0],[1,0,0],[1,1,1]]),"rots":4,"flips":1},
        "piece18": {"arr":np.array([[1,1,0],[0,1,1],[0,0,1]]),"rots":4,"flips":1},
        "piece19": {"arr":np.array([[1,0,0],[1,1,1],[0,0,1]]),"rots":2,"flips":2},
        "piece20": {"arr":np.array([[1,0,0],[1,1,1],[0,1,0]]),"rots":4,"flips":2},
        "piece21": {"arr":np.array([[0,1,0],[1,1,1],[0,1,0]]),"rots":1,"flips":1},
    }
    return dict_pieces

def rotate_piece(piece, k):
    #Rotates the piece. k=-1 rotates in clockwise direction
    return np.rot90(piece, k)
    
def flip_piece(piece):
    #Flip the piece inside-out
    return np.flipud(piece)
    
def discard_piece(piece, player):
    #Append to dictionary containing discarded pieces
    del player.remaining_pieces[piece.key()]
    player.discarded_pieces[piece.key()] = piece.value()