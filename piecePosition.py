# Weishan Li
# Jack DeGuglielmo
# September 2020
# Description: GameState class for storing the local state of the chess board

from collections import OrderedDict
from chessPiece import ChessPiece


class piecePosition:
    def __init__(self):
        self.heuristic = 0
        self.piece = None

    def __str__(self):
        return self.piece

board = [[piecePosition]*24]*24
