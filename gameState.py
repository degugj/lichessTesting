# Weishan Li
# Jack DeGuglielmo
# September 2020
# Description: GameState class for storing the local state of the chess board

from chessPiece import ChessPiece

class GameState:
    def __init__(self):
        self.board = {'a1': None, 'a2': None, 'a3': None, 'a4': None, 'a5': None, 'a6': None, 'a7': None, 'a8': None, \
                 'b1': None, 'b2': None, 'b3': None, 'b4': None, 'b5': None, 'b6': None, 'b7': None, 'b8': None, \
                 'c1': None, 'c2': None, 'c3': None, 'c4': None, 'c5': None, 'c6': None, 'c7': None, 'c8': None, \
                 'd1': None, 'd2': None, 'd3': None, 'd4': None, 'd5': None, 'd6': None, 'd7': None, 'd8': None, \
                 'e1': None, 'e2': None, 'e3': None, 'e4': None, 'e5': None, 'e6': None, 'e7': None, 'e8': None, \
                 'f1': None, 'f2': None, 'f3': None, 'f4': None, 'f5': None, 'f6': None, 'f7': None, 'f8': None, \
                 'g1': None, 'g2': None, 'g3': None, 'g4': None, 'g5': None, 'g6': None, 'g7': None, 'g8': None, \
                 'h1': None, 'h2': None, 'h3': None, 'h4': None, 'h5': None, 'h6': None, 'h7': None, 'h8': None}

    def reset(self):

        # K
        wKing = ChessPiece('K', 'w')
        self.board['e1'] = wKing
        bKing = ChessPiece('K', 'b')
        self.board['e8'] = bKing

        # q
        wQueen = ChessPiece('q', 'w')
        self.board['e1'] = wQueen
        bQueen = ChessPiece('q', 'b')
        self.board['e8'] = bQueen

        # b
        bBishopCells = ['c8', 'f8']
        bBishop = ChessPiece('b', 'b')
        self.board[bBishopCells[0]] = bBishop
        bBishop = ChessPiece('b', 'b')
        self.board[bBishopCells[1]] = bBishop

        wBishopCells = ['c1', 'f1']
        wBishop = ChessPiece('b', 'w')
        self.board[wBishopCells[0]] = wBishop
        wBishop = ChessPiece('b', 'w')
        self.board[wBishopCells[1]] = wBishop

        # k
        bKnightCells = ['b8', 'g8']
        bKnight = ChessPiece('k', 'b')
        self.board[bKnightCells[0]] = bKnight
        bKnight = ChessPiece('k', 'b')
        self.board[bKnightCells[1]] = bKnight

        wKnightCells = ['b1', 'g1']
        wKnight = ChessPiece('k', 'w')
        self.board[wKnightCells[0]] = wKnight
        wKnight = ChessPiece('k', 'w')
        self.board[wKnightCells[1]] = wKnight

        # r
        bRookCells = ['a8', 'a8']
        bRook = ChessPiece('r', 'b')
        self.board[bRookCells[0]] = bRook
        bRook = ChessPiece('r', 'b')
        self.board[bRookCells[1]] = bRook

        wRookCells = ['a1', 'h1']
        wRook = ChessPiece('r', 'w')
        self.board[wRookCells[0]] = wRook
        wRook = ChessPiece('r', 'w')
        self.board[wRookCells[1]] = wRook

        # p
        bPonsCells = ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']
        for item in bPonsCells:
            bPon = ChessPiece('p', 'b')
            self.board[item] = bPon

        wPonsCells = ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
        for item in wPonsCells:
            wPon = ChessPiece('p', 'w')
            self.board[item] = wPon

    def __str__(self):
        return "print the board here"   # this is where we want to put the board to text thing that Shira was talking about

test = GameState()
test.reset()
print(test)     # print will call __str()__