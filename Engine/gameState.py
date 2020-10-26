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
    def __init__(self):
        self.localPlayerColor = ''

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
        self.defaultState = self.board

        self.userMove = True

    """ movePiece: move piece
            params: 
                move: string that indicates chess convention move (i.e 'e7e5') (e7=start cell, e5=dest cell)
            return:
                none
    """
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


    def setCell(self, piece, cell_x, cell_y):
        self.board[cell_x][cell_y] = piece

    
    """ update_gamestate: handles user and opponent moves
        params:
        return:
    """
    def update_gamestate(self):

        # user's move
        if self.userMove:
            """
            read local gamestate for user move
            """
            while (self.userMove):
                print("User Move - Enter Move: ")
                move = input()

                # send move to server
                message, valid = interface.make_move(move)
                print(message, valid)
                if (valid):
                    # if move is success
                    try:
                        self.move_piece(move)
                        self.userMove = False
                    except:
                        print("Invalid input given")
                        

        # opponent's move
        else:

            """
            read gamestream for opponent moves
            """
            self.userMove = True

    # reset board to original state 
    def reset(self):
        self.board = self.defaultState

    def __str__(self):
        for i in range(8):
            print(self.board[i])

        return ''
