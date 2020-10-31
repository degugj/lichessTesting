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


        # create capture buffers for white and black
        # self.whiteBufferZone = {'wP1': '--', 'wP2': '--'
        #                         'wP3': '--', 'wP4': '--'
        #                         'wP5': '--', 'wP6': '--'
        #                         'wP7': '--', 'wP8': '--'
        #                         'wH1': '--', 'wH2': '--'
        #                         'wB1': '--', 'wB2': '--'
        #                         'wR1': '--', 'wR2': '--'
        #                         'wQ1': '--', 'wQ2': '--'}


        # self.blackBufferZone = {'bP1': '--', 'bP2': '--'
        #                         'bP3': '--', 'bP4': '--'
        #                         'bP5': '--', 'bP6': '--'
        #                         'bP7': '--', 'bP8': '--'
        #                         'bH1': '--', 'bH2': '--'
        #                         'bB1': '--', 'bB2': '--'
        #                         'bR1': '--', 'bR2': '--'
        #                         'bQ1': '--', 'bQ2': '--'}



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

        # find the piece and move to destination
        piece = self.board[startcell_x][startcell_y] 

        self.board[startcell_x][startcell_y] = "--"
        self.board[destcell_x][destcell_y] = piece


    """ capture piece and move to buffer """
    def capture_piece(self, piece, color):
        # if color == 'w' and piece[1] == 'P':
        #     for num in range(8):
        #         if self.blackBufferZone[piece + str(num)] == '--':
        #             self.blackBufferZone[piece + str(num)] = piece
        # elif 
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
                
                event = self.gameQueue.get_nowait()
                if event["type"] == 'gameState':

                    if self.firstTurn and self.userColor == 'w':
                        if self.firstTurn:
                            self.previousMovesEvent = event

                        if len(event["moves"]) == len(previousEvent["moves"]) + 5:
                            
                            move = event["moves"].split()[-1]
                            self.previousMovesEvent = event
                            self.firstTurn = False
                            waiting = False
                    
                    elif self.firstTurn and self.userColor == 'b':
                        move = event["moves"].split()[-1]
                        self.previousMovesEvent = event
                        self.firstTurn = False
                        waiting = False

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

