import numpy as np

def get_pieces():
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
        "piece10": {"arr":np.array([[1],[1],[1],[1],[1]]),"rots":2,"flips":1},
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

def discard_piece(piece_name, player):
    #Delete from dictionary of current pieces
    del player.remaining_pieces[piece_name]
    #Append to dictionary containing discarded pieces
    player.discarded_pieces[piece_name] = get_pieces()[piece_name]