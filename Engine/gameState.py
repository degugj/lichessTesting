# Weishan Li
# Jack DeGuglielmo
# September 2020
# Description: GameState class for storing the local state of the chess board

"""
-------------------------------
IMPORTS
-------------------------------
"""
import time

import pygame as pg

from Engine.lichess import lichessInterface_new as interface


"""
-------------------------------
GameState Class
-------------------------------
"""
class GameState():
    def __init__(self, gameQueue):

        # set user color (i.e 'w', 'b')
        self.gameQueue = gameQueue
        if self.gameQueue.get()["white"]["id"] == 'degugbot':     # <---------------------------------------------------------------------------------------DEGUGJ-----------------------------------
            self.userColor = 'w'
        else:
            self.userColor = 'b'

        # letter and number conversion to index self.board
        self.letter_to_y = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        self.number_to_x = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}

        # board state                      
        self.board = [
            ["bR", "bH", "bB", "bQ", "bK", "bB", "bH", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wH", "wB", "wQ", "wK", "wB", "wH", "wR"]]

        self.userMove = True

        # if user starts game as black
        if self.userColor == 'b':
            # letter and number conversion to index self.board
            self.letter_to_y = {'a':7, 'b':6, 'c':5, 'd':4, 'e':3, 'f':2, 'g':1, 'h':0}
            self.number_to_x = {'1':0, '2':1, '3':2, '4':3, '5':4, '6':5, '7':6, '8':7}

            # board state
            self.board = [
                ["wR", "wH", "wB", "wK", "wQ", "wB", "wH", "wR"],
                ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                ["bR", "bH", "bB", "bK", "bQ", "bB", "bH", "bR"]]

            self.userMove = False

        self.defaultState = self.board


        # capture buffer zones
        self.whiteBuffer = [["--", "--"],
                            ["--", "--"],
                            ["--", "--"],
                            ["--", "--"],
                            ["--", "--"],
                            ["--", "--"],
                            ["--", "--"],
                            ["--", "--"]]

        self.blackBuffer = [["--", "--"],
                            ["--", "--"],
                            ["--", "--"],
                            ["--", "--"],
                            ["--", "--"],
                            ["--", "--"],
                            ["--", "--"],
                            ["--", "--"]]
        # dictionary that maps bishop to row 4, knight to row 5, rook to row 6, and queen to row 7
        self.bufferMap = {'B':4, 'H':5, 'R':6, 'Q':7}

        # indicates if game is in first turn; used during get_opponentturn
        self.firstTurn = True
        # keeps track of previous opponents move; used during get_opponentturn
        self.previousMovesEvent = None

        # indicates if game is over
        self.gameOver = False



    """ get user color """
    def get_usercolor(self):
        return self.userColor


    """ get player turn """
    def get_playerturn(self):
        return self.userMove


    """ make a move on local gamestate """
    def move_piece(self, move, castling = False):

        # find starting cell in self.board
        startcell_y = self.letter_to_y[move[0]]
        startcell_x = self.number_to_x[move[1]]

        # find destination cell in self.board
        destcell_y = self.letter_to_y[move[2]]
        destcell_x = self.number_to_x[move[3]]

        # find the piece to be moved
        startpiece = self.board[startcell_x][startcell_y]
        # find destination piece
        destpiece = self.board[destcell_x][destcell_y]

        if not castling:
            # capturing condition
            if destpiece != "--":
                self.capture_piece(destpiece)
            else:
                # checks for en passant; returns corresponding captured pawn
                capturePawn = enpassant(startpiece, destpiece, move)
                if capturePawn != '':
                    destpiece = capturePawn
                    self.capture_piece(destpiece)

                # checks if castling; returns corresponding rook move if castling
                rookMove = self.castling(startpiece, move)
                if rookMove != '':
                    self.move_piece(rookMove, castling=True)

        self.board[startcell_x][startcell_y] = "--"
        self.board[destcell_x][destcell_y] = startpiece


    """ capture piece and move to buffer """
    def capture_piece(self, piece):
        pieceColor = piece[0]
        # if captured piece is black
        if pieceColor == 'b':
            # check if captured piece is pawn
            if piece[1] == 'P':
                for row in range(4):
                    for column in range(2):
                        if self.blackBuffer[row][column] == '--':
                            self.blackBuffer[row][column] = piece
                            return
            # all pieces other than pawn; bishop, knight, rook, queen
            else:
                for column in range(2):
                    if self.blackBuffer[self.bufferMap[piece[1]]][column] == '--':
                        self.blackBuffer[self.bufferMap[piece[1]]][column] = piece
                        return

        # if captured piece is white
        elif pieceColor == 'w':
            # check if captured piece is pawn, bishop, knight, rook, or queen and place into buffer accordingly
            if piece[1] == 'P':
                for row in range(4):
                    for column in range(2):
                        if self.whiteBuffer[row][column] == '--':
                            self.whiteBuffer[row][column] = piece
                            return
            # all pieces other than pawn; bishop, knight, rook, queen
            else:
                for column in range(2):
                    if self.whiteBuffer[self.bufferMap[piece[1]]][column] == '--':
                        self.whiteBuffer[self.bufferMap[piece[1]]][column] = piece
                        return
        return


    """ handles castling: returns corresponding rook if castling, else returns '' """
    def castling(self, piece, move):
        if piece == 'wK':
            if move == 'e1g1':
                # white king side castle; return corresponding rook move
                return 'h1f1'
            elif move == 'e1c1':
                # white queen side castle; return corresponding rook move
                return 'a1d1'

        elif piece == 'bK':
            if move == 'e8g8':
                # black king side castle; return corresponding rook move
                return 'h8f8'
            elif move == 'e8c8':
                #black queen side castle; return corresponding rook move
                return 'a8d8'

        return ''


    """ handles en passant move by pawns """
    def enpassant(self, piece, destpiece, move):
        # check if pawn has moved diagonally
        if move[0] != move[2]:
            # check for normal capture
            if destpiece != '--':
                # en passant; find captured piece (i.e move=a2b3, capturedPiece=b2)
                capturedPiece = self.board[letter_to_y[move[2]]][number_to_x[1]]
                return capturedPiece
        return ''


    """ handles user/opponent moves and updates gamestate """
    def update_gamestate(self):

        # user's move
        if self.userMove:
            move = self.get_usermove()
            self.move_piece(move)
            self.userMove = False

            print("Opponent's Turn...")
            return "ok"

        # opponent's move
        else:
            move = self.get_opponentmove()

            # checks move
            if move == "opponentresign":
                return "opponentresign"
            elif move == "none":
                return "ok"
            else:
                print('Opponent move: ', move)
                self.move_piece(move)
                self.userMove = True
                return "ok"


    """ read local game state for user move """
    def get_usermove(self):

        """
        read local game state
        """
        while 1:
            print("User's turn - Enter Move:")
            move = input()

            valid = interface.make_move(move)
            if valid:
                return move


    """ read game stream for opponent move """
    def get_opponentmove(self):

        try:
            # get event from game queue and check the type of event
            event = self.gameQueue.get_nowait()
            if event["type"] == 'gameState':

                # handles first turn
                if self.firstTurn:
                    # user starts the game with first move; opponent is second
                    if self.userColor == 'w':
                        if len(event["moves"]) == 9:
                            # get opponent's and save previous move
                            move = event["moves"].split()[-1]
                            self.firstTurn = False
                            self.previousMovesEvent = event
                            return move

                    # opponent starts the game with first move; opponent is first
                    if self.userColor == "b":
                        # get opponent's move and save previous move
                        move = event["moves"].split()[-1]
                        self.firstTurn = False
                        self.previousMovesEvent = event
                        return move
                
                # handles all turns beyond the first
                else:
                    # checks if the event is the opponent's; ignores user moves
                    if len(event["moves"]) == len(self.previousMovesEvent["moves"]) + 10:                        
                        # get opponent's move and save previous move
                        move = event["moves"].split()[-1]
                        self.previousMovesEvent = event
                        return move

                # check for resignation
                if event["status"] == "resign":
                    self.gameOver = True
                    return "opponentresign"
            
        except:
            pass

        return "none"


    """ handles when the game is over """
    def end_game(self, event, resign=False, checkmate=False):



        # init pygame window, window text, and icon
        pg.init()
        pg.display.set_caption("MagiChess: Game Over")
        icon = pg.image.load("Engine/chessboard/chessboard_images/wQ.png")
        pg.display.set_icon(icon)

        screen = pg.display.set_mode((200, 200))
        screen.fill(pg.Color("white"))
        clock = pg.time.Clock()

        font = pg.font.Font("freesansbold.ttf", size)
        if resign:
            textSurface = font.render("Game Over by resignation. Winner is " + event["winner"], True, color)

        if checkmate:
            textSurface = font.render("Game Over by checkmate. Winnder is " + event["winner"], True, color)

        # align and display text
        textBox = textSurface.get_rect()
        textBox.center = 100, 100
        screen.blit(textSurface, textBox)

        # colors of the button
        color_light = (170, 170, 170)
        color_dark = (100, 100, 100)

        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                
                if pg.type == pg.MOUSEBUTTONDOWN:
                    if 100 <= mouse[0] <= 100 + 50 and 200/3 <= mouse[1] <= 200/3 + 20:
                        pg.display.quit()
                        pg.quit()


            mouse = pg.mouse.get_pos()

            if 100 <= mouse[0] <= 100 + 50 and 200/3 <= mouse[1] <= 200/3 + 20:
                pygame.draw.rect(screen,color_light,[100,200/3,50,20])
            else:
                pygame.draw.rect(screen,color_dark,[100,200/3,50,20])

            text = smallfont.render('Close', True, (255,255,255))
            screen.blit(text, (100, 200/3))

            clock.tick(15)
            pg.display.flip()




        return



    """ reset board to original state """ 
    def reset(self):
        self.board = self.defaultState

    """ print board """
    def __str__(self):
        for i in range(8):
            print(self.board[i])

        return ''

