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

from Engine import chessboard
from Engine import audio

from Engine.lichess import lichessInterface_new as interface

#from Engine.mcu_interfaces import fastScan_interface as fastScan
from Engine.x328p_interface import x328p_gantry_interface as gantry_interface


isSoundOn = False
wGantry = True

"""
-------------------------------
GameState Class
-------------------------------
"""
class GameState():
    def __init__(self, gameQueue=None, replay=False, replay_user_color=None):
        
        # gameQueue = updating game stream queue -> live game
        #           = list of moves -> replay game
        self.gameQueue = gameQueue
        self.replay = replay
        # set user color (i.e 'w', 'b')
        if not self.replay:
            if self.gameQueue.get()["white"]["id"] == 'degugbot':
                self.userColor = 'w'
            else:
                self.userColor = 'b'
        else:
            self.userColor = replay_user_color
            self.moveset = gameQueue

        # capture buffer zones
        self.wBuffer = [["--", "--"],
                        ["--", "--"],
                        ["--", "--"],
                        ["--", "--"],
                        ["--", "--"],
                        ["--", "--"],
                        ["--", "--"],
                        ["--", "--"]]

        self.bBuffer = [["--", "--"],
                        ["--", "--"],
                        ["--", "--"],
                        ["--", "--"],
                        ["--", "--"],
                        ["--", "--"],
                        ["--", "--"],
                        ["--", "--"]]
        # dictionary that maps bishop to row 4, knight to row 5, rook to row 6, and queen to row 7 of buffer zones
        self.bufferMap = {'B':4, 'H':5, 'R':6, 'Q':7, 'K':7}
        self.defaultBuffer = self.wBuffer

        # user is white
        if self.userColor == 'w':
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
        else:
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

        # indicates how many turns have occurred
        self.turn = 0

        # indicates if game is in first turn; used during get_opponentturn
        self.firstTurn = True
        # keeps track of previous opponents move; used during get_opponentturn
        self.previousMovesEvent = None

        # cells need to be colored differently to indicate the starting and destination cell of moving pieces
        self.coloredCells = [(-1, -1), (-1, -1)]

        # message to be displayed for the user
        self.message = ""

        # indicates if game is over
        self.gameOver = False


    """ get user color """
    def get_usercolor(self):
        if self.userColor == 'w':
            return 'white'
        else:
            return 'black'

    """ get color of opponent """
    def get_opponentcolor(self):
        if self.userColor == 'w':
            return 'black'
        else:
            return 'white'

    """ set user color """
    def set_usercolor(self, user_color):
        self.userColor = user_color

    """ get player turn """
    def get_playerturn(self):
        return self.userMove

    """ find piece on local gamestate from chess coordinates """
    def get_piece_fromboard(self, letter, number):
        # map letter and number to local gamestate board
        cell_y = self.letter_to_y[letter]
        cell_x = self.number_to_x[number]
        # find the piece in the local board
        piece = self.board[cell_x][cell_y]
        # return the piece name and gamestate.board coordinates
        return (piece, (cell_x, cell_y))


    """ move piece to destination """
    def replace_piece_onboard(self, move, piece):
        # set original cell to empty and place piece on destination cell
        self.board[self.number_to_x[move[1]]][self.letter_to_y[move[0]]] = "--"
        self.board[self.number_to_x[move[3]]][self.letter_to_y[move[2]]] = piece
        return


