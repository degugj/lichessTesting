"""
-------------------------------
IMPORTS
-------------------------------
"""
import pygame as pg
import multiprocessing as mp
import time

from Engine import gameState as gs
from Engine import gui_pages as pages

"""
-------------------------------
DEFINITIONS AND VARIABLES 
-------------------------------
"""
WIN_WIDTH = 850
WIN_HEIGHT = 750
CB_WIDTH = CB_HEIGHT = 512
DIMENSIONS = 8
BUFFER_DIMENSIONSx = 2
BUFFER_DIMENSIONSy = 8
MAX_FPS = 15

xchessboardOffset = (WIN_WIDTH - CB_WIDTH) // 2
ychessboardOffset = (WIN_HEIGHT - CB_HEIGHT) // 4
cellSize = CB_HEIGHT // DIMENSIONS

leftbufferOffset = (xchessboardOffset - (2*cellSize)) // 2
rightbufferOffset = WIN_WIDTH - (2*cellSize) - leftbufferOffset

alertwindowOffsetx = xchessboardOffset
alertwindowOffsety = (WIN_HEIGHT - ychessboardOffset) - 50

images = {}


"""
-------------------------------
FUNCTIONS
-------------------------------
"""

""" init_chessboard():
	params:
		challengerName - name of opponent
		gamestate - local gamestate object
	return:
"""
def init_chessboard(challengerName, gamestate):

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

	# draw Alerts window
	draw_alertswindow(screen)

	# on-screen text
	leftbuffertextOffset = 	(WIN_WIDTH - CB_WIDTH) // 4
	rightbuffertextOffset =  WIN_WIDTH - leftbuffertextOffset
	display_text(screen, "Currently Playing: " + challengerName, (0,0,0), 20, WIN_WIDTH // 2, 40)
	display_text(screen, "White Capture Buffer", (0,0,0), 15, leftbuffertextOffset, ychessboardOffset-25)
	display_text(screen, "Black Capture Buffer", (0,0,0), 15, rightbuffertextOffset, ychessboardOffset-25)


	# letter and number chess gridding
	letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
	numbers = list(range(1,9))
	if gamestate.get_usercolor() == 'b':
		letters = letters[::-1]
		numbers = numbers[::-1]
	

	letterOffsetx = ((WIN_WIDTH - CB_WIDTH)//2) + (cellSize//2)
	letterOffsety = WIN_HEIGHT - ((WIN_HEIGHT - CB_HEIGHT)//2) - 50
	for letter in letters:
		display_text(screen, letter, (255,0,0), 12, letterOffsetx, letterOffsety)
		letterOffsetx += 64

	numberOffsetx = WIN_WIDTH - ((WIN_WIDTH - CB_WIDTH)//2) + 10
	numberOffsety = WIN_HEIGHT - (3*(WIN_HEIGHT - CB_HEIGHT)//4) - (cellSize//2)
	for number in numbers:
		display_text(screen, str(number), (255,0,0), 12, numberOffsetx, numberOffsety)
		numberOffsety -= 64


	# always run until quit event
	run = draw = True
	while run:

		for event in pg.event.get():
			if event.type == pg.QUIT:
				run = False
				draw = False

		if draw:
			draw_gamestate(screen, gamestate)

			# set max number of frames per second and update display
			clock.tick(MAX_FPS)
			pg.display.flip()

			# update gamestate of the board (i.e user/opponent makes move)
			gamestateUpdate = gamestate.update_gamestate(screen)
			if gamestateUpdate != 'ok':
				display_gameover(screen, gamestateUpdate)
				pg.display.flip()
				time.sleep(10)
				break

	# terminate gamestream
	pages.terminate_gamestream()
	# quit pygame
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



""" draw_alertswindow: draw alerts window where alerts will appear
	params:
		screen
	return:
"""
def draw_alertswindow(screen):
	color = pg.Color("light grey")
	pg.draw.rect(screen, color, pg.Rect(alertwindowOffsetx, alertwindowOffsety, CB_WIDTH, cellSize+30))
	return

""" display_alert: display alert text in alerts window
	params:
	return:
"""
def display_alert(screen, message):
	draw_alertswindow(screen)
	font = pg.font.Font("freesansbold.ttf", 15)
	# center the text
	textSurface = font.render(message, True, pg.Color("black"))
	textBox = textSurface.get_rect()
	textBox.center = WIN_WIDTH//2, alertwindowOffsety + 30
	screen.blit(textSurface, textBox)


""" draw_gamestate
	params:
		screen - game window
	return:
"""
def draw_gamestate(screen, gamestate):

	draw_board(screen)
	draw_buffers(screen)
	draw_pieces(screen, gamestate)

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
def draw_pieces(screen, gamestate):
	# pieces on the board
	for row in range(DIMENSIONS):
		for column in range(DIMENSIONS):
			piece = gamestate.board[row][column]
			if piece != "--":
				# draw pieces on top of the board; offsets used to center pieces into correct cells
				screen.blit(images[piece], (column*cellSize + xchessboardOffset, row*cellSize + ychessboardOffset, cellSize, cellSize))

	# pieces on the capture zones
	for row in range(BUFFER_DIMENSIONSy):
		for column in range(BUFFER_DIMENSIONSx):
			# draw white pieces
			whitePiece = gamestate.wBuffer[row][column]
			if whitePiece != "--":
				screen.blit(images[whitePiece], (column*cellSize + leftbufferOffset, row*cellSize + ychessboardOffset, cellSize, cellSize))
			# draw black pieces
			blackPiece = gamestate.bBuffer[row][column]
			if blackPiece != "--":
				screen.blit(images[blackPiece], (column*cellSize + rightbufferOffset, row*cellSize + ychessboardOffset, cellSize, cellSize))

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
	# center the text
	textSurface = font.render(message, True, color)
	textBox = textSurface.get_rect()
	textBox.center = x, y
	screen.blit(textSurface, textBox)


""" display_gameover: displays game over screen
	params:
		screen - game window
		reason - reason for game over
"""
def display_gameover(screen, reason):
	# clear screen
	screen.fill(pg.Color("white"))

	# game over text
	if reason == "blackresign":
		text = "White has resigned. Black has won."
		color = pg.Color("red")
	elif reason == "whiteresign":
		text = "Black have resigned. White has won."
		color = pg.Color("green")
	elif reason == "whitemate":
		text = "White has won by checkmate"
		color = pg.Color("red")
	elif reason == "blackmate":
		text = "Black has won by checkmate."
		color = pg.Color("green")
	else:
		text = "Opponent has aborted the game. You win by default."
		color = pg.Color("black")

	display_text(screen, text, color, 25, WIN_WIDTH//2, WIN_HEIGHT//2)

