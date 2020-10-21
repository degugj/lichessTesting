"""
-------------------------------
IMPORTS
-------------------------------
"""
import pygame as pg
import time

from Engine.chessboard import gameState as gs
#import gameState as gs

"""
-------------------------------
DEFINITIONS AND VARIABLES 
-------------------------------
"""
WIN_WIDTH = 850
WIN_HEIGHT = 750
CB_WIDTH = CB_HEIGHT = 512
DIMENSIONS = 8
MAX_FPS = 15

xchessboardOffset = (WIN_WIDTH - CB_WIDTH) // 2
ychessboardOffset = (WIN_HEIGHT - CB_HEIGHT) // 2
cellSize = CB_HEIGHT // DIMENSIONS

leftbufferOffset = (xchessboardOffset - (2*cellSize)) // 2
rightbufferOffset = WIN_WIDTH - (2*cellSize) - leftbufferOffset


images = {}


"""
-------------------------------
FUNCTIONS
-------------------------------
"""

""" init_chessboard():
	params:
	return:
"""
def init_chessboard(challengerName):

	# init pygame and set window title and icon
	pg.init()
	pg.display.set_caption('MagiChess: Challenger Game')
	icon = pg.image.load("Engine/chessboard/chessboard_images/wQ.png")
	pg.display.set_icon(icon)

	# set window dimensions and color, and create clock
	screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	screen.fill(pg.Color("white"))
	clock = pg.time.Clock()
	
	# load chesspiece images into dictionary
	load_images()

	# create gamestate object
	gamestate = gs.GameState()

	# on-screen text
	leftbuffertextOffset = 	(WIN_WIDTH - CB_WIDTH) // 4
	rightbuffertextOffset =  WIN_WIDTH - leftbuffertextOffset
	display_text(screen, "Currently Playing: " + challengerName, (0,0,0), 20, WIN_WIDTH // 2, 40)
	display_text(screen, "White Capture Buffer", (0,0,0), 15, leftbuffertextOffset, ychessboardOffset-25)
	display_text(screen, "Black Capture Buffer", (0,0,0), 15, rightbuffertextOffset, ychessboardOffset-25)

	# always run until quit event
	run = True
	while run:
		for e in pg.event.get():
			if e.type == pg.QUIT:
				run = False

		draw_gamestate(screen, gamestate)

		# set max number of frames per second and update display
		clock.tick(MAX_FPS)
		pg.display.flip()

	pg.display.quit()
	pg.quit()


""" load_images: loads chesspiece images into images dictionary
	params:
	return:
"""
def load_images():
	pieces = ['wP', 'wR', 'wH', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bH', 'bB', 'bK', 'bQ']
	# fill images dictionary with pieces and corresponding images
	for piece in pieces:
		image = pg.image.load("Engine/chessboard/chessboard_images/" + piece + ".png")
		images[piece] = pg.transform.scale(image, (cellSize, cellSize))


""" draw_gamestate
	params:
		screen - game window
	return:
"""
def draw_gamestate(screen, gamestate):
	gamestate.update_gamestate()
	draw_board(screen)
	draw_buffers(screen)
	draw_pieces(screen, gamestate.board)
	return


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
			# draw chess board; offsets used to center the board
			pg.draw.rect(screen, color, pg.Rect(column*cellSize + xchessboardOffset, row*cellSize + ychessboardOffset, cellSize, cellSize))
	return

""" draw_buffers: draw the capture buffers on either side of the board
	params:
		screen
	return:
"""
def draw_buffers(screen):
	colors = [pg.Color("grey"), pg.Color("dark grey")]
	# both left/right buffers will be 8x2
	for row in range(8):
		for column in range(2):
			color = colors[(row+column) % 2]
			# place left buffer
			pg.draw.rect(screen, color, pg.Rect(column*cellSize + leftbufferOffset, row*cellSize + ychessboardOffset, cellSize, cellSize))
			# place right buffer
			pg.draw.rect(screen, color, pg.Rect(column*cellSize + rightbufferOffset, row*cellSize + ychessboardOffset, cellSize, cellSize))
	return


""" draw_pieces: draw game pieces on top of the chess board
	params:
		screen - game window
		gamestate - curernt local game state of board
	return:
"""
def draw_pieces(screen, gamestate_board):
	for row in range(DIMENSIONS):
		for column in range(DIMENSIONS):
			piece = gamestate_board[row][column]
			if piece != "--":
				# draw pieces on top of the board; offsets used to center pieces into correct cells
				screen.blit(images[piece], (column*cellSize + xchessboardOffset, row*cellSize + ychessboardOffset, cellSize, cellSize))
	return


""" display_text: displays desired text to screen
	params:
		screen - game window
		message - text contents
		color - color of text
	return
"""
def display_text(screen, message, color, size, x, y):
	font = pg.font.Font("freesansbold.ttf", size)
	textSurface = font.render(message, True, color)
	textBox = textSurface.get_rect()
	textBox.center = x, y
	screen.blit(textSurface, textBox)

