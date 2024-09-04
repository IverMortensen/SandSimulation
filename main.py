import config
import pygame
import sys
import numpy as np
import random
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

# General settings, can be changed in config.py
SAND_SIZE = config.SAND_SIZE
SETTLING_RATE = config.SETTLING_RATE
DRAW_SIZE = config.DRAW_SIZE
USE_COLORED_SAND = config.USE_COLORED_SAND
SHOW_FPS = config.SHOW_FPS

# Set screen size
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

# Adjust screen width and height to align with sand size
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

# Color settings
BLACK = (0, 0, 0)
BACKGROUND = (35, 35, 36)
SAND_COLOR = (203, 189, 147)
currentRainbowColor = (0, 0, 255)
numColors = 50000
currentColor = 0

def GetRandomSandColor():
    range = 5
    red = random.randint(SAND_COLOR[0]-range, SAND_COLOR[0]+range)
    green = random.randint(SAND_COLOR[1]-range, SAND_COLOR[1]+range)
    blue = random.randint(SAND_COLOR[2]-range, SAND_COLOR[2]+range)
    return red, green, blue

def getRainbowColors(num_colors):
    cmap = plt.get_cmap("rainbow")  # Use the 'rainbow' colormap
    return [cmap(i) for i in np.linspace(0, 1, num_colors)]
if USE_COLORED_SAND:
    rainbowColors = getRainbowColors(numColors)

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

    # Find each sand partice in the sand matrix
    for y, row in enumerate(sandMatrix):
        for x, value in enumerate(row):
            if value == 1:
                # Get the color of the sand particle
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

def CreateSandPartice(sandMatrix, colorMatrix, column, row):
    global currentColor
    if column > -1 and column < COLUMS:
        if row > -1 and row < ROWS:
            if sandMatrix[row][column]:
                return
            
            if USE_COLORED_SAND:
                color = rainbowColors[currentColor]
                sandColor = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
                currentColor = (currentColor + 1 ) % numColors
            else:
                sandColor = GetRandomSandColor()
            
            sandMatrix[row][column] = 1
            colorMatrix[row][column] = sandColor

def MouseDraw(sandMatrix, colorMatrix, drawSize=5):
    mousePosition = pygame.mouse.get_pos()
    mouseRow = int(mousePosition[1] / SAND_SIZE)
    mouseColumn = int(mousePosition[0] / SAND_SIZE)

    for column in range(drawSize):
        for row in range(drawSize):
            sandColumn = int(column + mouseColumn - (drawSize/2))
            sandRow = int(row + mouseRow - (drawSize/2))

            CreateSandPartice(sandMatrix, colorMatrix, sandColumn, sandRow)
    
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

        # Draw new sand if the mouse is pressed
        if pygame.mouse.get_pressed()[0]:
            MouseDraw(sandMatrix, colorMatrix, DRAW_SIZE)

        # Update the sand and color matrix for the next frame
        sandMatrix, colorMatrix = UpdateMatrix(sandMatrix, colorMatrix)

        # Clear the screen
        screen.fill(BACKGROUND)

        # Draw the sand to the screen
        DrawMatrix(screen, sandMatrix, colorMatrix)

        # Draw the framerate (if on)
        if SHOW_FPS:
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
