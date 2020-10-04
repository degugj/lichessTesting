# Weishan Li
# Jack DeGuglielmo
# September 2020
# Description: ChessPiece class to represent a chess piece

class ChessPiece:
    def __init__(self, pieceType, color):
        self.type = pieceType   # What type of chess piece is this
        self.color = color  # What color is the piece ('w' or 'b')