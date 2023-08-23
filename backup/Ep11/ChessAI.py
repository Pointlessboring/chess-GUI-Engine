import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0

def findRandomMove(validMoves):
    """ Returns a random move. """
    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove(gs, validMoves):
    """ Returns a best move based on material value """

    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)

    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        opponentMaxScore = -CHECKMATE

        for opponentsMove in opponentsMoves:
            gs.makeMove(opponentsMove)
            if gs.checkmate: 
                score = turnMultiplier * CHECKMATE
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