# ---------------------------------------------------------------------------
#   GAMESTATE MOVES AND CONDITIONS
# ---------------------------------------------------------------------------

    """ make a move on local gamestate """
    def move_piece(self, move, castling = False):

        # return: '1' = ok, '0' = wrong scan, '-1' = hardware error
        if wGantry:
            if not self.userMove or self.replay:
                gantry_interface.make_physical_move(self, move)

        # length of move string (normally 4, pawn promotion 5)
        moveLength = len(move)

        # increment number of turns that have occurred
        self.turn += 1

        # find the piece to be moved and destination piece
        startpiece = self.get_piece_fromboard(move[0], move[1])
        destpiece = self.get_piece_fromboard(move[2], move[3])
        # get gamestate.board coordinates of the pieces
        self.coloredCells[0] = startpiece[1]
        self.coloredCells[1] = destpiece[1]
        # get actual piece (e.g 'wP', 'bP')
        startpiece = startpiece[0]
        destpiece = destpiece[0]

        if not castling:
            # capturing condition
            if destpiece != "--":
                self.capture_piece(destpiece)
            else:
                # check for pawn movement
                if startpiece[1] == 'P':
                    # check enpassant
                    self.enpassant(destpiece, move)

                # check if castling; returns corresponding rook move if castling
                rookMove = self.castling(startpiece, move)
                if rookMove != '':
                    # update gamestate after king's move/before rook's move
                    self.replace_piece_onboard(move, startpiece)
                    # move the rook
                    self.move_piece(rookMove, castling=True)
                    return

            # check for promotion
            if moveLength == 5:
                startpiece = self.promotion(startpiece, move)

        # move piece to destination
        self.replace_piece_onboard(move, startpiece)

        # boolean, because Sam doesn't have wav files
        if isSoundOn:
            audio.sound_move()

        return


    """ capture piece and move to buffer """
    def capture_piece(self, piece):
        pieceColor = piece[0]
        # if captured piece is black
        if pieceColor == 'b':
            # check if captured piece is pawn
            if piece[1] == 'P':
                for row in range(4):
                    for column in range(2):
                        if self.bBuffer[row][column] == '--':
                            self.bBuffer[row][column] = piece
                            return
            # all pieces other than pawn; bishop, knight, rook, queen
            else:
                for column in range(2):
                    if self.bBuffer[self.bufferMap[piece[1]]][column] == '--':
                        self.bBuffer[self.bufferMap[piece[1]]][column] = piece
                        return

        # if captured piece is white
        elif pieceColor == 'w':
            # check if captured piece is pawn, bishop, knight, rook, or queen and place into buffer accordingly
            if piece[1] == 'P':
                for row in range(4):
                    for column in range(2):
                        if self.wBuffer[row][column] == '--':
                            self.wBuffer[row][column] = piece
                            return
            # all pieces other than pawn; bishop, knight, rook, queen
            else:
                for column in range(2):
                    if self.wBuffer[self.bufferMap[piece[1]]][column] == '--':
                        self.wBuffer[self.bufferMap[piece[1]]][column] = piece
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


    """ handles pawn promotion """
    def promotion(self, pawn, move):

        # piece mapping
        pieceDict = {'b':'B', 'k':'H', 'r':'R', 'q':'Q'}
        # 5th element of string indicates promotion piece; (b, k, r, q) -> (B, H, R, Q)
        promotionPiece = pieceDict[move[4]]

        # check for user or opponent promotion
        if self.userMove:

            # put pawn in capture buffer and put return piece on board
            self.capture_piece(pawn)
            # find if piece is in return buffer
            if pawn[0] == 'w':
                for i in range(2):
                    if self.wBuffer[self.bufferMap[pieceDict[move[4]]]][i] != '--':
                        # remove promotion piece from white buffer and return it
                        self.wBuffer[self.bufferMap[pieceDict[move[4]]]][i] = '--'
                        return 'w' + promotionPiece

            else:
                for i in range(2):
                    if self.bBuffer[self.bufferMap[pieceDict[move[4]]]][i] != '--':
                        # remove promotion piece from black buffer and return it
                        self.bBuffer[self.bufferMap[pieceDict[move[4]]]][i] = '--'
                        return 'b' + promotionPiece

        # opponent promotion
        else:
            
            # put pawn in capture buffer
            self.capture_piece(pawn)
            # find if piece is in return buffer
            if pawn[0] == 'w':
                for i in range(2):
                    if self.wBuffer[self.bufferMap[promotionPiece]][i] != '--':
                        # remove promotion piece from white buffer and return it
                        self.wBuffer[self.bufferMap[promotionPiece]][i] = '--'
                        return 'w' + promotionPiece

            else:
                 for i in range(2):
                    if self.bBuffer[self.bufferMap[promotionPiece]][i] != '--':
                        # remove promotion piece from black buffer and return it
                        self.bBuffer[self.bufferMap[promotionPiece]][i] = '--'
                        return 'b' + promotionPiece
            
            print("Piece not in capture zone!")
            self.promotion(pawn, move)


    """ handles en passant move by pawns """
    def enpassant(self, destpiece, move):
        # check if pawn has moved diagonally
        if move[0] != move[2]:
            # check for normal capture
            if destpiece == '--': 
                # en passant; find captured piece (i.e move=a2b3, capturedPiece=b2)
                capturedPawn = self.board[self.number_to_x[move[1]]][self.letter_to_y[move[2]]]
                self.capture_piece(capturedPawn)

                # empty cell occupied by captured pawn
                self.board[self.number_to_x[move[1]]][self.letter_to_y[move[2]]] = '--'

        return


