import random
import ChessTree2Excel as ChessXL # requires openpyxl library

DEBUG = True

# tables inspired from https://www.chessprogramming.org/Simplified_Evaluation_Function
# Negative value are an interesting twist.

kingScores =  [[-0.30,-0.40,-0.40,-.050,-0.50,-0.40,-0.40,-0.30],
                [-0.30,-0.40,-0.40,-0.50,-0.50,-0.40,-0.40,-0.30],
                [-0.30,-0.40,-0.40,-0.50,-0.50,-0.40,-0.40,-0.30],
                [-0.30,-0.40,-0.40,-0.50,-0.50,-0.40,-0.40,-0.30],
                [-0.20,-0.30,-0.30,-0.40,-0.40,-0.30,-0.30,-0.20],
                [-0.10,-0.20,-0.20,-0.20,-0.20,-0.20,-0.20,-0.10],
                [+0.20,+0.20,+0.00,+0.00,+0.00,+0.00,+0.20,+0.20],
                [+0.20,+0.30,+0.10,+0.00,+0.00,+0.10,+0.30,+0.20]]

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

PawnScores =  [[+9.00,+9.00,+9.00,+9.00,+9.00,+9.00,+9.00,+9.00],
               [+0.50,+0.50,+0.50,+0.50,+0.50,+0.50,+0.50,+0.50],
               [+0.10,+0.10,+0.20,+0.30,+0.30,+0.20,+0.10,+0.10],
               [+0.05,+0.05,+0.10,+0.25,+0.25,+0.10,+0.05,+0.05],
               [+0.00,+0.00,+0.00,+0.20,+0.20,+0.00,+0.00,+0.00],
               [+0.05,-0.05,-0.10,+0.00,+0.00,-0.10,-0.05,+0.05],
               [+0.05,+0.10,+0.10,-0.20,-0.20,+0.10,+0.10,+0.05],
               [+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00,+0.00]]


piecePositionScores = {"wK": kingScores,"bK": kingScores[::-1],
                       "wQ": queenScores, "bQ": queenScores[::-1], 
                       "wR": rookScores,"bR": rookScores[::-1], 
                       "wB": bishopScores, "bB": bishopScores[::-1],
                       "wN": knightScores, "bN": knightScores[::-1],
                       "wP": PawnScores, "bP": PawnScores[::-1]}

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3.25, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
MAXDEPTH = 4
positionsScored = 0

def findRandomMove(validMoves):
    """ Returns a random move. """

    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove(gs, validMoves, returnQueue):
    """ Helper method to make 1st recursive call """

    global nextMove
    nextMove = None

    global positionsScored
    positionsScored = 0
    
    random.shuffle(validMoves)

    if DEBUG: 
        searchTree = ChessXL.searchTree(MAXDEPTH)
    else: 
        searchTree = None

    finalScore = NegaMaxAlphaBeta(gs, 
                                  validMoves, 
                                  MAXDEPTH, 
                                  -CHECKMATE - (MAXDEPTH - 1), 
                                  CHECKMATE + (MAXDEPTH - 1), 
                                  1 if gs.whiteToMove else -1, 
                                  [], 
                                  searchTree)
    
    # print move summary to terminal
    print("Move#" + str(len(gs.moveLog)// 2 + 1) + 
          "," + ("White" if gs.whiteToMove else "Black") + 
          ", Search Depth: " + str(MAXDEPTH) + 
          ", Positions evaluated: " + f'{positionsScored:6}',
          ", Move: ", f'{str(nextMove) : >4}',
          ", Score: ", f'{round(finalScore * (1 if gs.whiteToMove else -1),2):5}'
         )
    
    if DEBUG:
        searchTree.saveToExcel("Move#" + str(len(gs.moveLog)// 2 + 1))

    returnQueue.put(nextMove)

def NegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, evSign, mList, searchTree):
    """ 
    This is the NegaMax recursive tree searcher. 

    It is pretty simple but hard to understand. 

    I strongly suggest reading these resources including the 100 page animate gif at wikipedia
    https://www.chessprogramming.org/Negamax
    https://en.wikipedia.org/wiki/Negamax

    This function has several parameters including: mList and searchTree.
    - mList and searchTree are only used for debugging and could be removed.
    - mList holds the sequence of move in a branch from top to leaf.
    - searchTree is the python openpyxl object used to create the EXCEL output of the search tree.
    """

    global nextMove

    # Note that we add the depth to our eval function in case of checkmate. 
    # Hence, checkmate + depth of 3 is better than checkmate + depth of 2.
    # Depth is reduced by one for each recursive level so mate in one is MAXDEPT-1, in 2 is MAXDEPTH-2

    if depth == 0 or len(validMoves) == 0:
        return (evSign * scoreBoard(gs)) - (evSign * depth if not gs.stalemate else 0)

    maxScore = -CHECKMATE  # this is our negative infinity per the algorithm

    for move in validMoves:

        # create the next potential game state for a child node
        tempList = mList.copy()
        tempList.append(move)
        gs.makeMove(move)

        # generate child nodes: possible move and triggers STALEMATE and CHECKMATE flags
        nextMoves = gs.getValidMoves()

        # call NegaMax on the child nodes
        score = -NegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -evSign, tempList, searchTree)

        # this is the equivalent of the max function in the algorithm.        
        if score > maxScore:
            maxScore = score
            if depth == MAXDEPTH:
                nextMove = move

        # return the game state to the prior parent node so we can loop to next child
        gs.undoMove()

        if maxScore > alpha: # Can we increase our lower (minimum) boundary?
           alpha = maxScore

        if DEBUG: 
            searchTree.insertData(depth, tempList, evSign * score, str(nextMove))

        if alpha >= beta:  # Can we prune some branches? 
            break
  
    return maxScore  

def scoreBoard(gs):
    """ 
    Score the board based on material and others 
    A positive score is good for white. Negative is good for black.
    This Scoring function is not affected by who is next to move.
    """

    global positionsScored
    positionsScored += 1

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
            if square != '--' and square != 'K': # This ignores the kings positional values
                piecePositionScore = piecePositionScores[square][row][col]
                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePositionScore
    return score
