import pygame
import sys
import numpy as np
from time import sleep
import random

# Initialize Pygame
pygame.init()

# Width and height of each sand particle
SAND_SIZE = 4

# How long the sand takes to reach equilibrium (settle down)
SETTLING_RATE = 3

# Size of the sand drawing tool
DRAW_SIZE = 8

# Set screen size
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

# Adjust screen width and height align width sand size
SCREEN_WIDTH = SCREEN_WIDTH - (SCREEN_WIDTH % SAND_SIZE)
SCREEN_HEIGHT = SCREEN_HEIGHT - (SCREEN_HEIGHT % SAND_SIZE)

COLUMS = int(SCREEN_WIDTH / SAND_SIZE)
ROWS = int(SCREEN_HEIGHT / SAND_SIZE)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sand Simulation")

# Set up clock for managing frame rate
clock = pygame.time.Clock()
FPS = 120

# Set up font for displaying FPS
font = pygame.font.Font(None, 36)

# Define colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NIGHT_MODE = (35, 35, 36)
SAND_COLOR = (203, 189, 147)

def GetRandomSandColor():
    range = 5
    red = random.randint(203-range, 203+range)
    green = random.randint(189-range, 189+range)
    blue = random.randint(147-range, 147+range)
    return red, green, blue

def DrawGrid(surface, colums, rows):
    size = SCREEN_WIDTH / colums

    for i in range(colums):
        xPos = ((i * size), 0)
        yPos = ((i * size), SCREEN_HEIGHT)
        pygame.draw.line(surface, BLACK, xPos, yPos)

    for i in range(rows):
        xPos = (0, (i * size))
        yPos = (SCREEN_WIDTH, (i * size))
        pygame.draw.line(surface, BLACK, xPos, yPos)

def DrawSand(surface, colum, row, size, color=BLACK):
    x = colum * size
    y = row * size
    
    pygame.draw.rect(surface, color, (x, y, size, size))

def CreateMatrix(colums, rows):
    return np.zeros((rows, colums))

def CreateColorMatrix(columns, rows):
    matrix = []
    for row in range(rows):
        matrix.append([])
        for column in range(columns):
            matrix[row].append(0)
    return matrix

def DrawMatrix(surface, sandMatrix, colorMatrix):
    for y, row in enumerate(sandMatrix):
        for x, value in enumerate(row):
            if value == 1:
                DrawSand(surface, x, y, SAND_SIZE, colorMatrix[y][x])

def UpdateMatrix(sandMatrix, colorMatrix):
    newSandMatrix = CreateMatrix(COLUMS, ROWS)
    newColorMatrix = CreateColorMatrix(COLUMS, ROWS)

    for y, row in enumerate(sandMatrix):
        for x, value in enumerate(row):

            if value == 1:
                sandColor = colorMatrix[y][x]

                # Hitting bottom of screen?
                if y+1 == ROWS:
                    newSandMatrix[y][x] = 1
                    newColorMatrix[y][x] = sandColor

                # Sand bellow?
                elif sandMatrix[y+1][x] == 1:

                    # No sand on the left
                    if x-1 > -1 and sandMatrix[y+1][x-1] == 0 and not random.randint(0,3):
                        newSandMatrix[y+1][x-1] = 1
                        newColorMatrix[y+1][x-1] = sandColor

                    # No sand on the right
                    elif x+1 < COLUMS and sandMatrix[y+1][x+1] == 0 and not random.randint(0,3):
                        newSandMatrix[y+1][x+1] = 1
                        newColorMatrix[y+1][x+1] = sandColor

                    # Stand still
                    else:
                        newSandMatrix[y][x] = 1
                        newColorMatrix[y][x] = sandColor

                # Fall
                else:
                    newSandMatrix[y+1][x] = 1
                    newColorMatrix[y+1][x] = sandColor

    return newSandMatrix, newColorMatrix

def CreateSandPartice(sandMatrix, colorMatrix, column, row, color=SAND_COLOR):
    if column > -1 and column < COLUMS:
        sandMatrix[row][column] = 1
        colorMatrix[row][column] = color

def MouseDraw(sandMatrix, colorMatrix, drawSize=5):
    mousePosition = pygame.mouse.get_pos()
    mouseRow = int(mousePosition[1] / SAND_SIZE)
    mouseColumn = int(mousePosition[0] / SAND_SIZE)

    for column in range(drawSize):
        for row in range(drawSize):
            sandColumn = int(column + mouseColumn - (drawSize/2))
            sandRow = int(row + mouseRow - (drawSize/2))
            CreateSandPartice(sandMatrix, colorMatrix, sandColumn, sandRow, GetRandomSandColor())
    

def DrawFPS():
    # Get the frame rate
    fps = clock.get_fps()

    # Render the FPS text
    fps_text = font.render(f"FPS: {int(fps)}", True, (0, 0, 0))
    screen.blit(fps_text, (10, 10))


def main():
    sandMatrix = CreateMatrix(COLUMS, ROWS)
    colorMatrix = CreateColorMatrix(COLUMS, ROWS)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if pygame.mouse.get_pressed()[0]:
            MouseDraw(sandMatrix, colorMatrix, 5)

        sandMatrix, colorMatrix = UpdateMatrix(sandMatrix, colorMatrix)

        screen.fill(NIGHT_MODE)

        # DrawGrid(screen, COLUMS, ROWS)
        DrawMatrix(screen, sandMatrix, colorMatrix)
        DrawFPS()

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