# ---------------------------------------------------------------------------
# GAME STATE UPDATES AND GETTING USER/OPPONENT MOVES
# ---------------------------------------------------------------------------

    """ handles user/opponent moves and updates gamestate """
    def update_gamestate(self):

        if self.replay:
            if self.replay_move():
                return 'ok'
            else:
                return 'replay_over'
        else:
            # user's move
            if self.userMove:
                move = self.get_usermove()

                if move != "invalid":
                    # make move on local gamestate board
                    self.move_piece(move)
                    self.userMove = False
                    self.message = "Opponent's Turn..."

                return "ok"

            # opponent's move
            else:
                # read game stream for opponent event
                move = self.read_gamestream()

                # move has not been received by opponent
                if move == "none":
                    return "ok"
                # move has been received
                elif len(move) == 4 or len(move) == 5: 
                    self.message = "Opponent move: " + str(move)
                    # move piece on local gamestate board
                    self.move_piece(move)
                    self.userMove = True

                    return "ok"
                # other responses (i.e resgination, checkmate, abort) 
                else:
                    if move[0] == "mate":
                        self.move_piece(move[2])
                    return move


    """ read local game state for user move """
    def get_usermove(self):

        """
        read local game state
        """
        move = input("User's turn - Enter Move: ")

        # check for pawn move and promotion
        try:
            piece = self.board[self.number_to_x[move[1]]][self.letter_to_y[move[0]]]
            if piece[1] == 'P' and (move[3] == '1' or move[3] == '8'):
                while 1:
                    # prompt user for promotion piece
                    inputPiece = input("Promotion piece; bishop(b), knight(n), rook(r), queen(q): ")
                    if inputPiece == 'b' or inputPiece == 'k' or inputPiece == 'r' or inputPiece == 'q':
                        break
                    self.message = "Invalid promotion piece argument"
                # append promotion piece to move
                move += inputPiece
        except:
            pass

        # send move to LiChess server
        response = interface.make_move(move)
        if response == 1:
            return move
        else:
            self.message = response
            # chessboard.display_alert(response)
            return "invalid"


    """ read the game stream """
    def read_gamestream(self):

        try:
            # get event from game queue
            event = self.gameQueue.get_nowait()
            # gamestate has changed; either user or opponent has moved
            if event["type"] == 'gameState':
                print("Event Response: ", event)

                # check for resignation or checkmate; return winner and reason
                if event["status"] == "resign":
                    self.gameOver = True
                    return ('resign', event['winner'])
                # check for abort
                if event["status"] == "abort":
                    self.gameOver = True
                    return 'abort'

                # handles first turn
                if self.firstTurn:
                    # user starts the game with first move; opponent is second
                    if self.userColor == 'w':
                        if len(event["moves"]) == 9:
                            # get opponent's move and save previous move
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
                    if len(self.previousMovesEvent["moves"]) + 10 == len(event["moves"]) or len(self.previousMovesEvent["moves"]) + 11 == len(event["moves"]):                        
                        # get opponent's move and save previous move
                        move = event["moves"].split()[-1]
                        self.previousMovesEvent = event
                        # check if the move caused mate
                        if event["status"] == "mate":
                            self.gameOver = True
                            return ('mate', event['winner'], move)
                        else:
                            return move

            return "none"
        except:
            return "none"

    """ replaying a game """
    def replay_move(self):
        try:
            move = self.moveset[self.turn]
            time.sleep(3)
            self.move_piece(move)
            return 1
        except IndexError:
            self.gameOver = True
            self.message = "Replay Over"
            return 0

    """ reset board to original state """ 
    def reset(self):
        self.board = self.defaultState
        self.wBuffer = self.defaultBuffer
        self.bBuffer = self.defaultBuffer
        self.turns = 0
        self.coloredCells = [(-1, -1), (-1, -1)]
        self.gameover = False
        self.message = ""
        self.previousMovesEvent = None

    """ print board """
    def __str__(self):
        for i in range(8):
            print(self.board[i])

        return ''
