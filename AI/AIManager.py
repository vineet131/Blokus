#This is the AIManager script. It sends the current state of
#the board or other required parameters to the respective AI
#that we are using in the game
import MinimaxAI

def main(gameboard, ai_player, opponent_player):
    if ai_player.name == "MinimaxAI":
        MinimaxAI.main(gameboard, ai_player, opponent_player)
    #Add your AI here with elif conditions. It should end the turn
    #by setting player.current_piece with the piece to be placed