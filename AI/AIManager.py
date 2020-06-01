#This is the AIManager script. It sends the current state of
#the board or other required parameters to the respective AI
#that we are using in the game
import MinimaxAI

def main(gameboard, ai_player, opponent_player):
    if ai_player.name == "MinimaxAI":
        best_move = MinimaxAI.main(gameboard, ai_player, opponent_player)
    #Add your AI here with elif conditions. It should end the turn
    #by returning a dict containg the best move in the same format as
    #the return value in return_all_pending_moves

    gameboard.fit_piece(best_move, best_move["place_on_board_at"], ai_player, opponent_player)