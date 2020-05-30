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
    pass

def array_to_grid_coords():
    pass

def draw_gameboard(gameboard, screen):
    # This sets the WIDTH and HEIGHT of each grid location
    WIDTH = 25
    HEIGHT = 25
    MARGIN = 2

    for row in range(gameboard.shape[0]):
        for column in range(gameboard.shape[1]):
            box_width = piece_box_width + MARGIN + ((MARGIN + WIDTH) * column)
            box_heght = info_box_height + MARGIN + ((MARGIN + HEIGHT) * row)
            dims = [box_width, box_heght, WIDTH, HEIGHT]
            if gameboard[row][column] == -1:
                pygame.draw.rect(screen, constants.WHITE, dims)
            elif gameboard[row][column] == 1:
                pygame.draw.rect(screen, constants.GREEN, dims)