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
from Engine.lichess import lichessInterface_new as lichessinterface

"""
-------------------------------
DEFINITIONS AND VARIABLES 
-------------------------------
"""
WIN_WIDTH = 850
WIN_HEIGHT = 650
CB_WIDTH = CB_HEIGHT = 512
DIMENSIONS = 8
BUFFER_DIMENSIONSx = 2
BUFFER_DIMENSIONSy = 8
MAX_FPS = 15

# chessboard coordinates and cellsize
xchessboardOffset = (WIN_WIDTH - CB_WIDTH) // 2
ychessboardOffset = (WIN_HEIGHT - CB_HEIGHT) // 4
cellSize = CB_HEIGHT // DIMENSIONS

# buffer coordinates
leftbufferOffset = (xchessboardOffset - (2*cellSize)) // 2
rightbufferOffset = WIN_WIDTH - (2*cellSize) - leftbufferOffset

# alert window coordinates
alertwindowOffsetx = xchessboardOffset
alertwindowOffsety = (WIN_HEIGHT - ychessboardOffset) - 50

# button coordinate offsets
resignButtonX = xchessboardOffset + cellSize*3
resignButtonY = alertwindowOffsety - 40
abortButtonX = resignButtonX + cellSize*3
abortButtonY = resignButtonY

images = {}

### CONVERT COORDINATES TO TUPLES???? ###

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

	# on-screen text
	draw_gametext(screen, challengerName, gamestate)

	# draw section for alerts
	color = pg.Color("light grey")
	pg.draw.rect(screen, color, pg.Rect(alertwindowOffsetx, alertwindowOffsety, CB_WIDTH, cellSize+30))

	# always run until quit event
	run = draw = True
	while run:

		# check for termination condition
		for event in pg.event.get():
			if event.type == pg.QUIT:
				run = False
				draw = False

			# check for mouse click event
			elif event.type == pg.MOUSEBUTTONDOWN:
				print("mouse button pressed")
				# get position of mouse, and check if hovering button
				mouse = pg.mouse.get_pos()
				# check if mouse hovering button
				button = check_buttons(screen, mouse)
				if button == "resign":
					# user has resigned the game
					if gameover(screen, "resign", gamestate.get_usercolor, gamestate):
						draw = False
				if button == "abort":
					# user has aborted the game
					if gameover(screen, "abort", gamestate.get_usercolor, gamestate):
						draw = False

		if draw:
			# draw buttons
			draw_userbuttons(screen)

			# draw chessboard, buffer zones, pieces
			draw_gamestate(screen, gamestate)

			# set max number of frames per second and update display
			clock.tick(MAX_FPS)
			pg.display.flip()

			# update gamestate of the board (i.e user/opponent makes move)
			gamestateUpdate = gamestate.update_gamestate(screen)
			if gamestateUpdate != 'ok':
				gameover(screen, gamestateUpdate)
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

	return


