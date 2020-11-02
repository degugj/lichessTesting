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
        self.letter_to_x = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        self.number_to_y = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}

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
            self.letter_to_x = {'a':7, 'b':6, 'c':5, 'd':4, 'e':3, 'f':2, 'g':1, 'h':0}
            self.number_to_y = {'1':0, '2':1, '3':2, '4':3, '5':4, '6':5, '7':6, '8':7}

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
        
        self.firstTurn = True
        self.previousMovesEvent = None


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



    """ get user color """
    def get_usercolor(self):
        return self.userColor


    """ make a move on local gamestate """
    def move_piece(self, move):
        # find starting cell in self.board
        startcell_y = self.letter_to_x[move[0]]
        startcell_x = self.number_to_y[move[1]]

        # find destination cell in self.board
        destcell_y = self.letter_to_x[move[2]]
        destcell_x = self.number_to_y[move[3]]

        # find the pieces to be moved
        startpiece = self.board[startcell_x][startcell_y]
        destpiece = self.board[destcell_x][destcell_y]

        # capturing condition
        if destpiece != "--":
            self.capture_piece(destpiece)

        self.board[startcell_x][startcell_y] = "--"
        self.board[destcell_x][destcell_y] = startpiece


    """ capture piece and move to buffer """
    def capture_piece(self, piece):
        pieceColor = piece[0]
        # if captured piece is black
        if pieceColor == 'b':
            # check if captured piece is pawn, bishop, knight, rook, or queen and place into buffer accordingly
            if piece[1] == 'P':
                for row in range(4):
                    for column in range(2):
                        if self.blackBuffer[row][column] == '--':
                            self.blackBuffer[row][column] = piece
                            return
            elif piece[1] == 'B': 
                for column in range(2):
                    if self.blackBuffer[4][column] == '--':
                        self.blackBuffer[4][column] = piece
                        return
            elif piece[1] == 'H':
                for column in range(2):
                    if self.blackBuffer[5][column] == '--':
                        self.blackBuffer[5][column] = piece
                        return
            elif piece[1] == 'R':
                for column in range(2):
                    if self.blackBuffer[6][column] == '--':
                        self.blackBuffer[6][column] = piece
                        return
            elif piece[1] == 'Q':
                for column in range(2):
                    if self.blackBuffer[7][column] == '--':
                        self.blackBuffer[7][column] = piece
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
            elif piece[1] == 'B':
                for column in range(2):
                    if self.whiteBuffer[4][column] == '--':
                        self.whiteBuffer[4][column] = piece
                        return
            elif piece[1] == 'H':
                for column in range(2):
                    if self.whiteBuffer[5][column] == '--':
                        self.whiteBuffer[5][column] = piece
                        return
            elif piece[1] == 'R':
                for column in range(2):
                    if self.whiteBuffer[6][column] == '--':
                        self.whiteBuffer[6][column] = piece
                        return
            elif piece[1] == 'Q':
                for column in range(2):
                    if self.whiteBuffer[7][column] == '--':
                        self.whiteBuffer[7][column] = piece
                        return
        return


    """ handles user/opponent moves and updates gamestate """
    def update_gamestate(self): 

        # user's move
        if self.userMove:
            move = self.get_usermove()
            self.move_piece(move)
            self.userMove = False
                        

        # opponent's move
        else:
            print("Opponent's Turn...")
            move = self.get_opponentmove()
            print('opponent move: ', move)
            self.move_piece(move)
            self.userMove = True


    """ get_usermove: read local gamestate to get move
    params:
    return:
        move - user's desired move (i.e 'e2e4')
    """
    def get_usermove(self):

        """
        read local game state
        """
        while True:
            print("User's turn - Enter Move:")
            move = input()

            valid = interface.make_move(move)
            if valid:
                return move


    """ get_opponentmove: read gamestream for opponent moves
        params:
        return:
            move - opponent's move
    """
    def get_opponentmove(self):

        waiting = True
        while waiting:
            try:
                # get event from game queue and check the type of event
                event = self.gameQueue.get_nowait()
                if event["type"] == 'gameState':

                    # handles first turn
                    if self.firstTurn:
                        # user starts the game with first move
                        if self.userColor == 'w':
                            if len(event["moves"]) == 9:
                                move = event["moves"].split()[-1]
                                self.firstTurn = False
                                waiting = False
                                self.previousMovesEvent = event

                        # opponent starts the game with first move
                        if self.userColor == "b":
                            move = event["moves"].split()[-1]
                            self.firstTurn = False
                            waiting = False
                            self.previousMovesEvent = event
                    
                    # handles all turns beyond the first
                    else:
                        if len(event["moves"]) == len(self.previousMovesEvent["moves"]) + 10:                        
                            move = event["moves"].split()[-1]
                            waiting = False
                            self.previousMovesEvent = event
                
            except:
                pass


        return move



    """ reset board to original state """ 
    def reset(self):
        self.board = self.defaultState

    """ print board """
    def __str__(self):
        for i in range(8):
            print(self.board[i])

        return ''

