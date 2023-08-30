import random

# tables inspired from https://www.chessprogramming.org/Simplified_Evaluation_Function
# Negative value are an interesting twist.

kingScores =  [[+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00],
                [+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00],
                [+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00],
                [+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00],
                [+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00],
                [+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00],
                [+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00],
                [+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00]]

queenScores =  [[-0.20,-0.10,-0.10,-0.05,-0.05,-0.10,-0.10,-0.20],
                [-0.10,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,-0.10],
                [-0.10,+0.00,+0.05,+0.05,+0.05,+0.05,+0.00,-0.10],
                [-0.50,+0.00,+0.05,+0.05,+0.05,+0.05,+0.00,-0.05],
                [+0.00,+0.00,+0.05,+0.05,+0.05,+0.05,+0.00,-0.05],
                [-0.10,+0.05,+0.05,+0.05,+0.05,+0.05,+0.00,-0.10],
                [-0.10,+0.00,+0.05,+0.00,+0.00,+0.00,+0.00,-0.10],
                [-0.20,-0.10,-0.10,-0.05,-0.05,-0.10,-0.10,-0.20]]

rookScores =   [[+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00],
                [+0.05,+0.10,+0.10,+0.10,+0.10,+0.10,+0.10,+0.05],
                [-0.05,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,-0.05],
                [-0.05,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,-0.05],
                [-0.05,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,-0.05],
                [-0.05,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,-0.05],
                [-0.05,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,-0.05],
                [-0.00,+0.00,+0.00,+0.05,+0.05,+0.00,+0.00,-0.00]]

bishopScores = [[-0.20,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.20],
                [-0.10,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,-0.10],
                [-0.10,+0.00,+0.05,+0.10,+0.10,+0.05,+0.00,-0.10],
                [-0.10,+0.05,+0.05,+0.10,+0.10,+0.05,+0.05,-0.10],
                [-0.10,+0.00,+0.10,+0.10,+0.10,+0.10,+0.00,-0.10],
                [-0.10,+0.10,+0.10,+0.10,+0.10,+0.10,+0.10,-0.10],
                [-0.10,+0.05,+0.00,+0.00,+0.00,+0.00,+0.05,-0.10],
                [-0.20,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.20]]

knightScores = [[-0.50,-0.40,-0.30,-0.30,-0.30,-0.30,-0.40,-0.50],
                [-0.40,-0.20,+0.00,+0.00,+0.00,+0.00,-0.20,-0.40],
                [-0.30,+0.00,+0.10,+0.15,+0.15,+0.10,+0.00,-0.30],
                [-0.30,+0.05,+0.15,+0.20,+0.20,+0.15,+0.05,-0.30],
                [-0.30,+0.00,+0.15,+0.20,+0.20,+0.15,+0.00,-0.30],
                [-0.30,+0.05,+0.10,+0.15,+0.15,+0.10,+0.05,-0.30],
                [-0.40,-0.20,+0.00,+0.05,+0.05,+0.00,-0.20,-0.40],
                [-0.50,-0.40,-0.30,-0.30,-0.30,-0.30,-0.40,-0.50]]

PawnScores =   [[+9.00,+9.00,+9.00,+9.00,+9.00,+9.00,+9.00,+9.00],
                [+0.80,+0.80,+0.80,+0.80,+0.80,+0.80,+0.80,+0.80],
                [+0.35,+0.50,+0.50,+0.50,+0.50,+0.50,+0.50,+0.35],
                [+0.15,+0.25,+0.30,+0.45,+0.45,+0.30,+0.25,+0.15],
                [+0.10,+0.20,+0.20,+0.40,+0.40,+0.20,+0.20,+0.10],
                [+0.15,+0.00,-0.10,+0.10,+0.10,-0.10,+0.00,+0.15],
                [+0.05,+0.10,+0.00,-0.20,-0.20,+0.10,+0.10,+0.05],
                [+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00]]


piecePositionScores = {"wK": kingScores, "bK": kingScores[::-1], 
                       "wQ": queenScores, "bQ": queenScores[::-1], 
                       "wR": rookScores,"bR": rookScores[::-1], 
                       "wB": bishopScores, "bB": bishopScores[::-1],
                       "wN": knightScores, "bN": knightScores[::-1],
                       "wP": PawnScores, "bP": PawnScores[::-1]}

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
MAXDEPTH = 4
positionsScored = 0
searchTreeExportEnable = True # Triggers codes for searchTree export. Requires extra external library openpyxl
searchTree = None

