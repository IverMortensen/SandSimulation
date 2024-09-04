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
    range = 10
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

def DrawMatrix(surface, matrix):
    for y, row in enumerate(matrix):
        for x, value in enumerate(row):
            if value == 1:
                DrawSand(surface, x, y, SAND_SIZE, SAND_COLOR)

def UpdateMatrix(matrix):
    newMatrix = CreateMatrix(COLUMS, ROWS)

    for y, row in enumerate(matrix):
        for x, value in enumerate(row):

            if value == 1:

                # Hitting bottom of screen?
                if y+1 == ROWS:
                    newMatrix[y][x] = 1

                # Sand bellow?
                elif matrix[y+1][x] == 1:

                    # No sand on the left
                    if x-1 > 0 and matrix[y+1][x-1] == 0 and not random.randint(0,3):
                        newMatrix[y+1][x-1] = 1

                    # No sand on the right
                    elif x+1 < COLUMS and matrix[y+1][x+1] == 0 and not random.randint(0,3):
                        newMatrix[y+1][x+1] = 1
                    
                    # Stand still
                    else:
                        newMatrix[y][x] = 1
                # Fall
                else:
                    newMatrix[y+1][x] = 1

    return newMatrix

def MouseDraw(matrix):
    mousePosition = pygame.mouse.get_pos()
    row = int(mousePosition[1] / SAND_SIZE)
    column = int(mousePosition[0] / SAND_SIZE)

    matrix[row][column] = 1

    matrix[row-1][column] = 1
    matrix[row-2][column] = 1
    matrix[row-3][column] = 1

    matrix[row+1][column] = 1
    matrix[row+2][column] = 1
    matrix[row+3][column] = 1

    matrix[row][column-1] = 1
    matrix[row][column-2] = 1
    matrix[row][column-3] = 1

    matrix[row][(column+1)%COLUMS] = 1
    matrix[row][(column+2)%COLUMS] = 1
    matrix[row][(column+3)%COLUMS] = 1

    matrix[row+1][(column+1)%COLUMS] = 1
    matrix[row+1][(column+2)%COLUMS] = 1
    matrix[row+2][(column+1)%COLUMS] = 1

    matrix[row-1][(column+1)%COLUMS] = 1
    matrix[row-1][(column+2)%COLUMS] = 1
    matrix[row-2][(column+1)%COLUMS] = 1

    matrix[row+1][column-1] = 1
    matrix[row+1][column-2] = 1
    matrix[row+2][column-1] = 1

    matrix[row-1][column-1] = 1
    matrix[row-1][column-2] = 1
    matrix[row-2][column-1] = 1
    

def DrawFPS():
    # Get the frame rate
    fps = clock.get_fps()

    # Render the FPS text
    fps_text = font.render(f"FPS: {int(fps)}", True, (0, 0, 0))
    screen.blit(fps_text, (10, 10))


def main():
    matrix = CreateMatrix(COLUMS, ROWS)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # LOGIC
        if pygame.mouse.get_pressed()[0]:
            MouseDraw(matrix)

        matrix = UpdateMatrix(matrix)
        # Fill the screen with white
        screen.fill(NIGHT_MODE)

        # Drawing code goes here
        # DrawGrid(screen, COLUMS, ROWS)
        DrawMatrix(screen, matrix)
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
