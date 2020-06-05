import pygame, math
import constants

#This file handles generation of all the sizes of the elements
#The values have been optimised for 1280*720 window area
MARGIN = 2

board_width = 620
board_box_width = 42
piece_box_width = (constants.WINDOW_WIDTH - board_width) / 2 #330
one_piece_box_width = piece_box_width / 2 #165
single_piece_width = 9
info_box_width = constants.WINDOW_WIDTH #1280

board_height = board_width #620
board_box_height = board_box_width
piece_box_height = board_height
one_piece_box_height = math.floor(board_height / 11) #56
single_piece_height = single_piece_width #9
info_box_height = constants.WINDOW_HEIGHT - board_height #100

def draw_main_window():
    pass

def grid_to_array_coords():
    #column = pos[0] // (WIDTH + MARGIN)
    #row = pos[1] // (HEIGHT + MARGIN)
    #gameboard[row][column] = 1
    pass

def array_to_grid_coords():
    pass

def draw_gameboard(board_arr, canvas):
    for row in range(board_arr.shape[0]):
        for column in range(board_arr.shape[1]):
            box_width = piece_box_width + MARGIN + ((MARGIN + board_box_width) * column)
            box_height = info_box_height + MARGIN + ((MARGIN + board_box_height) * row)
            dims = [box_width, box_height, board_box_width, board_box_height]
            if board_arr[row][column] == constants.BOARD_FILL_VALUE:
                pygame.draw.rect(canvas, constants.WHITE, dims)
            elif board_arr[row][column] == constants.PLAYER1_VALUE:
                pygame.draw.rect(canvas, constants.PURPLE, dims)
            elif board_arr[row][column] == constants.PLAYER2_VALUE:
                pygame.draw.rect(canvas, constants.ORANGE, dims)

def draw_pieces(canvas, active_player, opponent):
    row, column = 0, 0
    a_pieces = active_player.remaining_pieces
    o_pieces = opponent.remaining_pieces
    if active_player.number == 1:
        for piece in a_pieces.keys():
            for j in range(a_pieces[piece]["arr"].shape[1]):
                for i in range(a_pieces[piece]["arr"].shape[0]):
                    if a_pieces[piece]["arr"][i][j] == 1:
                        x = (one_piece_box_width * column) + ((MARGIN + single_piece_width) * j) + MARGIN
                        y = info_box_height + (one_piece_box_height * row) + ((MARGIN + single_piece_height) * i)
                        for n in range(int(y - MARGIN), int(y + MARGIN + 1)):
                            for m in range(int(x - MARGIN), int(x + MARGIN + 1)):
                                dims_m = [m, n, single_piece_width, single_piece_height]
                                pygame.draw.rect(canvas, constants.WHITE, dims_m)
                        dims = [x, y, single_piece_width, single_piece_height]
                        pygame.draw.rect(canvas, constants.PURPLE, dims)
            column += 1
            if column == 2:
                row += 1
                column = 0
        row, column = 0, 0
        for piece in o_pieces.keys():
            for j in range(o_pieces[piece]["arr"].shape[1]):
                for i in range(o_pieces[piece]["arr"].shape[0]):
                    if o_pieces[piece]["arr"][i][j] == 1:
                        x = piece_box_width + board_width + (one_piece_box_width * column) + ((MARGIN + single_piece_width) * j) + MARGIN
                        y = info_box_height + (one_piece_box_height * row) + ((MARGIN + single_piece_height) * i)
                        for m in range(int(x - MARGIN), int(x + MARGIN + 1)):
                            for n in range(int(y - MARGIN), int(y + MARGIN + 1)):
                                dims_m = [m, n, single_piece_width, single_piece_height]
                                pygame.draw.rect(canvas, constants.WHITE, dims_m)
                        dims = [x, y, single_piece_width, single_piece_height]
                        pygame.draw.rect(canvas, constants.ORANGE, dims)
            column += 1
            if column == 2:
                row += 1
                column = 0
        row, column = 0, 0
    elif active_player.number == 2:
        for piece in o_pieces.keys():
            for j in range(o_pieces[piece]["arr"].shape[1]):
                for i in range(o_pieces[piece]["arr"].shape[0]):
                    if o_pieces[piece]["arr"][i][j] == 1:
                        x = (one_piece_box_width * column) + ((MARGIN + single_piece_width) * j) + MARGIN
                        y = info_box_height + (one_piece_box_height * row) + ((MARGIN + single_piece_height) * i)
                        for n in range(int(y - MARGIN), int(y + MARGIN + 1)):
                            for m in range(int(x - MARGIN), int(x + MARGIN + 1)):
                                dims_m = [m, n, single_piece_width, single_piece_height]
                                pygame.draw.rect(canvas, constants.WHITE, dims_m)
                        dims = [x, y, single_piece_width, single_piece_height]
                        pygame.draw.rect(canvas, constants.PURPLE, dims)
            column += 1
            if column == 2:
                row += 1
                column = 0
        row, column = 0, 0
        for piece in a_pieces.keys():
            for j in range(a_pieces[piece]["arr"].shape[1]):
                for i in range(a_pieces[piece]["arr"].shape[0]):
                    if a_pieces[piece]["arr"][i][j] == 1:
                        x = piece_box_width + board_width + (one_piece_box_width * column) + ((MARGIN + single_piece_width) * j) + MARGIN
                        y = info_box_height + (one_piece_box_height * row) + ((MARGIN + single_piece_height) * i) + MARGIN
                        for m in range(int(x - MARGIN), int(x + MARGIN + 1)):
                            for n in range(int(y - MARGIN), int(y + MARGIN + 1)):
                                dims_m = [m, n, single_piece_width, single_piece_height]
                                pygame.draw.rect(canvas, constants.WHITE, dims_m)
                        dims = [x, y, single_piece_width, single_piece_height]
                        pygame.draw.rect(canvas, constants.ORANGE, dims)
            column += 1
            if column == 2:
                row += 1
                column = 0
        row, column = 0, 0

def draw_infobox(screen, active_player, opponent):
    font = pygame.font.SysFont("Trebuchet MS", 30)
    if active_player.number == 1:
        text1 = font.render("Player 1 Score: "+str(active_player.score), True, constants.WHITE)
        text2 = font.render("Player 2 Score: "+str(opponent.score), True, constants.WHITE)
        pos1 = pygame.Rect((0, 0, piece_box_width, info_box_height))
        pos2 = pygame.Rect((piece_box_width + board_width, 0, piece_box_width, info_box_height))
    screen.blit(text1, text1.get_rect(center = pos1.center))
    screen.blit(text2, text2.get_rect(center = pos2.center))
    current_time = str(pygame.time.get_ticks() / 1000)
    
    text_center = font.render("Blokus on Pygame", False, constants.WHITE)
    pos_center = pygame.Rect((0, 0, info_box_width, info_box_height))
    #screen.fill(constants.BLACK)
    screen.blit(text_center, text_center.get_rect(center = pos_center.center))
