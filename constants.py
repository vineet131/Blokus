import sys, os

#Developer options for debugging
VERBOSITY = 1

#Board size
ROW_COUNT = 14
COLUMN_COUNT = 14

#89 is the total no. of squares in all 21 pieces
STARTING_SCORE = 89

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_SIZE = [WINDOW_WIDTH, WINDOW_HEIGHT]

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
PURPLE = [128, 0, 128]
ORANGE = [255, 169, 0]
RED = [255, 60, 0]

#The empty squares on the board shall be populated by this value
BOARD_FILL_VALUE = 0
#All squares corresponding to player 1 & 2 on the board shall be populated
#by these values
PLAYER1_VALUE = 1
PLAYER2_VALUE = 2

#Players need to place their initial moves on the following board coordinates
STARTING_PTS = \
{"player1" : [4,4],
 "player2" : [9,9]}

#For Minimax, we define infinity and minus infinity
INFINITY = 10000
M_INFINITY = -10000

def write_to_log(msg):
    log_folder = os.path.abspath(os.path.dirname(sys.argv[0]))
    log_file = os.path.join(log_folder, "log.txt")
    with open(log_file, "a+") as f:
        f.write("\n\n\n"+msg)
        f.close()