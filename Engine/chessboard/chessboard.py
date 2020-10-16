"""
-------------------------------
IMPORTS
-------------------------------
"""
import pygame as pg
import time

import gameState as gs
"""
-------------------------------
DEFINITIONS AND VARIABLES 
-------------------------------
"""
WIDTH = HEIGHT = 512
DIMENSIONS = 8
CELL_SIZE = HEIGHT // DIMENSIONS
MAX_FPS = 15

images = {}


"""
-------------------------------
FUNCTIONS
-------------------------------
"""

""" load_images: loads chesspiece images into images dictionary
params:
	none
return:
	none
"""
def load_images():
	pieces = ['wP', 'wR', 'wH', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bH', 'bB', 'bK', 'bQ']
	# fill images dictionary with pieces and corresponding images
	for piece in pieces:
		image = pg.image.load("chessboard_images/" + piece + ".png")
		images[piece] = pg.transform.scale(image, (CELL_SIZE, CELL_SIZE))

""" init_chessboard():
params:
	none
return:
	none
"""
def init_chessboard():

	# init pygame and set window title and icon
	pg.init()
	pg.display.set_caption('MagiChess: Challenger Game')
	icon = pg.image.load("chessboard_images/wQ.png")
	pg.display.set_icon(icon)

	# set window dimensions and color, and create clock
	screen = pg.display.set_mode((WIDTH, HEIGHT))
	screen.fill(pg.Color("white"))
	clock = pg.time.Clock()
	
	# load chesspiece images into dictionary
	load_images()

	# create gamestate object
	gamestate = gs.GameState()

	# always run until quit event
	run = True
	while run:
		for e in pg.event.get():
			if e.type == pg.QUIT:
				run = False

		draw_gamestate(screen, gamestate)
		clock.tick(MAX_FPS)
		pg.display.flip()


""" draw_gamestate
params:
	screen - game window
return:
	none
"""
def draw_gamestate(screen, gamestate):
	draw_board(screen)
	draw_pieces(screen, gamestate.board)


""" draw_board
params:
	screen - game window
return:
	none
"""
def draw_board(screen):
	colors = [pg.Color("white"), pg.Color("dark grey")]
	for row in range(DIMENSIONS):
		for column in range(DIMENSIONS):
			color = colors[(row+column) % 2]
			pg.draw.rect(screen, color, pg.Rect(column*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE))


""" draw_pieces
params:
	screen - game window
	gamestate - curernt local game state of board
return:
	none
"""
def draw_pieces(screen, gamestate_board):
	for row in range(DIMENSIONS):
		for column in range(DIMENSIONS):
			piece = gamestate_board[row][column]
			if piece != "--":
				screen.blit(images[piece], (column*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
	return
 
 init_chessboard()