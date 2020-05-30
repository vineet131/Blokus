import numpy as np, pygame
import board, pieces, constants, player, draw_elements
from board import Board

def pygame_init():
    pygame.init()
    window = pygame.display.set_mode(constants.WINDOW_SIZE)
    pygame.display.set_caption("Blokus on Pygame")
    return window

screen = pygame_init()

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

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
                is_quit = True
        if is_quit:
            break
        large_text = pygame.font.Font('freesansbold.ttf', 115)
        #We also need a window where we can choose starting options
        #That window is where we will initialise the player objects

is_quit = False

def init(player1_is_ai,
         player2_is_ai,
         player1_color,
         player2_color):
    gameboard = Board().board
    player1 = player.Player(constants.PLAYER1_VALUE, player1_color, player1_is_ai)
    player2 = player.Player(constants.PLAYER2_VALUE, player2_color, player2_is_ai)
    return gameboard, player1, player2

def game_loop():
    game_over = False

    gameboard, player1, player2 = init(False, True, constants.PURPLE, constants.ORANGE)

    while not game_over:
        # Check for player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                #column = pos[0] // (WIDTH + MARGIN)
                #row = pos[1] // (HEIGHT + MARGIN)
                #gameboard[row][column] = 1
    
        if is_quit:
            break
    
        keys = pygame.key.get_pressed()
        key_controls(keys)

        # Set the screen background
        screen.fill(constants.BLACK)

        draw_elements.draw_gameboard(gameboard, screen)

        # Limit to 60 frames per second
        clock.tick(60)
 
        # Update the screen with what is drawn.
        pygame.display.update()

game_loop()
if is_quit:
    pygame.quit()