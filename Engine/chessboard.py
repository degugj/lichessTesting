"""
-------------------------------
IMPORTS
-------------------------------
"""
import pygame as pg
import multiprocessing as mp
import time

from Engine import gameState as gs, gui_pages as pages, audio
from Engine.lichess import lichessInterface_new as lichessinterface

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

# size of single cell
cellSize = CB_HEIGHT // DIMENSIONS
# chessboard coordinates (x offset, y offset)
chessboardCoords = ((WIN_WIDTH - CB_WIDTH) // 2, (WIN_HEIGHT - CB_HEIGHT) // 4)

# buffer coordinates (left buffer offset, right buffer offset)
leftbufferCoords = (chessboardCoords[0] - (2*cellSize)) // 2
bufferCoords = (leftbufferCoords, WIN_WIDTH - (2*cellSize) - leftbufferCoords)

# alert window coordinates
alertwindowCoords = (chessboardCoords[0], (WIN_HEIGHT - chessboardCoords[1]) - 50)

# button coordinate offsets
resignbuttonCoords = (chessboardCoords[0] + cellSize*3, alertwindowCoords[1] - 40)
abortbuttonCoords = (resignbuttonCoords[0] + cellSize*3, resignbuttonCoords[1])

# dictionary to hold images
images = {}

screen = None

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
	global screen
	screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	screen.fill(pg.Color("white"))
	clock = pg.time.Clock()
	
	# load chesspiece images into dictionary
	load_images()

	# on-screen text
	draw_gametext(screen, challengerName, gamestate)

	# draw section for alerts
	color = pg.Color("light grey")
	pg.draw.rect(screen, color, pg.Rect(alertwindowCoords[0], alertwindowCoords[1], CB_WIDTH, cellSize+30))

	audio.sound_gamestart()

	# always run until quit event
	run = draw = True
	while run:

		# check pygame events (ex. close window, mouse click)
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
					if gameover(("resign", gamestate.get_opponentcolor()), gamestate):
						draw = False
						run = False
						time.sleep(3)
						break
				if button == "abort":
					# user has aborted the game
					if gameover(("abort", gamestate.get_opponentcolor()), gamestate):
						draw = False
						run = False
						time.sleep(3)
						break

		if draw:

			# draw buttons
			draw_userbuttons(screen)

			# draw chessboard, buffer zones, pieces
			draw_gamestate(screen, gamestate)

			# set max number of frames per second and update display
			clock.tick(MAX_FPS)
			pg.display.flip()

			display_alert(gamestate.message)

			# update gamestate of the board (i.e user/opponent makes move)
			gamestateUpdate = gamestate.update_gamestate()

			if gamestateUpdate != 'ok':
				draw_gamestate(screen, gamestate)
				gameover(gamestateUpdate, gamestate)
				time.sleep(3)
				run = False

	# terminate gamestream
	pages.terminate_gamestream()
	# quit pygame
	pg.display.quit()


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
	display_text(screen, "White Capture Buffer", (0,0,0), 15, leftbuffertextOffset, chessboardCoords[1]-25)
	display_text(screen, "Black Capture Buffer", (0,0,0), 15, rightbuffertextOffset, chessboardCoords[1]-25)

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
	draw_button(screen, pg.Color("blue"), resignbuttonCoords[0], resignbuttonCoords[1], 
					cellSize*2, cellSize//2, "Resign Game")
	# abort button
	draw_button(screen, pg.Color("red"), abortbuttonCoords[0], abortbuttonCoords[1], 
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
	if resignbuttonCoords[0] < mouse[0] < (resignbuttonCoords[0] + cellSize*2) and resignbuttonCoords[1] < mouse[1] < (resignbuttonCoords[1]) + cellSize//2:
		# change button color if pressed
		draw_button(screen, pg.Color("grey"), resignbuttonCoords[0], resignbuttonCoords[1], 
					cellSize*2, cellSize//2, "Resign Game")
		time.sleep(0.5)
		return "resign"
	# check if button hovering is abort button
	if abortbuttonCoords[0] < mouse[0] < (abortbuttonCoords[0] + cellSize*2) and abortbuttonCoords[1] < mouse[1] < (abortbuttonCoords[1] + cellSize//2):
		# change button color if pressed
		draw_button(screen, pg.Color("grey"), abortbuttonCoords[0], abortbuttonCoords[1], 
					cellSize*2, cellSize//2, "Abort Game")
		time.sleep(0.5)
		return "abort"


""" display_alert: display alert text in alerts window
	params:
	return:
"""
def display_alert(message):
	# clear alert section
	global screen
	pg.draw.rect(screen, pg.Color("light grey"), pg.Rect(alertwindowCoords[0], alertwindowCoords[1], CB_WIDTH, cellSize+30))
	# display alert message
	display_text(screen, message, pg.Color("black"), 15, WIN_WIDTH//2, alertwindowCoords[1]+30)
	pg.display.flip()

	return


""" draw_gamestate
	params: screen
	return:
"""
def draw_gamestate(screen, gamestate):

	draw_board(screen, gamestate.coloredCells)
	draw_buffers(screen)
	draw_pieces(screen, gamestate)

	return


""" draw_board
	params: screen
	return:
"""
def draw_board(screen, coloredCells):
	startCell = coloredCells[0]
	destCell = coloredCells[1]
	# alternate board cell colors
	colors = [pg.Color("white"), pg.Color("dark grey")]
	for row in range(DIMENSIONS):
		for column in range(DIMENSIONS):
			if row == startCell[0] and column == startCell[1] or row == destCell[0] and column == destCell[1]:
				color = pg.Color("Khaki") 
			else:
				color = colors[(row+column) % 2]
			# draw chess board; offsets used to center the board
			pg.draw.rect(screen, color, pg.Rect(column*cellSize + chessboardCoords[0], row*cellSize + chessboardCoords[1], cellSize, cellSize))

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
			pg.draw.rect(screen, color, pg.Rect(column*cellSize + bufferCoords[0], row*cellSize + chessboardCoords[1], cellSize, cellSize))
			# place right buffer
			pg.draw.rect(screen, color, pg.Rect(column*cellSize + bufferCoords[1], row*cellSize + chessboardCoords[1], cellSize, cellSize))
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
				screen.blit(images[piece], (column*cellSize + chessboardCoords[0], row*cellSize + chessboardCoords[1], cellSize, cellSize))

	# pieces on the capture zones
	for row in range(BUFFER_DIMENSIONSy):
		for column in range(BUFFER_DIMENSIONSx):
			# draw white pieces
			whitePiece = gamestate.wBuffer[row][column]
			if whitePiece != "--":
				screen.blit(images[whitePiece], (column*cellSize + bufferCoords[0], row*cellSize + chessboardCoords[1], cellSize, cellSize))
			# draw black pieces
			blackPiece = gamestate.bBuffer[row][column]
			if blackPiece != "--":
				screen.blit(images[blackPiece], (column*cellSize + bufferCoords[1], row*cellSize + chessboardCoords[1], cellSize, cellSize))

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


""" gameover: game has ended
	params: screen (pygame screen), reason (tuple: (winner, reason)), gamestate
	return:
"""
def gameover(reason, gamestate):
	# user has won
	if reason[1] == gamestate.get_usercolor():
		# play victory tone
		audio.sound_victory()
		# opponent has resigned
		if reason[0] == "resign":
			# display message
			gamestate.message = "GAME OVER! The opponent has resigned and you have won!"

		# opponent has aborted
		if reason[0] == "abort":
			# display message
			gamestate.message = "GAME OVER! The opponent has resigned and you have won!"

		# user won by checkmate
		if reason[0] == "mate":
			gamestate.message = "GAME OVER! The opponent has resigned and you have won!"

	# opponent has won
	else:
		# play defeat tone
		audio.sound_defeat()
		# user has resigned
		if reason[0] == "resign":
			# send to lichess server
			if lichessinterface.gameover("resign", screen):
				gamestate.message = "GAME OVER! The opponent has resigned and you have won!"
			
		# user has aborted  
		if reason[0] == "abort":
			# send to lichess server
			if lichessinterface.gameover("abort", screen):
				gamestate.message = "GAME OVER! The opponent has resigned and you have won!"
			
		# opponent won by checkmate
		if reason[0] == "mate":
			gamestate.message = "GAME OVER! The opponent has resigned and you have won!"


	display_alert(gamestate.message)


# quit pygame module
def terminate_pygame():
	pg.quit()
	return