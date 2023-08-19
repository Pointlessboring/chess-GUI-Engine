"""
This is our main driver file. It is responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512            # Ideally divisible by DIMENSION below
DIMENSION = 8                   # Chess board is 8x8. 
SQ_SIZE = HEIGHT // DIMENSION   
MAX_FPS = 15                    # For animations later on
IMAGES = {}

"""
Initialize a global dictionary of images. This will be called once in main.
"""

def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for pieces in pieces:
        IMAGES[pieces] = p.transform.scale(p.image.load("images/" + pieces + ".png"), (SQ_SIZE,SQ_SIZE))

"""
The main driver for our code. This will handle user input and updating the graphics
"""

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

"""
Responsible for all graphics with a current game state
"""
def drawGameState(screen, gs):
    drawBoard(screen) # Draws squares
    drawPieces(screen, gs.board) # Draw pieces on top of the squares

"""
Draw the squares on the board.
"""
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range (DIMENSION):
        for c in range (DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
"""
Draw the pieces on the board using the current GameState.board
"""
def drawPieces(screen, board):
    for r in range (DIMENSION):
        for c in range (DIMENSION):
            piece = board[r][c]
            if piece != "--": # Not an empty square
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()

