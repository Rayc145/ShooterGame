# Import and initialize the pygame library
from string import whitespace
import pygame
pygame.init()
import json
# Set up the drawing window
WIDTH, HEIGHT = 700, 700
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
charx, chary = 100, 350
speed, jumpSpeed = 0, 0
inAir = False
GRIDHEIGHT = HEIGHT/20
GRIDWIDTH = WIDTH/20
page = "menu"

# Functions
def drawGrid(color):
    for rows in range(0, HEIGHT, int(GRIDHEIGHT)):
        pygame.draw.line(screen, color, [0, rows], [WIDTH, rows])
    for columns in range(0, WIDTH, int(GRIDWIDTH)):
        pygame.draw.line(screen, color, [columns, 0], [columns, HEIGHT])

class Player:
    def __init__(self, x, y):
        self.width = 35
        self.height = 35
        self.color = RED
        self.jumpSpeed = 0
        self.inAir = False
        self.rect = pygame.draw.rect(screen, self.color, [x, y, self.width, self.height])
        self.rect.x = x
        self.rect.y = y

    def update(self, listOfTiles):
        # Character movement
        dy = 0
        dx = 0
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_a]:
            dx = -5
        if keys[pygame.K_d]:
            dx = 5
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and not self.inAir:
            self.inAir = True
            self.jumpSpeed = -15   
        self.jumpSpeed += 1    
        if self.jumpSpeed > 10:
            self.jumpSpeed = 10
            self.inAir = True
        dy += self.jumpSpeed
        # Character collision
        for tile in listOfTiles:
            if tile.colliderect(self.rect.x, self.rect.y+dy, self.width, self.height):
                if self.jumpSpeed < 0:
                    dy = tile.bottom - self.rect.top 
                    self.jumpSpeed = 0
                elif self.jumpSpeed >= 0:
                    dy = tile.top - self.rect.bottom
                    self.inAir = False
            if tile.colliderect(self.rect.x+dx, self.rect.y, self.width, self.height):
                dx = 0
        self.rect.y += dy
        self.rect.x += dx
        pygame.draw.rect(screen, self.color, [self.rect.x, self.rect.y, self.width, self.height])

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.menuColor = BLACK
        self.font = pygame.font.SysFont("Arial", int(self.height)*2, False, False)
        with open("levels.json", "r") as readFile:
            data = json.load(readFile)
            self.board = data["level1"]
        """self.board = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], 
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],  
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],  
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],     
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],  
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],  
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],  
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],  
            [1,0,0,1,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1], 
            [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], 
        ]"""
        self.listOfTiles = []

    def drawBoard(self):
        for rows in range(len(self.board)):
            for columns in range(len(self.board[rows])):
                if (self.board[rows][columns] == 1):
                    self.listOfTiles.append(pygame.draw.rect(screen, DIRT, [columns*int(self.width), rows*int(self.height), int(self.width), int(self.height)]))

    def gameMaker(self, mousePos, button):
        #1 - left, 2 - middle, 3 - right, 4 - scroll up, 5 - scroll down
        (x, y) = mousePos
        if button == 1:
            self.board[int(y/int(self.height))][int(x/int(self.width))] = 1
        elif button == 3:
            self.board[int(y/int(self.height))][int(x/int(self.width))] = 0

    def mainMenu(self):
        menuText = self.font.render("Menu", True, BLACK)
        screen.blit(menuText, (int(self.width)*8, int(self.height)))
        editorText = self.font.render("Editor", True, WHITE)
        pygame.draw.rect(screen, self.menuColor, [int(self.width)*7, int(self.height)*6, int(self.width)*6, int(self.height)*2])
        screen.blit(editorText, (int(self.width)*8, int(self.height)*6-5))
    
    def mainMenuEvents(self, mousePos):
        global page
        (x, y) = mousePos
        if int(self.width)*7 < x < int(self.width)*13 and int(self.height)*6 < y < int(self.height)*8:
            page = "editor"
    
gameBoard = Game(GRIDWIDTH, GRIDHEIGHT)
character = Player(100, 350)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("levels.json", "r") as readFile:
                data = json.load(readFile)
            data["level1"] = gameBoard.board
            with open("levels.json", "w") as writeFile:
                json.dump(data, writeFile)
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if page == "menu":
                gameBoard.mainMenuEvents(pygame.mouse.get_pos())
            elif page == "editor":
                gameBoard.gameMaker(pygame.mouse.get_pos(), event.button)
    # Fill the background with white
    screen.fill(WHITE)
    # Grid
    drawGrid(BLACK)
    if page == "menu":
        gameBoard.mainMenu()
    elif page == "editor":
        gameBoard.drawBoard()
        character.update(gameBoard.listOfTiles)
    # Flip the display
    pygame.display.flip()
    clock.tick(30)
# Done! Time to quit.
pygame.quit()