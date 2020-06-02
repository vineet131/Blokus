import numpy as np, pygame
import board, pieces, constants, player, draw_elements
from board import Board

def pygame_init():
    pygame.init()
    window = pygame.display.set_mode(constants.WINDOW_SIZE)
    pygame.display.set_caption("Blokus on Pygame")
    return window

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

def init(player1_is_ai,
         player2_is_ai,
         player1_color,
         player2_color,
         player1_name_if_ai,
         player2_name_if_ai):
    gameboard = Board()
    player1 = player.Player(constants.PLAYER1_VALUE, player1_color, player1_is_ai, player1_name_if_ai)
    player2 = player.Player(constants.PLAYER2_VALUE, player2_color, player2_is_ai, player2_name_if_ai)
    return gameboard, player1, player2

def game_loop():
    game_over = False

    gameboard, player1, player2 = init(False, True, constants.PURPLE, constants.ORANGE, None, "MinimaxAI")
    active_player, opponent = player1, player2

    while not game_over:
        is_piece_selected = False
        #Two kinds of players, human and AI. We use that as our basis for checking and making turn based moves.
        #When AI player's turn, let the AIManager handle the move making
        #When human player's turn, listen for input
        if active_player.is_ai:
            AIManager.main(gameboard, active_player, opponent)
            active_player, opponent = player.switch_active_player(active_player, opponent)
        else:
            # Check for player input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    IS_QUIT = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # User clicks the mouse. Get the position
                    pos = pygame.mouse.get_pos()
                    if constants.VERBOSITY > 0:
                        print(pos)
                    
                elif event.type == pygame.MOUSEBUTTONUP:
                    if is_piece_selected:
                        if gameboard.fit_piece(active_player.current_piece, active_player, opponent):
                            active_player, opponent = player.switch_active_player(active_player, opponent)
                elif event.type == pygame.MOUSEMOTION:
                    if is_piece_selected:
                        mouse_x, mouse_y = event.pos
                        #rectangle.x = mouse_x + offset_x
                        #rectangle.y = mouse_y + offset_y
            keys = pygame.key.get_pressed()
            key_controls(keys)

        # Set the screen background
        screen.fill(constants.BLACK)

        draw_elements.draw_gameboard(gameboard.board, screen)
        draw_elements.draw_pieces(screen, active_player, opponent)

        # Limit to 60 frames per second
        clock.tick(60)
 
        # Update the screen with what is drawn.
        pygame.display.update()

screen = pygame_init()
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
IS_QUIT = False

game_loop()

if IS_QUIT:
    pygame.quit()