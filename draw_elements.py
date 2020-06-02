import pygame
import constants

#This file handles generation of all the sizes of the elements
#The values have been optimised for 1280*720 window area
piece_box_width = round(0.35 * constants.WINDOW_WIDTH) #450
single_piece_width = piece_box_width / 3 #150
board_width = constants.WINDOW_WIDTH - (2 * piece_box_width) #380
info_box_width = constants.WINDOW_WIDTH #1280

piece_box_height = 0.875 * constants.WINDOW_HEIGHT #630
single_piece_height = piece_box_height / 7 #90
board_height = piece_box_height #630
info_box_height = constants.WINDOW_HEIGHT - board_height #90

def draw_main_window():
    pass

def grid_to_array_coords():
    #column = pos[0] // (WIDTH + MARGIN)
    #row = pos[1] // (HEIGHT + MARGIN)
    #gameboard[row][column] = 1
    pass

def array_to_grid_coords():
    pass

def draw_gameboard(board_arr, screen):
    # This sets the WIDTH and HEIGHT of each grid location
    WIDTH = 25
    HEIGHT = 25
    MARGIN = 2

    for row in range(board_arr.shape[0]):
        for column in range(board_arr.shape[1]):
            box_width = piece_box_width + MARGIN + ((MARGIN + WIDTH) * column)
            box_height = info_box_height + MARGIN + ((MARGIN + HEIGHT) * row)
            dims = [box_width, box_height, WIDTH, HEIGHT]
            if board_arr[row][column] == -1:
                pygame.draw.rect(screen, constants.WHITE, dims)
            elif board_arr[row][column] == 1:
                pygame.draw.rect(screen, constants.GREEN, dims)

def draw_pieces(screen, active_player, opponent):
    row, column = 0, 0
    a_pieces = active_player.remaining_pieces
    o_pieces = opponent.remaining_pieces
    if active_player.number == 1:
        for piece in a_pieces.keys():
            for i in range(a_pieces[piece]["arr"].shape[0]):
                for j in range(a_pieces[piece]["arr"].shape[1]):
                    if a_pieces[piece]["arr"][i][j] == 1:
                        width = info_box_width * column
                        height = info_box_height * row
                        dims = [width, height, single_piece_width, single_piece_height]
                        pygame.draw.rect(screen, constants.PURPLE, dims)
            column += 1
            if column == 3:
                row += 1
                column = 0
        """for piece in o_pieces.keys():
            for i in range(o_pieces[piece]["arr"].shape[0]):
                for j in range(o_pieces[piece]["arr"].shape[1]):
                    if o_pieces[piece]["arr"][i][j] == 1:
                        width = info_box_width * column
                        height = info_box_height * row
                        dims = [width, height, single_piece_width, single_piece_height]
                        pygame.draw.rect(screen, constants.ORANGE, dims)
            column += 1
            if column == 3:
                row += 1
                column = 0"""