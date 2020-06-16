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

board_origin = [piece_box_width, info_box_height]

def draw_title_window():
    pass

def grid_to_array_coords():
    #column = pos[0] // (WIDTH + MARGIN)
    #row = pos[1] // (HEIGHT + MARGIN)
    #gameboard[row][column] = 1
    pass

def array_to_grid_coords():
    pass

def draw_gameboard(canvas, board_arr):
    mouse_row, mouse_col = get_square_under_mouse(board_arr)
    for row in range(board_arr.shape[0]):
        for column in range(board_arr.shape[1]):
            box_width = piece_box_width + MARGIN + ((MARGIN + board_box_width) * column)
            box_height = info_box_height + MARGIN + ((MARGIN + board_box_height) * row)
            dims = [box_width, box_height, board_box_width, board_box_height]
            rect = pygame.Rect(dims)
            if [row, column] == [mouse_row, mouse_col] and \
               board_arr[row][column] == constants.BOARD_FILL_VALUE:
                rect.x -= MARGIN
                rect.y -= MARGIN
                rect.h += 2*MARGIN
                rect.w += 2*MARGIN
                pygame.draw.rect(canvas, constants.GREEN, rect)
                rect.x += MARGIN
                rect.y += MARGIN
                rect.h -= 2*MARGIN
                rect.w -= 2*MARGIN
            
            if board_arr[row][column] == constants.BOARD_FILL_VALUE:
                pygame.draw.rect(canvas, constants.WHITE, rect)
            elif board_arr[row][column] == constants.PLAYER1_VALUE:
                pygame.draw.rect(canvas, constants.PURPLE, rect)
            elif board_arr[row][column] == constants.PLAYER2_VALUE:
                pygame.draw.rect(canvas, constants.ORANGE, rect)

def get_square_under_mouse(board_arr):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - board_origin
    x, y = [int(v // (board_box_width + MARGIN)) for v in mouse_pos]
    try:
        if x >= 0 and y >= 0: return [y, x]
    except IndexError: pass
    return [-1, -1]
    
def init_piece_rects(canvas, player1, player2):
    row, column = 0, 0
    p1_pieces, p2_pieces = player1.remaining_pieces, player2.remaining_pieces
    p1_rects, p2_rects, temp_rects = [], [], []
    
    for piece in p1_pieces.keys():
        piece_rects = []
        for j in range(p1_pieces[piece]["arr"].shape[1]):
            for i in range(p1_pieces[piece]["arr"].shape[0]):
                if p1_pieces[piece]["arr"][i][j] == 1:
                    x = (one_piece_box_width * column) + ((MARGIN + single_piece_width) * j) + MARGIN
                    y = info_box_height + (one_piece_box_height * row) + ((MARGIN + single_piece_height) * i)
                    piece_rects.append(pygame.Rect([x, y, single_piece_width, single_piece_height]))
        p1_rects.append(piece_rects)
        column += 1
        if column == 2:
            row += 1
            column = 0
    row, column = 0, 0
    for piece in p2_pieces.keys():
        piece_rects = []
        for j in range(p2_pieces[piece]["arr"].shape[1]):
            for i in range(p2_pieces[piece]["arr"].shape[0]):
                if p2_pieces[piece]["arr"][i][j] == 1:
                    x = piece_box_width + board_width + (one_piece_box_width * column) + ((MARGIN + single_piece_width) * j) + MARGIN
                    y = info_box_height + (one_piece_box_height * row) + ((MARGIN + single_piece_height) * i)
                    piece_rects.append(pygame.Rect([x, y, single_piece_width, single_piece_height]))
        p2_rects.append(piece_rects)
        column += 1
        if column == 2:
            row += 1
            column = 0
    return p1_rects, p2_rects

def generate_element_offsets(pieces, event):
    offset_list = []
    selected = None
    for i, piece in enumerate(pieces):
        for r in piece:
            if r.collidepoint(event.pos):
                selected = i
    if selected is not None:
        for chosen_piece in pieces[selected]:
            selected_offset_x = chosen_piece.x - event.pos[0]
            selected_offset_y = chosen_piece.y - event.pos[1]
            print(selected_offset_x, selected_offset_y)
            offset_list.append([selected_offset_x, selected_offset_y])
    return offset_list, selected

def draw_pieces(canvas, p1_rects, p2_rects, p1_color, p2_color):
    for piece in p1_rects:
        for unit_sq in piece:
            pygame.draw.rect(canvas, p1_color, unit_sq)
            unit_sq.x -= MARGIN
            unit_sq.y -= MARGIN
            pygame.draw.rect(canvas, constants.WHITE, unit_sq, MARGIN)
    for piece in p2_rects:
        for unit_sq in piece:
            pygame.draw.rect(canvas, p2_color, unit_sq)

def draw_infobox(canvas, player1, player2):
    font = pygame.font.SysFont("Trebuchet MS", 30)
    text1 = font.render("Player 1 Score: "+str(player1.score), True, constants.WHITE)
    text2 = font.render("Player 2 Score: "+str(player2.score), True, constants.WHITE)
    pos1 = pygame.Rect((0, 0, piece_box_width, info_box_height))
    pos2 = pygame.Rect((piece_box_width + board_width, 0, piece_box_width, info_box_height))
    canvas.blit(text1, text1.get_rect(center = pos1.center))
    canvas.blit(text2, text2.get_rect(center = pos2.center))
    current_time = str(pygame.time.get_ticks() / 1000)
    
    text_center = font.render("Blokus on Pygame", False, constants.WHITE)
    pos_center = pygame.Rect((0, 0, info_box_width, info_box_height))
    #canvas.fill(constants.BLACK)
    canvas.blit(text_center, text_center.get_rect(center = pos_center.center))
