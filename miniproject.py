
from cell import Cell

import time
import pygame
from pygame.locals import *
pygame.init()


GREY = (180,180,180)
BLACK = (50, 50, 50)
WHITE = (255,255,255)
GREEN = (115, 212, 50)
RED = (255, 60, 60)
ORANGE = (255, 190, 60)
 

mini_maze = open("mini_maze.txt",'r').read().split('\n')
medium_maze = open("medium_maze.txt",'r').read().split('\n')
big_maze = open("big_maze.txt",'r').read().split('\n')
open_maze = open("open_maze.txt",'r').read().split('\n')
debugging_maze =  open("debugging_maze.txt",'r').read().split('\n')

# function to take the user input and create the maze
def create_maze(maze_file):
    '''takes in a multi-line string, returns a 2d array to represent the maze'''
    maze = []
    for i in maze_file:
        row = []
        maze.append(row)
        for j in i:
            row.append(j)
    return maze


# function to check if the current cell can go in more than one direction
def check_if_split_road(x, y):
    '''takes the current position of the cell, iterates over its neighboring cells,
    and if it can go in multiple paths we add the cell to the nodesList '''
    possiblePathes = 0
    for i in range (y-1, y+2):
        if(0 <= i < HEIGHT and maze[i][x] == ' ' and i != y):
            possiblePathes +=1
        
    for j in range (x-1, x+2):
        if(0 <= j < WIDTH and maze[y][j] == ' ' and j != x):
            possiblePathes +=1
    
    if(possiblePathes > 2):
        newCell = Cell([x, y])
        nodesList.append(newCell)


myStack = []
visited = set()
finalStack = []

# recursive implementation of depth first search algorithm 
def depth_first(maze, x, y, stack, visited, finalStack):    
    if((x, y) not in visited and maze[y][x] != '%'):
        stack.append([x, y])
        visited.add((x, y))
        
        if(maze[y][x] == '.'):
            print(stack)
            for i in stack:
                finalStack.append(i)
            return True

        if (maze[y][x] == ' ' or maze[y][x] == 'P'):
            depth_first(maze, x-1, y, stack, visited, finalStack)#left
        if (maze[y][x] == ' ' or maze[y][x] == 'P'):
            depth_first(maze, x+1, y, stack, visited, finalStack)#right
        if (maze[y][x] == ' ' or maze[y][x] == 'P'):
            depth_first(maze, x, y+1,  stack, visited, finalStack)#bottom
        if (maze[y][x] == ' ' or maze[y][x] == 'P'):
            depth_first(maze, x, y-1, stack, visited, finalStack)#top
        
        stack.pop()
        return False



# function to visualize the maze in the cmd
def show_maze(maze):
        for row in maze:
            print("".join(str(cell) for cell in row))

    

def draw_cell(screen, CELLSIZE, MARGIN, row, column, color):
    pygame.draw.rect(screen,
                            color,
                            [(MARGIN + CELLSIZE) * column + MARGIN,
                            (MARGIN + CELLSIZE) * row + MARGIN,
                            CELLSIZE,
                            CELLSIZE])


def draw_board(screen, CELLSIZE, board, MARGIN):
    for row in range(HEIGHT):
        for column in range(WIDTH):
            color = GREEN
            if board[row][column] == '%':
                color = BLACK
            elif board[row][column] == ' ':
                color = GREY
            elif board[row][column] == '.':
                color = ORANGE
            elif board[row][column] == 'P':
                color = RED
            draw_cell(screen, CELLSIZE, MARGIN, row, column, color)
    pygame.display.flip()



maze = create_maze(big_maze)
HEIGHT = len(maze)
WIDTH = len(maze[0])

CELLSIZE = 15
MARGIN = 0
screen_height = HEIGHT*(CELLSIZE+MARGIN)
screen_width = WIDTH*(CELLSIZE+MARGIN)
size = (screen_width, screen_height)  

nodesList = []
startPosition = []
endPosition = []

for i in range(HEIGHT):
    for j in range(WIDTH):
        if maze[i][j] == '.':
            endPosition = [j, i]
        if maze[i][j] == 'P':
            startPosition = [j, i]

print(startPosition)
print(endPosition)


for i in range(HEIGHT):
    for j in range(WIDTH):
        if(maze[i][j] == ' ' or maze[i][j] == 'P'):
            check_if_split_road(j, i)

print(len(nodesList))

for i in nodesList:
    print(i.position)

show_maze(maze)

print("hi")
print(depth_first(maze, startPosition[0], startPosition[1], myStack, visited, finalStack))
print("bye")

show_maze(maze)

print(finalStack)
print(myStack)

for i in finalStack:
    x=i[0]
    y=i[1]
    maze[y][x] = "x"

maze[startPosition[1]][startPosition[0]] = "P"
maze[endPosition[1]][endPosition[0]] = "."

show_maze(maze)

while True:
    screen = pygame.display.set_mode(size)
    screen.fill(WHITE)
    draw_board(screen, CELLSIZE, maze, MARGIN)
