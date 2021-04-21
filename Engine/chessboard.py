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
WIN_WIDTH = 720
WIN_HEIGHT = 480
CB_WIDTH = CB_HEIGHT = 360
DIMENSIONS = 8
BUFFER_DIMENSIONSx = 2
BUFFER_DIMENSIONSy = 8
MAX_FPS = 15

# size of single cell
cellSize = CB_HEIGHT // DIMENSIONS
# chessboard coordinates (x offset, y offset)
chessboardCoords = ((WIN_WIDTH - CB_WIDTH) // 2, (WIN_HEIGHT - CB_HEIGHT) // 4)

offsetFifteen = WIN_HEIGHT/32

# buffer coordinates (left buffer x offset, right buffer x offset)
leftbufferCoords = (chessboardCoords[0] - (2*cellSize)) // 2
bufferCoords = (leftbufferCoords, WIN_WIDTH - (2*cellSize) - leftbufferCoords)

# alert window coordinates
alertwindowCoords = (chessboardCoords[0], (chessboardCoords[1] + CB_HEIGHT) + 30)

# button coordinate offsets
resignbuttonCoords = (bufferCoords[0], chessboardCoords[1]+CB_HEIGHT+offsetFifteen)
abortbuttonCoords = (bufferCoords[1], chessboardCoords[1]+CB_HEIGHT+offsetFifteen)

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
    
    replay = gamestate.replay

    # load chesspiece images into dictionary
    load_images()

    # on-screen text
    draw_gametext(screen, challengerName, gamestate)

    # draw buttons
    draw_userbuttons(screen, replay)
    
    audio.sound_gamestart()

    # always run until quit event
    run = draw = True

    # up_gs_process = mp.Process(target=updating_gamestate, args=(gamestate,))
    # up_gs_process.start()
    # print("updating gs PID: ", up_gs_process.pid)
    
    while run:        

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                draw = False

            # check for mouse click event
            elif event.type == pg.MOUSEBUTTONDOWN:
                print("button pressed")
                # get position of mouse, and check if hovering button
                mouse = pg.mouse.get_pos()
                # check if mouse hovering button
                button = check_buttons(screen, mouse, gamestate)
                if button == "resign" and not replay:
                    # user has resigned the game
                    if gameover(("resign", gamestate.get_opponentcolor()), gamestate):
                        draw = False
                        run = False
                        time.sleep(3)
                        break
                if button == "abort" and not replay:
                    # user has aborted the game
                    if gameover(("abort", gamestate.get_opponentcolor()), gamestate):
                        draw = False
                        run = False
                        time.sleep(3)
                        break
                if button == "quit":
                    draw = False
                    run = False


        if draw:

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

                draw = False

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
    display_text(screen, "Currently Playing: " + challengerName, (0,0,0), 20, WIN_WIDTH // 2, chessboardCoords[1]-offsetFifteen)
    display_text(screen, "White Capture Buffer", (0,0,0), 15, leftbuffertextOffset, chessboardCoords[1]-offsetFifteen)
    display_text(screen, "Black Capture Buffer", (0,0,0), 15, rightbuffertextOffset, chessboardCoords[1]-offsetFifteen)

    # letter and number coordinates
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    numbers = list(range(1,9))
    if gamestate.get_usercolor() == 'black':
        letters = letters[::-1]
        numbers = numbers[::-1]
    
    # find letter offsets and draw
    letterOffsetx = chessboardCoords[0] + (cellSize//2)
    letterOffsety = chessboardCoords[1] + CB_HEIGHT + offsetFifteen//2
    for letter in letters:
        display_text(screen, letter, (255,0,0), 12, letterOffsetx, letterOffsety)
        letterOffsetx += cellSize

    # find number offsets and draw
    numberOffsetx = chessboardCoords[0] + CB_WIDTH + offsetFifteen//2
    numberOffsety = chessboardCoords[1] + CB_HEIGHT - (cellSize//2)
    for number in numbers:
        display_text(screen, str(number), (255,0,0), 12, numberOffsetx, numberOffsety)
        numberOffsety -= cellSize

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


""" draw_userbuttons: draws all buttons for the user
    params: screen
    return:
"""
def draw_userbuttons(screen, replay):
    
    # pg.draw.rect(screen, pg.Color("white"), pg.Rect(abortbuttonCoords[0], abortbuttonCoords[1], 
    #                 cellSize*2, cellSize//2))

    if replay:
        # quit button
        draw_button(screen, pg.Color("red"), abortbuttonCoords[0], abortbuttonCoords[1], 
                    cellSize*2, cellSize//2, "Exit")
    else:
        # resign button
        draw_button(screen, pg.Color("grey"), resignbuttonCoords[0], resignbuttonCoords[1], 
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


""" remove_button: remove a button
    params: screen, x, y 
    return:
"""
def remove_button(screen, x, y, length, height):
    # whiteout the button's coordinate locations
    pg.draw.rect(screen, pg.Color("white"), pg.Rect(x, y, length, height))
    return

""" check_buttons: called when game checks for mouse clicks
    params: screen, mouse (mouse location)
    return:
"""
def check_buttons(screen, mouse, gamestate):
    # check if button hovering resign game button
    if not gamestate.replay:
        if resignbuttonCoords[0] < mouse[0] < (resignbuttonCoords[0] + cellSize*2) and resignbuttonCoords[1] < mouse[1] < (resignbuttonCoords[1]) + cellSize//2:
            return "resign"
        # check if button hovering is abort button
        if gamestate.turn < 2 and abortbuttonCoords[0] < mouse[0] < (abortbuttonCoords[0] + cellSize*2) and abortbuttonCoords[1] < mouse[1] < (abortbuttonCoords[1] + cellSize//2):
            return "abort"
    elif abortbuttonCoords[0] < mouse[0] < (abortbuttonCoords[0]+cellSize*2) and abortbuttonCoords[1] < mouse[1] < (abortbuttonCoords[1] + cellSize//2):
        return "quit"



""" display_alert: display alert text in alerts window
    params:
    return:
"""
def display_alert(message):
    # clear alert section
    global screen
    pg.draw.rect(screen, pg.Color("white"), pg.Rect(alertwindowCoords[0], alertwindowCoords[1], CB_WIDTH, cellSize))
    # display alert message
    display_text(screen, message, pg.Color("black"), 15, WIN_WIDTH//2, alertwindowCoords[1]+10)
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
            # if row == startCell[0] and column == startCell[1] or row == destCell[0] and column == destCell[1]:
            #     color = pg.Color("Khaki") 
            color = colors[(row+column) % 2]
            # draw chess board; offsets used to center the board
            pg.draw.rect(screen, color, pg.Rect(column*cellSize + chessboardCoords[0], row*cellSize + chessboardCoords[1], cellSize, cellSize))
            # highlight cells
            color_cells(coloredCells, "Khaki")

    return


""" color_cells: draw colored cells on the board
    params: screen
    return:
"""
def color_cells(coloredCells, c):
    global screen
    for cell in coloredCells:
        x = cell[0]
        y = cell[1]
        if x != -1 and y != -1:
            color = pg.Color(c)
            pg.draw.rect(screen, color, pg.Rect(y*cellSize + chessboardCoords[0], x*cellSize + chessboardCoords[1], cellSize, cellSize))


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


""" gameover: game has ended
    params: reason (tuple: (reason, winner_color)), gamestate
    return:
"""
def gameover(reason, gamestate):
    
    if reason == 'replay_over':
        pass
    # user has won
    elif reason[1] == gamestate.get_usercolor():
        # play victory tone
        audio.sound_victory()
        # opponent has resigned
        if reason[0] == "resign":
            # display message
            gamestate.message = "GAME OVER! The opponent has resigned and you have won!"

        # opponent has aborted
        if reason[0] == "abort":
            # display message
            gamestate.message = "GAME OVER! The opponent has aborted the match!"

        # user won by checkmate
        if reason[0] == "mate":
            gamestate.message = "GAME OVER! You have won by checkmate!"

    # opponent has won
    else:
        # play defeat tone
        audio.sound_defeat()
        # user has resigned
        if reason[0] == "resign":
            # send to lichess server
            if lichessinterface.gameover("resign", screen):
                gamestate.message = "GAME OVER! You have resigned and the opponent has won."
            
        # user has aborted  
        if reason[0] == "abort":
            # send to lichess server
            if lichessinterface.gameover("abort", screen):
                gamestate.message = "GAME OVER! You have aborted the game."
            
        # opponent won by checkmate
        if reason[0] == "mate":
            gamestate.message = "GAME OVER! The opponent has won by checkmate!"


    display_alert(gamestate.message)

"""
updating and drawing gamestate on screen
"""
def updating_gamestate(gamestate):
    return
    
# quit pygame module
def terminate_pygame():
    pg.quit()
    return