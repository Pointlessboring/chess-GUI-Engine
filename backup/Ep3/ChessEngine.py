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
    
    def makeMove(self, move):
        """
        Takes a move as a parameter and executes it. (Won't work for castling, enpassant, promotion)
        """

        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # Log the move
        self.whiteToMove = not self.whiteToMove # Swap player to play

    def undoMove(self):
        """
        This function will undo the last move.
        """

        if len(self.moveLog) != 0: # Make sure that there is a move to undo.
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove


    def getValidMoves(self):
        """
        All moves considering checks.
        """
        return self.getAllPossibleMoves()
    

    def getAllPossibleMoves(self):
        """
        All possible moves.
        """
        moves = [Move((6,4), (4,4), self.board)] # hardcode for testing purposes.
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #Number of columns. 
                turn = self.board[r][c][0] # Turn is the 'color' of the piece on the square
                if (turn == 'w' and self.whiteToMove) and (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
        return moves
                        
    def getPawnMoves():
        """
        Get all the pawn moves for the pawn located at row, col and add these moves to the list.
        """
        pass

    def getRookMoves():
        """
        Get all the pawn moves for the pawn located at row, col and add these moves to the list.
        """
        pass

class Move():
    # map keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v:k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v:k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board) -> None:
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)

    def __eq__(self, other):
        """ Overriding the equals method """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankfile(self.startRow, self.startCol) + self.getRankfile(self.endRow, self.endCol)

    def getRankfile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
