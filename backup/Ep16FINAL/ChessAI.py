import random

# tables imported from https://www.chessprogramming.org/Simplified_Evaluation_Function
# Negative value are an interesting twist.

kingScores =  [[-30,-40,-40,-50,-50,-40,-40,-30],
                [-30,-40,-40,-50,-50,-40,-40,-30],
                [-30,-40,-40,-50,-50,-40,-40,-30],
                [-30,-40,-40,-50,-50,-40,-40,-30],
                [-20,-30,-30,-40,-40,-30,-30,-20],
                [-10,-20,-20,-20,-20,-20,-20,-10],
                [20, 20,  0,  0,  0,  0, 20, 20],
                [20, 30, 10,  0,  0, 10, 30, 20]]

queenScores =  [[-20,-10,-10, -5, -5,-10,-10,-20],
                [-10,  0,  0,  0,  0,  0,  0,-10],
                [-10,  0,  5,  5,  5,  5,  0,-10],
                [-5,  0,  5,  5,  5,  5,  0, -5],
                [0,  0,  5,  5,  5,  5,  0, -5],
                [-10,  5,  5,  5,  5,  5,  0,-10],
                [-10,  0,  5,  0,  0,  0,  0,-10],
                [-20,-10,-10, -5, -5,-10,-10,-20]]

rookScores =   [[0,  0,  0,  0,  0,  0,  0,  0],
                [5, 10, 10, 10, 10, 10, 10,  5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [0,  0,  0,  5,  5,  0,  0,  0]]

bishopScores = [[-20,-10,-10,-10,-10,-10,-10,-20],
                [-10,  0,  0,  0,  0,  0,  0,-10],
                [-10,  0,  5, 10, 10,  5,  0,-10],
                [-10,  5,  5, 10, 10,  5,  5,-10],
                [-10,  0, 10, 10, 10, 10,  0,-10],
                [-10, 10, 10, 10, 10, 10, 10,-10],
                [-10,  5,  0,  0,  0,  0,  5,-10],
                [-20,-10,-10,-10,-10,-10,-10,-20]]

knightScores = [[-50,-40,-30,-30,-30,-30,-40,-50],
                [-40,-20,  0,  0,  0,  0,-20,-40],
                [-30,  0, 10, 15, 15, 10,  0,-30],
                [-30,  5, 15, 20, 20, 15,  5,-30],
                [-30,  0, 15, 20, 20, 15,  0,-30],
                [-30,  5, 10, 15, 15, 10,  5,-30],
                [-40,-20,  0,  5,  5,  0,-20,-40],
                [-50,-40,-30,-30,-30,-30,-40,-50]]

PawnScores =  [[900,  900,  900,  900,  900,  900,  900,  900],
               [50, 50, 50, 50, 50, 50, 50, 50],
               [10, 10, 20, 30, 30, 20, 10, 10],
               [5,  5, 10, 25, 25, 10,  5,  5],
               [0,  0,  0, 20, 20,  0,  0,  0],
               [5, -5,-10,  0,  0,-10, -5,  5],
               [5, 10, 10,-20,-20, 10, 10,  5],
               [0,  0,  0,  0,  0,  0,  0,  0]]


piecePositionScores = {"wK": kingScores,"bK": kingScores[::-1],
                       "wQ": queenScores, "bQ": queenScores[::-1], 
                       "wR": rookScores,"bR": rookScores[::-1], 
                       "wB": bishopScores, "bB": bishopScores[::-1],
                       "wN": knightScores, "bN": knightScores[::-1],
                       "wP": PawnScores, "bP": PawnScores[::-1]}

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
MAXDEPTH = 4

def findRandomMove(validMoves):
    """ Returns a random move. """

    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove(gs, validMoves, returnQueue):
    """ Helper method to make 1st recursive call """

    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMoveNegaMaxAlphaBeta(gs, validMoves, MAXDEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    returnQueue.put(nextMove)

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    #TODO: move ordering - Implement this later

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == MAXDEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha: #pruning happens
           alpha = maxScore
        if alpha >= beta:
            break 
    return maxScore  

def scoreBoard(gs):
    """ 
    Score the board based on material and others 
    A positive score is good for white. Negative is good for black.
    """
    if gs.checkmate: 
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != '--':
                # score it positionally
                piecePositionScore = piecePositionScores[square][row][col]

                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore / 100
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePositionScore / 100
    return score