if searchTreeExportEnable: 
    # The export code requires the openpyxl library. https://openpyxl.readthedocs.io
    import ChessTree2Excel as ChessXL # this will enable exporting the searchTree in an Excel file for easy reading.
    searchTree = ChessXL.searchTree(MAXDEPTH)

def findRandomMove(validMoves):
    """ Returns a random move. """

    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove(gs, validMoves, returnQueue):
    """ Helper method to make 1st recursive call """

    global positionsScored
    positionsScored = 0

    if searchTreeExportEnable:
        global currentBestMove # used to display temporary best move across unrelated branches.
        currentBestMove = None
    
    random.shuffle(validMoves) # introduces variety, also allows diffent moves if you undo

    finalScore, finalSeq = NegaMaxAlphaBeta(gs, 
                                  validMoves, 
                                  MAXDEPTH, 
                                  -CHECKMATE - (MAXDEPTH - 1), 
                                  CHECKMATE + (MAXDEPTH - 1), 
                                  1 if gs.whiteToMove else -1, 
                                  [])
    finalBestMove = finalSeq[0]    
    
    # print move summary to terminal
    print("Move#" + str(len(gs.moveLog)// 2 + 1) + 
          "," + ("White" if gs.whiteToMove else "Black") + 
          ", Search Depth: " + str(MAXDEPTH) + 
          ", Positions evaluated: " + f'{positionsScored:6}',
          ", Move: ", f'{str(finalBestMove) : >4}',
          ", Score: ", f'{round(finalScore,2):5}',
          ", Best line:", [str(m) for m in finalSeq]
         )
    
    if searchTreeExportEnable:
        searchTree.saveToExcel("Move#" + str(len(gs.moveLog)// 2 + 1))

    returnQueue.put(finalBestMove)

def NegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, evSign, moveSeq):
    """ 
    This is the NegaMax recursive tree searcher. See https://en.wikipedia.org/wiki/Negamax
    """

    if searchTreeExportEnable: 
        global searchTree # only used for export to Excel 
        global currentBestMove # in export to excel code to display current best move across unrelated branches.

    if depth == 0 or len(validMoves) == 0: # we have reached a leaf or a terminal node.
        return ((evSign * scoreBoard(gs)) - (evSign * depth if gs.checkmate else 0)), moveSeq

    maxScore = -2*CHECKMATE  # this is our negative infinity per the algorithm
    bestSeq = moveSeq.copy()

    for move in validMoves:

        # create the next potential game state for a child node
        gs.makeMove(move)

        currentMoveSeq = moveSeq.copy()
        currentMoveSeq.append(move)

        # generate child nodes: possible move and triggers STALEMATE and CHECKMATE flags
        nextMoves = gs.getValidMoves()

        # call NegaMax on the child nodes
        score, childMoveSeq = NegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -evSign, currentMoveSeq)
        score *= -1

        # this is the equivalent of the max function in the algorithm.        
        if score > maxScore:
            maxScore = score
            bestSeq = childMoveSeq.copy()

            if searchTreeExportEnable:
                if depth == MAXDEPTH: # We are the 1st row of children, record new temporary best move.
                    currentBestMove = move 

        if searchTreeExportEnable: 
            searchTree.insertData(depth, currentMoveSeq, evSign * score, str(currentBestMove))

        gs.undoMove() # return the game state to the prior parent node so we can loop to next child

        if maxScore > alpha: # Can we increase our lower (minimum) boundary?
           alpha = maxScore

        if alpha >= beta:  # If boundaries cross, not longer need to search. Prune child branches. 
            break
  
    return maxScore, bestSeq  

def scoreBoard(gs):
    """ 
    Score the board based on material and others 
    A positive score is good for white. Negative is good for black.
    This scoring function is not affected by who is next to move.
    """

    global positionsScored
    positionsScored += 1

    if gs.checkmate: 
        return CHECKMATE * -1 if gs.whiteToMove else 1
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != '--' and square != 'K':
                score += (pieceScore[square[1]] + 
                          piecePositionScores[square][row][col]) * (1 if square[0] == 'w' else -1)
    return score

