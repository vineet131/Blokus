import numpy as np, pygame, os
import board, pieces, constants, player, drawElements
from board import Board
from AI import AIManager
#Handles where the window position is drawn on the os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (30,30)

class PygameClass:
    def __init__(self, player_init_params = None, render = True):
        if render:
            self.screen, self.background, self.piece_surface, self.clock = self.init_pygame()
        self.offset_list = []
        self.game_over = False
        self.selected = None
        self.gameboard = Board()
        self.board_rects = drawElements.init_gameboard(self.gameboard.board)
        self.infobox_msg_time_start = None
        self.infobox_msg_timeout = 4000 #milliseconds
        self.infobox_msg = ""

        if player_init_params is None:
            player_init_params = {"p1" : {"is_ai" : False, "color" : constants.PURPLE, "name_if_ai" : None},
                                  "p2" : {"is_ai" : True, "color" : constants.ORANGE, "name_if_ai" : "RandomMovesBot"}}
        self.player1, self.player2 = self.init_players(player_init_params)
        
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
    
    def init_players(self, player_init_params):
        player1 = player.Player(constants.PLAYER1_VALUE, player_init_params["p1"]["color"], \
                                player_init_params["p1"]["is_ai"], player_init_params["p1"]["name_if_ai"])
        player2 = player.Player(constants.PLAYER2_VALUE, player_init_params["p2"]["color"], \
                                player_init_params["p2"]["is_ai"], player_init_params["p2"]["name_if_ai"])
        return player1, player2
    
    def event_handler(self, active_player, opponent):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                IS_QUIT = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if constants.VERBOSITY > 1:
                    print("Mouse pos:", pygame.mouse.get_pos())
                #If a piece is selected, we see if we can place it on the board
                if self.selected is not None:
                    if drawElements.are_squares_within_board(active_player.current_piece, self.board_rects):
                        rect_coords = [active_player.current_piece["rects"][0].centerx, \
                                       active_player.current_piece["rects"][0].centery]
                        board_arr_coords = drawElements.grid_to_array_coords(rect_coords)
                        #This part just adjusts the coordinates so that the piece's array coordinate at [0,0] is chosen
                        j = 0
                        while not active_player.current_piece["arr"][0][j] == 1:
                            j += 1
                        board_arr_coords[1] -= j
                        active_player.current_piece["place_on_board_at"] = board_arr_coords
                        ###End of code that adjusts the coordinates
                        #Just fit the piece, the code written inside the method will handle the rest
                        if self.gameboard.fit_piece(active_player.current_piece, active_player, opponent):
                            self.selected = None
                            active_player, opponent = player.switch_active_player(active_player, opponent)
                        #Display an error message if piece isn't fit
                        else:
                            self.display_infobox_msg_start("not_valid_move")
                    #Empty the selection if we click outide the board
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
                    self.key_controls(event, active_player)
        return active_player, opponent
    
    def key_controls(self, event, active_player):
        if event.key == pygame.K_LEFT:
            #Rotate left
            active_player.rotate_current_piece()
            self.offset_list = drawElements.draw_rotated_flipped_selected_piece(active_player.current_piece)
        elif event.key == pygame.K_RIGHT:
            #Rotate right
            active_player.rotate_current_piece(False)
            self.offset_list = drawElements.draw_rotated_flipped_selected_piece(active_player.current_piece)
        elif event.key == pygame.K_UP:
            #Flip along main diagonal
            active_player.flip_current_piece()
            self.offset_list = drawElements.draw_rotated_flipped_selected_piece(active_player.current_piece)
    
    def display_infobox_msg_start(self, msg_key):
        self.infobox_msg_time_start = pygame.time.get_ticks()
        self.infobox_msg = msg_key
    
    def display_infobox_msg_end(self):
        if pygame.time.get_ticks() - self.infobox_msg_time_start > self.infobox_msg_timeout:
            self.infobox_msg_time_start = None

#Game into screen code (Currently incomplete)
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
                #This was for debugging purposes
                pygame.time.wait(20)
            AIManager.main(pgc.gameboard, active_player, opponent)
            active_player, opponent = player.switch_active_player(active_player, opponent)
        else:
            active_player, opponent = pgc.event_handler(active_player, opponent)
        
        # Set the screen background
        pgc.background.fill(constants.BLACK)
        
        #Draw the necessary components
        drawElements.draw_infobox(pgc.background, pgc.player1, pgc.player2)
        if pgc.infobox_msg_time_start is not None:
            drawElements.draw_infobox_msg(pgc.background, pgc.player1, pgc.player2, pgc.infobox_msg)
            pgc.display_infobox_msg_end()
        drawElements.draw_gameboard(pgc.background, pgc.board_rects, pgc.gameboard, \
                                    active_player.current_piece, active_player)
        drawElements.draw_pieces(pgc.background, pgc.player1, pgc.player2, active_player, pgc.selected)
        if pgc.selected is not None:
            drawElements.draw_selected_piece(pgc.background, pgc.offset_list, pygame.mouse.get_pos(), \
                                             active_player.current_piece, active_player.color)
        if board.is_game_over(pgc.gameboard, active_player, opponent):
            #pgc.game_over = True
            pgc.display_infobox_msg_start("game_over")
        pgc.screen.blit(pgc.background, (0,0))
        
        # Limit to 60 frames per second
        pgc.clock.tick(60)
 
        # Update the screen with what is drawn.
        pygame.display.update()

if __name__ == "__main__":
    IS_QUIT = False

    game_loop()

    if IS_QUIT:
        pygame.quit()