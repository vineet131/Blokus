import numpy as np, pygame
import board, pieces, constants, player, draw_elements
from board import Board
from AI import AIManager

def pygame_init():
    pygame.init()
    window = pygame.display.set_mode(constants.WINDOW_SIZE)
    background = pygame.Surface(constants.WINDOW_SIZE)
    pygame.display.set_caption("Blokus on Pygame")
    pygame.font.init()
    """font = pygame.font.SysFont("", 15)
    label = font.render("Blokus", 1, constants.BLACK)
    surface.blit(label, dims)"""
    return window, background

def key_controls(keys):
    if keys[pygame.K_LEFT]:
        #Move left
        pass
    if keys[pygame.K_RIGHT]:
        #Move right
        pass
    if keys[pygame.K_UP]:
        #Move up
        pass
    if keys[pygame.K_DOWN]:
        #Move down
        pass
    if keys[pygame.K_a]:
        #Rotate left
        pass
    if keys[pygame.K_d]:
        #Rotate right
        pass
    if keys[pygame.K_w]:
        #Flip along main diagonal
        pass
    if keys[pygame.K_s]:
        #Flip along other diagonal
        pass

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                IS_QUIT = True
        if IS_QUIT:
            break
        large_text = pygame.font.Font('freesansbold.ttf', 115)
        #We also need a window where we can choose starting options
        #That window is where we will initialise the player objects

def event_handler(gameboard, active_player, opponent, game_over, offset_list,\
                  selected, p1_rects, p2_rects):
    is_piece_selected = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            IS_QUIT = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if constants.VERBOSITY > 0:
                print(pygame.mouse.get_pos())
            if event.button == 1 and selected is not None: #Left mouse click
                selected = None
            else:
                if active_player.number == 1:
                    offset_list, selected = draw_elements.generate_element_offsets(p1_rects, event)
                elif active_player.number == 2:
                    offset_list, selected = draw_elements.generate_element_offsets(p2_rects, event)
        elif event.type == pygame.MOUSEBUTTONUP:
            if is_piece_selected:
                if gameboard.fit_piece(active_player.current_piece, active_player, opponent):
                    active_player, opponent = player.switch_active_player(active_player, opponent)
        elif event.type == pygame.MOUSEMOTION:
            if selected is not None:
                rect = p1_rects[selected]
                for i in range(len(rect)):
                    rect[i].x = event.pos[0] + offset_list[i][0]
                    rect[i].y = event.pos[1] + offset_list[i][1]
                    rect[i].h += 39
                    rect[i].w += 39
                    print(rect[i].x, rect[i].y, rect[i].h, rect[i].w, event.pos)
    #for keys in pygame.key.get_pressed():
    #    key_controls(keys)
    return game_over, active_player, opponent, offset_list, selected

def init(player1_is_ai, player2_is_ai,
         player1_color, player2_color,
         player1_name_if_ai, player2_name_if_ai):
    gameboard = Board()
    player1 = player.Player(constants.PLAYER1_VALUE, player1_color, player1_is_ai, player1_name_if_ai)
    player2 = player.Player(constants.PLAYER2_VALUE, player2_color, player2_is_ai, player2_name_if_ai)
    return gameboard, player1, player2

def game_loop():
    game_over = False
    selected, p1_rects, p2_rects = None, [], []
    offset_list = []

    #gameboard, player1, player2 = init(False, True, constants.PURPLE, constants.ORANGE, None, "MinimaxAI")
    gameboard, player1, player2 = init(True, True, constants.PURPLE, constants.ORANGE, "RandomMovesBot", "MinimaxAI")
    active_player, opponent = player1, player2

    while not game_over:
        if active_player.number == 1:
            p1_rects, p2_rects = draw_elements.init_piece_rects(background, active_player, opponent)
        elif active_player.number == 2:
            p1_rects, p2_rects = draw_elements.init_piece_rects(background, opponent, active_player)
        #Two kinds of players, human and AI. We use that as our basis for checking and making turn based moves.
        #When AI player's turn, let the AIManager handle the move making
        #When human player's turn, listen for input
        if active_player.is_ai:
            if not active_player.is_1st_move:
                pygame.time.wait(7000)
            AIManager.main(gameboard, active_player, opponent)
            active_player, opponent = player.switch_active_player(active_player, opponent)
        else:
            game_over, active_player, opponent, offset_list, selected \
            = event_handler(gameboard, active_player, opponent, game_over, offset_list, selected, p1_rects, p2_rects)
        
        # Set the screen background
        screen.fill(constants.BLACK)
        
        draw_elements.draw_infobox(background, active_player, opponent)
        draw_elements.draw_pieces(background, p1_rects, p2_rects, player1.color, player2.color)
        draw_elements.draw_gameboard(background, gameboard.board)
        screen.blit(background, (0,0))
        #print(draw_elements.get_square_under_mouse(gameboard.board))
        
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Update the screen with what is drawn.
        pygame.display.update()
        if selected is None:
            background.fill(constants.BLACK)

screen, background = pygame_init()
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
IS_QUIT = False

game_loop()

if IS_QUIT:
    pygame.quit()