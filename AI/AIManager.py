#This is the AIManager script. It sends the current state of
#the board or other required parameters to the respective AI
#that we are using in the game
from AI import MinimaxAI
from RandomMovesBot.RandomMovesBot import return_random_move

def main(gameboard, ai_player, opponent_player):
    best_move = None
    if ai_player.ai_name == "MinimaxAI":
        best_move = MinimaxAI.main(gameboard, ai_player, opponent_player)
    elif ai_player.ai_name == "RandomMovesBot":
        best_move = return_random_move(ai_player)
    """Add your AI here with elif conditions. It should end the turn
    by returning a dict containg the best move in the same format as
    the return value in return_all_pending_moves"""
    
    #######################################################################
    if not gameboard.fit_piece(best_move, ai_player, opponent_player):
        raise Exception("AI piece was not fit")