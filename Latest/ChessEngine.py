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
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.enpassantPossible = () # this will be the coordinate where en passant capture is possible.
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightLog = [CastleRights(self.currentCastlingRight.wks,
                                            self.currentCastlingRight.wqs,
                                            self.currentCastlingRight.bks,
                                            self.currentCastlingRight.bqs)]

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

        #pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0]+'Q'

        #enpassant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'
        
        #update enpassantPossible variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.endCol)
        else:
            self.enpassantPossible = ()
        
        # Castling move. Note that the king will already have moved per code above.
        if move.isCastleMove:
            if (move.endCol - move.startCol) == 2: # King side castle
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] #copies the rook
                self.board[move.endRow][move.endCol+1] = '--'
            else:   # queen side castle
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2] #copies the rook
                self.board[move.endRow][move.endCol-2] = '--'

        # update castling rights - whenever it is a rook or king move.
        self.updateCastleRights(move)

        self.castleRightLog.append(CastleRights(self.currentCastlingRight.wks,
                                                self.currentCastlingRight.wqs,
                                                self.currentCastlingRight.bks,
                                                self.currentCastlingRight.bqs))
    
    def undoMove(self):
        """ This function will undo the last move. """

        if len(self.moveLog) != 0: # Make sure that there is a move to undo.
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

            # debug
            # print("Undo: piece moved ", move.pieceMoved)
            # print("Undo: piece captured ", move.pieceCaptured)
            # print("Undo: isEnpassantMove ", move.isEnpassantMove)
            # print("Undo: isCastleMove ", move.isCastleMove)

            if move.pieceMoved == 'wK': 
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

            #undo enpassant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--' # Clear previous End position
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
                # print("Undo: Enpassant end position", move.endRow , move.endCol)
                # print("Undo: Enpassant capture position", move.startRow , move.endCol)

            #undo 2 square pawn advance
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

            # undo castling rights
            self.castleRightLog.pop()
            self.currentCastlingRight = CastleRights(self.castleRightLog[-1].wks,
                                            self.castleRightLog[-1].wqs,
                                            self.castleRightLog[-1].bks,
                                            self.castleRightLog[-1].bqs)

            # undo castle move
            if move.isCastleMove:
                if (move.endCol - move.startCol) == 2: # King side castle
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1] #copies the rook
                    self.board[move.endRow][move.endCol-1] = '--'
                else:   # queen side castle
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1] #copies the rook
                    self.board[move.endRow][move.endCol+1] = '--'


    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                else:
                    move.startCol == 7 
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'BR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                else:
                    move.startCol == 7 
                    self.currentCastlingRight.bks = False
    
    def getValidMoves(self):
        """ All moves considering checks. """
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()

        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]            
        if self.inCheck:
            if len(self.checks) == 1: # Only 1 check. Block or move king
                moves = self.getAllPossibleMoves()
                #to block a check you must move a piece between king and enemy piece
                check = self.checks[0] 
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                #if Knight, must capture knight or move king.
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else: 
                    for i in range (1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) # Check[2] and Check [3] are the check directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:  # This is the piece making the check
                            break
                # Remove all moves that do not block check or move king.
                for i in range (len(moves) -1, -1, -1):
                    if moves[i].pieceMoved[1] !='K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares: # move does not block check or capture checking piece
                            moves.remove(moves[i])
            else: # double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else: #not in check so all moves are fine.
            moves = self.getAllPossibleMoves()

        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True

        return moves

        
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
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) -1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        if self.whiteToMove:
            if self.board[r - 1][c] == '--': # Check for 1 square advance
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r,c),(r - 1,c), self.board))
                    if (r == 6) and (self.board[r - 2][c]) == '--': # Check for 2 square advance
                        moves.append(Move((r, c), (r - 2, c), self.board))
            # Pawn captures
            if c - 1 >= 0:  # Capture to the left 
                if not piecePinned or pinDirection == (-1, -1):
                    if self.board[r - 1][c - 1][0] == 'b':
                        moves.append(Move((r , c),(r - 1, c - 1), self.board))
                    elif (r - 1, c - 1) == self.enpassantPossible:
                        moves.append(Move((r , c),(r - 1, c - 1), self.board, isEnpassantMove=True))
            if c + 1 <= 7: # Capture to the right
                if not piecePinned or pinDirection == (-1, 1):
                    if self.board[r - 1][c + 1][0] == 'b':
                        moves.append(Move((r , c),(r - 1, c + 1), self.board))
                    elif (r - 1, c + 1) == self.enpassantPossible:
                        moves.append(Move((r , c),(r - 1, c + 1), self.board, isEnpassantMove=True))
        else:
            if self.board[r + 1][c] == '--': # Check for 1 square advance
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((r , c),(r + 1, c), self.board))
                if (r == 1) and (self.board[r + 2][c]) == '--': # Check for 2 square advance
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # Capture to the left
                if not piecePinned or pinDirection == (1, -1):
                    if self.board[r + 1][c - 1][0] == 'w':
                        moves.append(Move((r , c),(r + 1, c - 1), self.board))
                    elif (r + 1, c - 1) == self.enpassantPossible:
                        moves.append(Move((r , c),(r + 1, c - 1), self.board, isEnpassantMove=True))
            if c + 1 <= 7: # Capture to the right
                if not piecePinned or pinDirection == (1, 1):
                    if self.board[r + 1][c + 1][0] == 'w':
                        moves.append(Move((r, c),(r + 1,c + 1), self.board))            
                    elif (r + 1, c + 1) == self.enpassantPossible:
                        moves.append(Move((r , c),(r + 1, c + 1), self.board, isEnpassantMove=True))

    def getRookMoves(self, r, c, moves):
        """ Get all the Rook moves for the Rook located at row, col and add these moves to the list. """ 
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) -1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q' : # Don't remove Queen from pin on Rook, only remove it on bishops moves.
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1 , 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range (1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--':
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: #friendly piece
                            break
                else: # off board
                    break

    def getKnightMoves(self, r, c, moves):
        """ Get all the Knight moves for the Knight located at row, col and add these moves to the list. """
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) -1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        knightMoves = ((-2 , -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]           
            if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
         
    def getBishopMoves(self, r, c, moves):
        """ Get all the Bishop moves for the Bishop located at row, col and add these moves to the list. """
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) -1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1 , -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range (1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
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
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]           
            if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
               endPiece = self.board[endRow][endCol]
               if endPiece[0] != allyColor: # empty or enemy piece
                # place king and check for checks
                if allyColor == 'w':
                    self.whiteKingLocation = (endRow, endCol)
                else: 
                    self.blackKingLocation = (endRow, endCol)
                inCheck, pins, checks = self.checkForPinsAndChecks()
                if not inCheck:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

                # place king back on its original location
                if allyColor == 'w':
                    self.whiteKingLocation = (r, c)
                else: 
                    self.blackKingLocation = (r, c)

        self.getCastleMoves(r, c, moves, allyColor)

    def getCastleMoves(self, r, c, moves, allyColor):
        """ Generate all possible castle moves for the king at r, c and add moves to list of moves """
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not(self.whiteToMove) and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves, allyColor)

        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not(self.whiteToMove) and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves, allyColor)       


    def getKingsideCastleMoves(self, r, c, moves, allyColor):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
            if not(self.isCastleCheck([4,5,6])):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))

    def getQueensideCastleMoves(self, r, c, moves, allyColor):
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--':
            if not(self.isCastleCheck([2,3,4])):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))
                
    def isCastleCheck(self, positions):
        """ Note this is not good design """

        tempKing = self.whiteKingLocation if self.whiteToMove else self.blackKingLocation # Save the original location
        totalCheck = False

        if self.whiteToMove:
            for pos in positions:
                self.whiteKingLocation = (tempKing[0], pos)
                inCheck, temp, temp = self.checkForPinsAndChecks()    
                totalCheck = totalCheck or inCheck
            self.whiteKingLocation = tempKing
        else: 
            for pos in positions:
                self.blackKingLocation =  (tempKing[0], pos)
                inCheck, temp, temp = self.checkForPinsAndChecks()    
                totalCheck = totalCheck or inCheck
            self.blackKingLocation = tempKing            

        return totalCheck

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]            

        directions = ((-1, 0), (0,-1), (1, 0), (0, 1),      # These are Rows
                      (-1, -1), (-1, 1), (1, -1), (1, 1))   # These are diagonals
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K': # Excludes King because of Quirk in getKingMoves
                        if possiblePin == (): 
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:  # 2nd allied piece, so no pin or check in this direction.
                            break 
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # 5 possibilities here based on the enemy piece type.
                        # 1) Orthogonally away from king and enemy piece is a rook
                        # 2) Diagonally away from king and enemy piece is a bishop
                        # 3) 1 square away diagonally from king and piece is a pawn
                        # 4) any direction and piece is a Queen
                        # 5) any direction 1 square away and piece is a king.

                        if  (0 <= j <= 3 and type == 'R') or \
                            (4 <= j <= 7 and type == 'B') or \
                            (i == 1 and type == 'p' and ((enemyColor == "w" and 6 <= j <= 7) or (enemyColor == "b" and 4 <= j <= 5))) or \
                            (type == 'Q' ) or (i == 1 and type == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:  
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else: 
                    break
              
        # Check for knight checks
        knightMoves = ((-2 , -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]           
            if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
               endPiece = self.board[endRow][endCol]
               if endPiece[0] == enemyColor and endPiece[1] == 'N':
                   inCheck = True
                   checks.append((endRow, endCol, m[0], m[1]))
        
        return inCheck, pins, checks

class CastleRights():

    def __init__(self, wks, bks, wqs, bqs) -> None:
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs                                                          

class Move():
    # map keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v:k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v:k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isCastleMove=False) -> None:
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7 ) 

        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"

        self.isCastleMove = isCastleMove
        
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
