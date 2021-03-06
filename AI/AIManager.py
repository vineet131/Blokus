#This is the AIManager script. It sends the current state of
#the board or other required parameters to the respective AI
#that we are using in the game
from AI import MinimaxAI, CustomEvaluationAI, ReinforcementLearningAI
from RandomMovesBot.RandomMovesBot import return_random_move
from board import is_game_over

def main(gameboard, ai_player, opponent_player):
    best_move = None
    if ai_player.ai_name == "MinimaxAI":
        best_move = MinimaxAI.main(gameboard, ai_player, opponent_player)
    elif ai_player.ai_name == "RandomMovesBot":
        best_move = return_random_move(gameboard, ai_player)
    elif ai_player.ai_name == "CustomEvaluationAI":
        best_move = CustomEvaluationAI.main(gameboard, ai_player, opponent_player)
    elif ai_player.ai_name == "ReinforcementLearningAI":
        best_move = ReinforcementLearningAI.main(gameboard, ai_player, opponent_player)
    """
    Add your AI here with elif conditions. It should end the turn
    by returning a dict containg the best move in the same format as
    the return value in return_all_pending_moves() in board.py. If the number of moves
    playable are zero, then we return None. This is because game doesn't
    finish until both players have exhausted their moves. This method only returns
    moves. The logic to handle whether game is over is already included in the game loop
    """
    
    #######################################################################
    if best_move != None:
        if not gameboard.fit_piece(best_move, ai_player, opponent_player):
            print("For player %s with number %s, the following move has failed:\n %s" \
                  % (ai_player.ai_name, ai_player.number, best_move))
            print("The state of the gameboard is: \n%s" % gameboard.board)
            raise Exception("Piece selected by AI was not fit")
        return best_move