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

from Engine.lichess import lichessInterface_new as interface
#from Engine.mcu_interfaces import fastScan_interface as fastScan

#from Engine.x328p_interface import x328p_interface as gantry_interface

"""
-------------------------------
GameState Class
-------------------------------
"""
class GameState():
    def __init__(self, gameQueue=None):

        # set user color (i.e 'w', 'b')
        self.gameQueue = gameQueue

        if self.gameQueue.get()["white"]["id"] == 'degugbot':
            self.userColor = 'w'
        else:
            self.userColor = 'b'

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
        # dictionary that maps bishop to row 4, knight to row 5, rook to row 6, and queen to row 7
        self.bufferMap = {'B':4, 'H':5, 'R':6, 'Q':7}
        
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


# ---------------------------------------------------------------------------
#   GAMESTATE MOVES AND CONDITIONS
# ---------------------------------------------------------------------------

    """ make a move on local gamestate """
    def move_piece(self, move, castling = False):

        # return: '1' = ok, '0' = wrong scan, '-1' = hardware error
        #if not self.userMove:
            #gantry_interface.make_physical_move(self, move)

        # length of move string (normally 4, pawn promotion 5)
        moveLength = len(move)

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
                # check for pawn movement
                if startpiece[1] == 'P':
                    # check enpassant
                    self.enpassant(destpiece, move)

                # check if castling; returns corresponding rook move if castling
                rookMove = self.castling(startpiece, move)
                if rookMove != '':
                    # update gamestate after king's move/before rook's move
                    self.board[startcell_x][startcell_y] = "--"
                    self.board[destcell_x][destcell_y] = startpiece
                    # move the rook
                    self.move_piece(rookMove, castling=True)
                    return

            # check for promotion
            if moveLength == 5:
                startpiece = self.promotion(startpiece, move)


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
    def update_gamestate(self, screen):

        # user's move
        if self.userMove:
            chessboard.display_alert(screen, "User's Turn")
            move = self.get_usermove(screen)

            if move:
                # make move on local gamestate board
                self.move_piece(move)

            self.userMove = False
            return "ok"

        # opponent's move
        else:
            chessboard.display_alert(screen, "Opponent's Turn...")
            move = self.get_opponentmove(screen)

            # move has not been received by opponent
            if move == "none":
                return "ok"
            # move has been received
            elif len(move) == 4 or len(move) == 5:
                chessboard.display_alert(screen, "Opponent move: " + move)
                # move piece on local gamestate board
                self.move_piece(move)
                self.userMove = True
                return "ok"
            else:
                return move


    """ read local game state for user move """
    def get_usermove(self, screen):

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
                    chessboard.display_alert(screen, "Invalid promotion piece argument")
                # append promotion piece to move
                move += inputPiece
        except:
            pass

        # send move to LiChess server
        valid = interface.make_move(move, screen)
        if valid:
            return move


    """ read game stream for opponent move """
    def get_opponentmove(self, screen):

        try:
            # get event from game queue and check the type of event
            event = self.gameQueue.get_nowait()
            if event["type"] == 'gameState':
                print("OPPONENT EVENT", event)
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
                        return move

                # check for resignation
                if event["status"] == "resign":
                    self.gameOver = True
                    return event["winner"] + "resign"
                if event["status"] == "mate":
                    self.gameOver = True
                    return event["winner"] + "mate"
            
        except:
            pass

        return "none"


    """ reset board to original state """ 
    def reset(self):
        self.board = self.defaultState

    """ print board """
    def __str__(self):
        for i in range(8):
            print(self.board[i])

        return ''

