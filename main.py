# Import and initialize the pygame library
from turtle import width
import pygame
pygame.init()

# Set up the drawing window
WIDTH, HEIGHT = 800, 500
SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()
# Run until the user asks to quit
running = True
# Variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DIRT = (87, 58, 2)
speed = 5
charx, chary = 20, 300
board = [
    [[],[],[],[],[],[],[],[],[],[]], 
    [[],[],[],[],[],[],[],[],[],[]], 
    [[],[],[],[],[],[],[],[],[],[]], 
    [[],[],[],[],[],[],[],[],[],[]], 
    [[],[],[],[],[],[],[],[],[],[]], 
    [[],[],[],[],[],[],[],[],[],[]], 
    [[],[],[],[],[],[],[],[],[],[]], 
    [[],[],[],[],[],[],[],[],[],[]], 
    [["Ground"],["Ground"],["Ground"],["Ground"],["Ground"],["Ground"],["Ground"],["Ground"],["Ground"],["Ground"]], 
    [[],[],[],[],[],[],[],[],[],[]],
]
GRIDHEIGHT = HEIGHT/10
GRIDWIDTH = WIDTH/10
# Functions
def drawGrid(color):
    for rows in range(0, HEIGHT, int(GRIDHEIGHT)):
        pygame.draw.line(screen, color, [0, rows], [WIDTH, rows])
    for columns in range(0, WIDTH, int(GRIDWIDTH)):
        pygame.draw.line(screen, color, [columns, 0], [columns, HEIGHT])
        
def drawBoard():
    for rows in range(len(board)):
        for columns in range(len(board[rows])):
            if (board[rows][columns] == ["Ground"]):
                pygame.draw.rect(screen, DIRT, [columns*int(GRIDWIDTH), rows*int(GRIDHEIGHT), int(GRIDWIDTH), int(GRIDHEIGHT)])
    

def drawChar(color, x, y):
    pygame.draw.rect(screen, color, [x, y, 50, 50])

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Fill the background with white
    screen.fill(WHITE)
    # Character movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        charx -= speed
    if keys[pygame.K_d]:
        charx += speed
    # Grid
    drawGrid(BLACK)
    drawChar(RED, charx, chary)
    drawBoard()
    # Flip the display
    pygame.display.flip()
    clock.tick(30)
# Done! Time to quit.
pygame.quit()