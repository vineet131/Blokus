import numpy as np, copy
import constants

def main(gameboard, player, opponent_player):
    gameboard_copy = copy.deepcopy(gameboard)
    #We trained the TD learning algorithm to predict a max value when player 2 wins.
    #So we pass the board state to the algorithm as if we are player 2
    """if player.number == 1:
        #Naive swap of array values. If you know a faster way, help me
        #Stack Overflow was of no help to me
        state = np.array(np.where(state == 1, constants.INFINITY, state))
        state = np.array(np.where(state == 2, 1, state))
        state = np.array(np.where(state == constants.INFINITY, 2, state))"""
    best_move = player.ai_class.explore_or_exploit(gameboard_copy, player, opponent_player)
    return best_move