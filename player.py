import pieces, constants, board

class Player:
    
    players = [constants.PLAYER1_VALUE, constants.PLAYER2_VALUE]
    
    def __init__(self, player_number, color, is_ai, ai_name = None):
        self.number = player_number
        self.remaining_pieces = pieces.get_pieces()
        self.discarded_pieces = {}
        self.current_piece = {"piece": "", "arr": [], "rotated": 0, "flipped": 0}
        self.color = color
        self.score = board.scoring_fn(remaining_pieces)
        
        #tl = top left, bl = bottom left, tr = top right, br = bottom right
        self.board_corners = {"bl":[],"br":[],"tl":[],"tr":[]}
        self.board_corners_copy = {"bl":[],"br":[],"tl":[],"tr":[]}
        self.is_1st_move = True
        #Useful for AIs
        self.is_ai = is_ai
        self.ai_name = ai_name
        self.remaining_pieces_copy = {}
        self.discarded_pieces_copy = {}

    def update_score(self):
        self.score = board.scoring_fn(remaining_pieces)
    
    def empty_current_piece(self):
        self.current_piece = {"piece": "", "arr": [], "rotated": 0, "flipped": 0}