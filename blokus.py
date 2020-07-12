import numpy as np, pygame, os
import board, pieces, constants, player, drawElements
from board import Board
from AI import AIManager
#Handles where the window position is drawn on the os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (30,30)

class PygameClass:
    def __init__(self):
        self.screen, self.background, self.piece_surface, self.clock = self.init_pygame()
        self.offset_list = []
        self.game_over = False
        self.selected = None
        self.gameboard = Board()
        self.board_rects = drawElements.init_gameboard(self.gameboard.board)
        self.player1, self.player2 = self.init_players(False, True, constants.PURPLE, constants.ORANGE, None, "RandomMovesBot")
        #self.player1, self.player2 = self.init_players(False, False, constants.PURPLE, constants.ORANGE, None, None)
        #self.player1, self.player2 = self.init_players(False, True, constants.PURPLE, constants.ORANGE, None, "MinimaxAI")
        #self.player1, self.player2 = self.init_players(True, True, constants.PURPLE, constants.ORANGE, "RandomMovesBot", "MinimaxAI")
        #self.player1, self.player2 = self.init_players(True, True, constants.PURPLE, constants.ORANGE, "RandomMovesBot", "RandomMovesBot")
        
    def init_pygame(self):
        pygame.init()
        window = pygame.display.set_mode(constants.WINDOW_SIZE)
        background = pygame.Surface(constants.WINDOW_SIZE)
        piece_surface = pygame.Surface([50,50]).set_alpha(180)
        pygame.display.set_caption("Blokus on Pygame")
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
        """font = pygame.font.SysFont("", 15)
        label = font.render("Blokus", 1, constants.BLACK)
        surface.blit(label, dims)"""
        return window, background, piece_surface, clock
    
    def init_players(self, player1_is_ai, player2_is_ai,\
                     player1_color, player2_color,\
                     player1_name_if_ai, player2_name_if_ai):
        player1 = player.Player(constants.PLAYER1_VALUE, player1_color, player1_is_ai, player1_name_if_ai)
        player2 = player.Player(constants.PLAYER2_VALUE, player2_color, player2_is_ai, player2_name_if_ai)
        return player1, player2
    
    def event_handler(self, active_player, opponent):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                IS_QUIT = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if constants.VERBOSITY > 0:
                    print("Mouse pos:", pygame.mouse.get_pos())
                #If a piece is selected, we see if we can place it on the board
                if self.selected is not None:
                    if drawElements.are_squares_within_board(active_player.current_piece, self.board_rects):
                        coords = [active_player.current_piece["rects"][0].centerx, active_player.current_piece["rects"][0].centery]
                        active_player.current_piece["place_on_board_at"] = drawElements.grid_to_array_coords(coords)
                        if self.gameboard.fit_piece(active_player.current_piece, active_player, opponent):
                            active_player.empty_current_piece()
                            self.selected = None
                            active_player, opponent = player.switch_active_player(active_player, opponent)
                    else:
                        self.selected = None
                #else we check if we need to pick up a piece
                else:
                    self.offset_list, self.selected = drawElements.generate_element_offsets(active_player.remaining_pieces, event)
                    if self.selected is not None:
                        active_player.current_piece["piece"] = self.selected
                        active_player.current_piece["arr"] = active_player.remaining_pieces[self.selected]["arr"]
                        active_player.current_piece["rects"] = active_player.remaining_pieces[self.selected]["rects"]
            elif event.type == pygame.MOUSEBUTTONUP:
                drawElements.init_piece_rects(self.player1.remaining_pieces, self.player2.remaining_pieces)
            elif event.type == pygame.KEYDOWN:
                if self.selected is not None:
                    key_controls(event, active_player)
        return active_player, opponent
    
def key_controls(event, active_player):
    if event.key == pygame.K_LEFT:
        #Rotate left
        active_player.rotate_current_piece(False)
    elif event.key == pygame.K_RIGHT:
        #Rotate right
        active_player.rotate_current_piece()
    elif event.key == pygame.K_UP:
        #Flip along main diagonal
        pass
    elif event.key == pygame.K_DOWN:
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

#The main game loop
def game_loop():
    pgc = PygameClass()
    active_player, opponent = pgc.player1, pgc.player2
    drawElements.init_piece_rects(pgc.player1.remaining_pieces, pgc.player2.remaining_pieces)
    
    while not pgc.game_over:
        #Two kinds of players, human and AI. We use that as our basis for checking and making turn based moves.
        #When AI player's turn, let the AIManager handle the move making
        #When human player's turn, listen for input
        if active_player.is_ai:
            if not active_player.is_1st_move:
                pygame.time.wait(2000)
            AIManager.main(pgc.gameboard, active_player, opponent)
            active_player, opponent = player.switch_active_player(active_player, opponent)
        else:
            active_player, opponent = pgc.event_handler(active_player, opponent)
        
        # Set the screen background
        pgc.background.fill(constants.BLACK)
        
        drawElements.draw_infobox(pgc.background, active_player, opponent)
        drawElements.draw_gameboard(pgc.background, pgc.board_rects, pgc.gameboard.board, active_player.current_piece)
        drawElements.draw_pieces(pgc.background, pgc.player1, pgc.player2, active_player, pgc.selected)
        if pgc.selected is not None:
            drawElements.draw_selected_piece(pgc.background, pgc.offset_list, pygame.mouse.get_pos(), active_player.current_piece, active_player.color)
        
        pgc.screen.blit(pgc.background, (0,0))
        #print(drawElements.get_square_under_mouse(gameboard.board))
        
        # Limit to 60 frames per second
        pgc.clock.tick(60)
 
        # Update the screen with what is drawn.
        pygame.display.update()
        
        if board.is_game_over(pgc.gameboard, active_player, opponent):
            pgc.game_over = True

IS_QUIT = False

game_loop()

if IS_QUIT:
    pygame.quit()