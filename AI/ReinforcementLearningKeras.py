from AI import ReinfocementLearningModelKeras as rlmk
from blokus import init, pygame_init
import constants, board, pieces, drawElements
import os, numpy as np, matplotlib.pyplot as plt
from tqdm import tqdm

N_EPISODES = 2000
LEARNING_RATE = 0.1
GAMMA = 0.95 #Discount at each step
RENDER_EVERY = 400
BATCH_SIZE = 32

if not os.path.exists('models'):
    os.makedirs('models')
MODEL_SAVE_FOLDER = os.getcwd()
MODEL_SAVE_FILE = os.path('models')

def reward_func(player, reward, did_player_lose_game = False):
    score = board.scoring_fn(player.remaining_pieces)
    if not did_player_lose_game:
        reward += score * (GAMMA ^ player.turn_number)
    else:
        reward = reward - 2
    return reward

for ep in tqdm(range(N_EPISODES), ascii=True, unit="Episodes"):
    game_over = False
    if ep % RENDER_EVERY:
        is_render == True
        screen, background, clock = pygame_init
    
    gameboard, player1, player2 = init(True, True, constants.PURPLE, constants.ORANGE, "RandomMovesBot", "RandomMovesBot")
    #Made the redundant passing to player1 & player2 first and then to active_player & opponent for clarity/legibility
    active_player, opponent = player1, player2
    
    state_size = np.reshape(gameboard.board, [1, constants.ROW_COUNT*constants.COLUMN_COUNT]).shape
    action_size_1 = len(player.remaining_pieces)
    action_size_2 = 2 #x & y position
    dqnet = rlmk.DQN(state_size, action_size)
    
    while not game_over:
        check_action = dqnet.explore_or_exploit(gameboard)
        if  == None:
            move = AIManager.main(gameboard, active_player, opponent)
        else:
            
        
        active_player, opponent = player.switch_active_player(active_player, opponent)
        if is_render:
            if active_player.number == 1:
                p1_rects, p2_rects = drawElements.init_piece_rects(background, active_player, opponent)
            elif active_player.number == 2:
                p1_rects, p2_rects = drawElements.init_piece_rects(background, opponent, active_player)
            # Set the screen background
            screen.fill(constants.BLACK)
        
            drawElements.draw_infobox(background, active_player, opponent)
            drawElements.draw_pieces(background, p1_rects, p2_rects, player1.color, player2.color)
            drawElements.draw_gameboard(background, gameboard.board)
            screen.blit(background, (0,0))
            #print(drawElements.get_square_under_mouse(gameboard.board))
        
            # Limit to 60 frames per second
            clock.tick(60)
 
            # Update the screen with what is drawn.
            pygame.display.update()
            if selected is None:
                background.fill(constants.BLACK)
        
        if board.is_game_over(gameboard, active_player, opponent):
            game_over = True
    