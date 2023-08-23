import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
MAXDEPTH = 3

def findRandomMove(validMoves):
    """ Returns a random move. """
    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove(gs, validMoves):
    """ Returns a best move based on material value """
    # Delete ME
    
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)

    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.stalemate: 
            opponentMaxScore = STALEMATE
        elif gs.checkmate: 
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkmate: 
                    score = CHECKMATE
                elif gs.stalemate: 
                    score = STALEMATE
                else: 
                    score = -turnMultiplier * scoreMaterial(gs.board) 
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()
        if  opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove() # return to actual board position
    return bestPlayerMove

def findBestMoveMinMax(gs, validMoves):
    """ Helper method to make 1st recursive call """
    global nextMove
    nextMove = None
    findMoveMinMax(gs, validMoves, MAXDEPTH, gs.whiteToMove)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == MAXDEPTH:
                    nextMove = move 
            gs.undoMove()
        return maxScore
    
    else: 
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)           
            if score < minScore:
                minScore = score
                if depth == MAXDEPTH:
                    nextMove = move 
            gs.undoMove()
        return minScore    

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