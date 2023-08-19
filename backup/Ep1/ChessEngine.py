"""
This class is responsible for storing all information about the current state of a game of chess.
It will also be responsible to determine valid move at current state. 
It will also keep a move log.
"""

class GameState():
    def __init__(self) -> None:
        # board is a 8x8 2d list. each element has 2 characters.
        # 1st character is color of piece "b" or "w"
        # 2nd is the type of piece "K", "Q", "R", "B", "N", "P"
        # "--" represents an empty space with no piece

        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", 'bN', "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", 'bp', "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", 'wp', "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", 'wN', "wR"]]

        self.whiteToMove = True
        self.moveLog = []

