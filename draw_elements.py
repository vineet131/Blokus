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

board_origin = [info_box_height + MARGIN, piece_box_width + MARGIN]

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

def get_square_under_mouse(board_arr):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - board_origin
    x, y = [int(v // TILESIZE) for v in mouse_pos]
    try: 
        if x >= 0 and y >= 0: return (board[y][x], x, y)
    except IndexError: pass
    return None, None, None
    
def init_piece_rects(canvas, player1, player2):
    row, column = 0, 0
    p1_pieces, p2_pieces = player1.remaining_pieces, player2.remaining_pieces
    p1_rects, p2_rects, temp_rects = [], [], []
    
    for piece in p1_pieces.keys():
        for j in range(p1_pieces[piece]["arr"].shape[1]):
            for i in range(p1_pieces[piece]["arr"].shape[0]):
                if p1_pieces[piece]["arr"][i][j] == 1:
                    piece_rects = []
                    x = (one_piece_box_width * column) + ((MARGIN + single_piece_width) * j) + MARGIN
                    y = info_box_height + (one_piece_box_height * row) + ((MARGIN + single_piece_height) * i)
                    #The piece
                    piece_rects.append(pygame.Rect([x, y, single_piece_width, single_piece_height]))
                    #The boundaries of the piece
                    piece_rects.append(pygame.Rect([x - MARGIN, y - MARGIN, single_piece_width + 2*MARGIN, MARGIN]))
                    piece_rects.append(pygame.Rect([x - MARGIN, y, MARGIN, single_piece_height]))
                    piece_rects.append(pygame.Rect([x + single_piece_width, y, MARGIN, single_piece_height]))
                    piece_rects.append(pygame.Rect([x - MARGIN, y + single_piece_height, single_piece_width + 2*MARGIN, MARGIN]))
                    temp_rects.append(piece_rects)
        p1_rects.append(temp_rects)
        temp_rects = []
        column += 1
        if column == 2:
            row += 1
            column = 0
    row, column = 0, 0
    for piece in p2_pieces.keys():
        for j in range(p2_pieces[piece]["arr"].shape[1]):
            for i in range(p2_pieces[piece]["arr"].shape[0]):
                if p2_pieces[piece]["arr"][i][j] == 1:
                    piece_rects = []
                    x = piece_box_width + board_width + (one_piece_box_width * column) + ((MARGIN + single_piece_width) * j) + MARGIN
                    y = info_box_height + (one_piece_box_height * row) + ((MARGIN + single_piece_height) * i)
                    #The piece
                    piece_rects.append(pygame.Rect([x, y, single_piece_width, single_piece_height]))
                    #The boundaries of the piece
                    piece_rects.append(pygame.Rect([x - MARGIN, y - MARGIN, single_piece_width + 2*MARGIN, MARGIN]))
                    piece_rects.append(pygame.Rect([x - MARGIN, y, MARGIN, single_piece_height]))
                    piece_rects.append(pygame.Rect([x + single_piece_width, y, MARGIN, single_piece_height]))
                    piece_rects.append(pygame.Rect([x - MARGIN, y + single_piece_height, single_piece_width + 2*MARGIN, MARGIN]))
                    temp_rects.append(piece_rects)
        p2_rects.append(temp_rects)
        temp_rects = []
        column += 1
        if column == 2:
            row += 1
            column = 0
    return p1_rects, p2_rects

def generate_element_offsets(rects, event):
    offset_list = []
    selected = None
    for i, piece in enumerate(rects):
        for unit_sq in piece:
            for r in unit_sq:
                if r.collidepoint(event.pos):
                    selected = i
                    for chosen_piece in rects[selected]:
                        for chosen_unit_sq in chosen_piece:
                            selected_offset_x = chosen_unit_sq.x - event.pos[0]
                            selected_offset_y = chosen_unit_sq.y - event.pos[1]
                            offset_list.append([selected_offset_x, selected_offset_y])
    return offset_list, selected

def draw_pieces(canvas, p1_rects, p2_rects, p1_color, p2_color):
    for piece in p1_rects:
        for unit_sq in piece:
            pygame.draw.rect(canvas, p1_color, unit_sq[0])
            for i in range(1, 5):
                pygame.draw.rect(canvas, constants.WHITE, unit_sq[i])
    for piece in p2_rects:
        for unit_sq in piece:
            pygame.draw.rect(canvas, p2_color, unit_sq[0])
            for i in range(1, 5):
                pygame.draw.rect(canvas, constants.WHITE, unit_sq[i])

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
