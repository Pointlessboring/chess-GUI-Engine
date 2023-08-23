"""
This is our main driver file. It is responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
import ChessEngine
import ChessAI

DIMENSION = 8                   # Chess board is 8x8.
WIDTH = HEIGHT = 512            # Ideally divisible by DIMENSION
SQ_SIZE = HEIGHT // DIMENSION   
MAX_FPS = 15                    # For animations later on
IMAGES = {}
COLORS = ["white", "gray"]      # Colors for the squares

def loadImages():
    """ Initialize a global dictionary of images. This will be called once in main. """

    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    for pieces in pieces:
        IMAGES[pieces] = p.transform.scale(p.image.load("images/" + pieces + ".png"), (SQ_SIZE,SQ_SIZE))

def main():
    """ The main driver for our code. This will handle user input and updating the graphics """

    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    playerOne = True  #True if Human, False if AI
    playerTwo = False #True if Human, False if AI

    moveMade = False #Flag variable when a move is made. 
    animate = False #flag variable, do we need to animate the move.

    loadImages()
    running = True
    sqSelected = () # (row, col) tuple. Keeps track of the last click of the user
    playerClicks = [] # keeps track of player clicks (two tuples: ex: [(6,4), (4,4)]
    gameOver = False

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or \
                    (not(gs.whiteToMove) and playerTwo)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not(gameOver) and humanTurn:
                    location = p.mouse.get_pos() # (x,y) location of mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row,col): # did the user click the same square again
                        sqSelected = () # deselect
                        playerClicks = []
                    else: 
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2: #after 2nd click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = () # Reset user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False

                if e.key == p.K_r: #Reset the board when 'r' is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

        # AI Move finder logic
        if not(humanTurn) and not(gameOver):
            AIMove = ChessAI.findBestMoveMinMax(gs, validMoves)
            if AIMove is None: 
                AIMove = ChessAI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade == True:
            if animate == True: 
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
            print(str(int((len(gs.moveLog)+1)/2)) + ('w' if not(gs.whiteToMove) else 'b'), gs.moveLog[-1].getChessNotation())

        drawGameState(screen,gs, validMoves, sqSelected)

        if gs.checkmate:
            gameOver = True
            drawText(screen, ('Black' if gs.whiteToMove else 'White') + ' wins by checkmate')
        if gs.stalemate:
            drawText(screen, 'Stalemate')
        clock.tick(MAX_FPS)
        p.display.flip()



def highlightSquare(screen, gs, validMoves, sqSelected):
    """ Highlight square selected and moves for the piece selected """

    if sqSelected !=():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            #highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # 100 is the transparency value 0 = invisible, 255 is solid.
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight moves from that square
            s.fill(p.Color('yellow'))

            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))
         
def drawGameState(screen, gs, validMoves, sqSelected):
    """ Responsible for all graphics with a current game state """

    drawBoard(screen) # Draws squares
    highlightSquare(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) # Draw pieces on top of the squares

def drawBoard(screen):
    """ Draw the squares on the board. """

    for r in range (DIMENSION):
        for c in range (DIMENSION):
            color = p.Color(COLORS[(r+c)%2])
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    """ Draw the pieces on the board using the current GameState.board """

    for r in range (DIMENSION):
        for c in range (DIMENSION):
            piece = board[r][c]
            if piece != "--": # Not an empty square
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def animateMove(move, screen, board, clock):
    """ Animating a move """

    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #frames to move one square.
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare

    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame/frameCount, move.startCol + dC * frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = p.Color(COLORS[(move.endRow + move.endCol)%2])
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE) # erase piece at destination.
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE ,r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    """ Write Message in middle of screen """

    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('White'))
    textlocation = p.Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textlocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textlocation.move(2, 2))

if __name__ == "__main__":
    main()