""" draw_gametext: draws the game text onto window
	params: screen (pygame screen), challengerName (name of opponent), gamestate (local gamestate of board)
	return:
"""
def draw_gametext(screen, challengerName, gamestate):
	# draw headings
	leftbuffertextOffset =  (WIN_WIDTH - CB_WIDTH) // 4
	rightbuffertextOffset =  WIN_WIDTH - leftbuffertextOffset
	display_text(screen, "Currently Playing: " + challengerName, (0,0,0), 20, WIN_WIDTH // 2, 40)
	display_text(screen, "White Capture Buffer", (0,0,0), 15, leftbuffertextOffset, ychessboardOffset-25)
	display_text(screen, "Black Capture Buffer", (0,0,0), 15, rightbuffertextOffset, ychessboardOffset-25)

	# draw letter and number coordinates
	letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
	numbers = list(range(1,9))
	if gamestate.get_usercolor() == 'b':
		letters = letters[::-1]
		numbers = numbers[::-1]
	
	# find letter offsets and draw
	letterOffsetx = ((WIN_WIDTH - CB_WIDTH)//2) + (cellSize//2)
	letterOffsety = WIN_HEIGHT - ((WIN_HEIGHT - CB_HEIGHT)//2) - 50
	for letter in letters:
		display_text(screen, letter, (255,0,0), 12, letterOffsetx, letterOffsety)
		letterOffsetx += 64

	# find number offsets and draw
	numberOffsetx = WIN_WIDTH - ((WIN_WIDTH - CB_WIDTH)//2) + 10
	numberOffsety = WIN_HEIGHT - (3*(WIN_HEIGHT - CB_HEIGHT)//4) - (cellSize//2)
	for number in numbers:
		display_text(screen, str(number), (255,0,0), 12, numberOffsetx, numberOffsety)
		numberOffsety -= 64

	return



""" draw_userbuttons: draws all buttons for the user
	params: screen
	return:
"""
def draw_userbuttons(screen):
	# resign button
	draw_button(screen, pg.Color("blue"), resignButtonX, resignButtonY, 
					cellSize*2, cellSize//2, "Resign Game")
	# abort button
	draw_button(screen, pg.Color("red"), abortButtonX, abortButtonY, 
					cellSize*2, cellSize//2, "Abort Game")

	return



""" draw_button: create a button
	params: screen, color, x, y, length, height, text
	return:
"""
def draw_button(screen, color, x, y, length, height, text):
	# draw button
	pg.draw.rect(screen, color, pg.Rect(x, y, length, height))
	# draw button text
	display_text(screen, text, pg.Color("black"), 12, x+length//2, y+height//2)

	return



""" check_buttons: called when game checks for mouse clicks
	params: screen, mouse (mouse location)
	return:
"""
def check_buttons(screen, mouse):
	# check if button hovering resign game button
	if resignButtonX < mouse[0] < (resignButtonX + cellSize*2) and resignButtonY < mouse[1] < (resignButtonY) + cellSize//2:
		# change button color if pressed
		draw_button(screen, pg.Color("grey"), resignButtonX, resignButtonY, 
					cellSize*2, cellSize//2, "Resign Game")
		time.sleep(0.5)
		return "resign"
	# check if button hovering is abort button
	if resignButtonX < mouse[0] < resignButtonX + cellSize*2 and resignButtonY < mouse[1] < (resignButtonY) + cellSize//2:
		# change button color if pressed
		draw_button(screen, pg.Color("grey"), abortButtonX, abortButtonY, 
					cellSize*2, cellSize//2, "Abort Game")
		time.sleep(0.5)
		return "abort"


""" display_alert: display alert text in alerts window
	params:
	return:
"""
def display_alert(screen, message):

	# clear alert section
	pg.draw.rect(screen, pg.Color("light grey"), pg.Rect(alertwindowOffsetx, alertwindowOffsety, CB_WIDTH, cellSize+30))
	# display alert message
	display_text(screen, message, pg.Color("black"), 15, WIN_WIDTH//2, alertwindowOffsety+30)

	return


""" draw_gamestate
	params: screen
	return:
"""
def draw_gamestate(screen, gamestate):

	draw_board(screen)
	draw_buffers(screen)
	draw_pieces(screen, gamestate)

	return


""" draw_board
	params: screen
	return:
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
	params: screen
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
	params: screen (pygame screen), gamestate (current local game state of board)
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
	params: screen (pygame screen), message (text contents), color (color of text)
	return:
"""
def display_text(screen, message, color, size, x, y):
	font = pg.font.Font("freesansbold.ttf", size)
	# center the text
	textSurface = font.render(message, True, color)
	textBox = textSurface.get_rect()
	textBox.center = x, y
	screen.blit(textSurface, textBox)


""" display_gameover: game has ended
	params: screen (pygame screen), reason (reason for game over), color (color of loser), gamestate
	return:
"""
def gameover(screen, reason, color, gamestate):

	# user has lost
	if gamestate.get_usercolor == color:
		# user has resigned
		if reason == "resign":
			if lichessinterface.gameover("resign"):
				display_alert(screen, "GAME OVER! You have lost due to resignation!")
			return
		# user has aborted
		if reason == "abort":
			if lichessinterface.gameover("abort"):
				display_alert(screen, "GAME OVER! You have aborted the game!")
			return
	else:
		# opponent has resigned
		if reason == "resign":
			display_alert(screen, "GAME OVER! The opponent has resigned and you have won!")
			return
		# opponent has aborted  
		if reason == "abort":
			display_alert(screen, "GAME OVER! The opponent has aborted the game!")
			return
			

