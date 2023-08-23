import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
MAXDEPTH = 2

def findRandomMove(validMoves):
    """ Returns a random move. """
    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove(gs, validMoves):
    """ Helper method to make 1st recursive call """
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    #findMoveNegaMax(gs, validMoves, MAXDEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, MAXDEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print("Positions reviewed", counter)
    return nextMove

def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    # DeleteMe as we improved this to NegaMaxAlphaBeta
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreMaterial(gs.board)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == MAXDEPTH:
                nextMove = move
              
        gs.undoMove()
    return maxScore    

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreMaterial(gs.board)

    #move ordering - Implement this later

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
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score

def scoreMaterial(board):
    """ Score the board based on material """
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score