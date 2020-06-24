import pieces, constants, board

class Player:
    
    players = [constants.PLAYER1_VALUE, constants.PLAYER2_VALUE]
    
    def __init__(self, player_number: int, color: list, is_ai: bool, ai_name = None):
        self.number = player_number
        self.remaining_pieces = pieces.get_pieces()
        self.discarded_pieces = {}
        self.current_piece = {"piece": "", "arr": [], "rotated": 0, "flipped": 0, "place_on_board_at": []}
        self.color = color
        self.score = board.scoring_fn(self.remaining_pieces)
        
        #tl = top left, bl = bottom left, tr = top right, br = bottom right
        self.board_corners = {"bl":[], "br":[], "tl":[], "tr":[]}
        self.is_1st_move = True
        #Used for AIs
        self.is_ai = is_ai
        self.ai_name = ai_name

    def update_score(self):
        self.score = board.scoring_fn(self.remaining_pieces)
    
    def set_current_piece(self, piece_name):
        self.current_piece = {"piece": piece_name, "arr": pieces.get_pieces()[piece_name]}
    
    def empty_current_piece(self):
        self.current_piece = {"piece": "", "arr": [], "rotated": 0, "flipped": 0, "place_on_board_at": []}
    
    #We only rotate whatever is the current piece. We keep track of which rotated state its in
    def rotate_current_piece(self, clockwise = True):
        max_rots = get_pieces()[self.current_piece["piece"]]["rots"]
        current_state = self.current_piece["rotated"]
    
        if clockwise:
            if current_state == max_rots - 1:
                current_state = 0
            else:
                current_state += 1
            self.current_piece["rotated"] = current_state
            return np.rot90(self.current_piece["arr"], k = 1)
        else:
            if current_state == 0:
                current_state = max_rots - 1
            else:
                current_state -= 1
            self.current_piece["rotated"] = current_state
            return np.rot90(self.current_piece["arr"], k = -1)

    #We only flip whatever is the current piece. We keep track of which flipped state its in
    def flip_current_piece(self):
        if get_pieces()[self.current_piece["piece"]]["flips"] == 1:
            return self.current_piece["arr"]
        else:
            if self.current_piece["flipped"] == 1:
                self.current_piece["flipped"] = 0
            else:
                self.current_piece["flipped"] += 1
            return np.flipud(self.current_piece["arr"])

def switch_active_player(active_player, opponent):
    return opponent, active_player