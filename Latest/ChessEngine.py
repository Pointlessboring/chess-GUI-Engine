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
   
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    def makeMove(self, move):
        """ Takes a move as a parameter and executes it. (Won't work for castling, enpassant, promotion) """

        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # Log the move
        self.whiteToMove = not self.whiteToMove # Swap player to play

        if move.pieceMoved == 'wK': 
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):
        """
        This function will undo the last move.
        """

        if len(self.moveLog) != 0: # Make sure that there is a move to undo.
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

            if move.pieceMoved == 'wK': 
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    def getValidMoves(self):
        """ All moves considering checks. """
        #1) generate all possible moves
        moves = self.getAllPossibleMoves()
        
        #2) for each move, make the move
        for i in range(len(moves)-1 , -1, -1):
            self.makeMove(moves[i])
            #3) generate all of opponents's moves
            #4) for each of your opponents' move see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i]) #5) if they do attack your king, the move is invalid
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else: 
                self.staleMate = True
        else: 
            self.staleMate = False
            self.checkMate = False        

        return moves

    def inCheck(self):
        """ """
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        """ Determine if opponents can attack square (r, c) """
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getAllPossibleMoves(self):
        """ All possible moves. """
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #Number of columns. 
                turn = self.board[r][c][0] # Turn is the 'color' of the piece on the square
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves
                        
    def getPawnMoves(self, r, c, moves):
        """ Get all the pawn moves for the pawn located at row, col and add these moves to the list. """
        if self.whiteToMove:
            if self.board[r-1][c] == '--': # Check for 1 square advance
                moves.append(Move((r,c),(r-1,c), self.board))
                if (r == 6) and (self.board[r-2][c]) == '--': # Check for 2 square advance
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c - 1 >= 0:  # Capture to the left
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c-1), self.board))
            if c + 1 <= 7: # Capture to the right
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c+1), self.board))
        else:
            if self.board[r + 1][c] == '--': # Check for 1 square advance
                moves.append(Move((r,c),(r + 1,c), self.board))
                if (r == 1) and (self.board[r + 2][c]) == '--': # Check for 2 square advance
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # Capture to the left
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r,c),(r + 1, c - 1), self.board))
            if c + 1 <= 7: # Capture to the right
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r,c),(r + 1,c + 1), self.board))            

    def getRookMoves(self, r, c, moves):
        """ Get all the Rook moves for the Rook located at row, col and add these moves to the list. """
        directions = ((-1 , 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range (1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: 
                        break
                else: 
                    break

    def getKnightMoves(self, r, c, moves):
        """ Get all the Knight moves for the Knight located at row, col and add these moves to the list. """
        knightMoves = ((-2 , -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]           
            if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
               endPiece = self.board[endRow][endCol]
               if endPiece[0] != allyColor:
                moves.append(Move((r, c), (endRow, endCol), self.board))
         
    def getBishopMoves(self, r, c, moves):
        """ Get all the Bishop moves for the Bishop located at row, col and add these moves to the list. """
        directions = ((-1 , -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range (1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: 
                        break
                else: 
                    break

    def getQueenMoves(self, r, c, moves):
        """ Get all the Queen moves for the Queen located at row, col and add these moves to the list. """
        self.getRookMoves(r,c, moves)
        self.getBishopMoves(r,c, moves)

    def getKingMoves(self, r, c, moves):
        """ Get all the King moves for the King located at row, col and add these moves to the list. """
        kingMoves = ((-1 , -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]           
            if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
               endPiece = self.board[endRow][endCol]
               if endPiece[0] != allyColor:
                moves.append(Move((r, c), (endRow, endCol), self.board))

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
        
    def __eq__(self, other):
        """ Overriding the equals method """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankfile(self.startRow, self.startCol) + self.getRankfile(self.endRow, self.endCol)

    def getRankfile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
