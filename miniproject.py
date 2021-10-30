
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
BLUE = (60, 120, 255)
 

mini_maze = open("mini_maze.txt",'r').read().split('\n')
medium_maze = open("medium_maze.txt",'r').read().split('\n')
big_maze = open("big_maze.txt",'r').read().split('\n')
open_maze = open("open_maze.txt",'r').read().split('\n')
debugging_maze =  open("debugging_maze.txt",'r').read().split('\n') #this is a very small maze i created for debbuging purpose

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




# recursive implementation of depth first search algorithm 
def depth_first(maze, x, y, stack, visited, screen): 
    """first checks if the current cell is not visited before and not a wall
    and adds it to the stack that holds the possible path"""   
    if((x, y) not in visited and maze[y][x] != '%'):
        stack.append([x, y])
        visited.add((x, y))

        """the terminating condition of the recursive function, if we reached the end
        return true to end the function after filling the stack"""
        if(maze[y][x] == '.'):
            maze[y][x] = "x"
            draw_board(screen, CELLSIZE=15, board=maze, MARGIN=0)
            print(stack)
            return True
        """the function tries every possible path in the following orientation R-L-B-T,
        every time the function checks whether we solved the maze or not before it 
        moves to a new direction"""
        maze[y][x] = "*"
        draw_board(screen, CELLSIZE=15, board=maze, MARGIN=0)
        time.sleep(0.01)
        isSolved = depth_first(maze, x+1, y, stack, visited, screen)#right
        if (not isSolved):
            isSolved = depth_first(maze, x-1, y, stack, visited, screen)#left
        if (not isSolved):
            isSolved = depth_first(maze, x, y+1,  stack, visited, screen)#bottom
        if (not isSolved):
            isSolved = depth_first(maze, x, y-1, stack, visited, screen)#top
        if (isSolved):
            maze[y][x] = "x"
            draw_board(screen, CELLSIZE=15, board=maze, MARGIN=0)
            time.sleep(0.05)
            return True
        """if the maze is not solved after trying R-L-B-T, 
        and we reached a dead-end, the function removes the
        cell from the stack and returns false to trackback to the previous node """
        stack.pop()
        return False
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


# function to draw a gui using pygame library
def draw_board(screen, CELLSIZE, board, MARGIN):
    for row in range(HEIGHT):
        for column in range(WIDTH):
            color = GREY
            if board[row][column] == '%': # wall
                color = BLACK
            elif board[row][column] == 'x': # final path
                color = GREEN
            elif board[row][column] == '.': # end position
                color = ORANGE
            elif board[row][column] == 'P': # starting position
                color = RED
            elif board[row][column] == '*': # searched area
                color = BLUE
            draw_cell(screen, CELLSIZE, MARGIN, row, column, color)
    pygame.display.flip()



maze = create_maze(medium_maze)
HEIGHT = len(maze)
WIDTH = len(maze[0])

CELLSIZE = 15
MARGIN = 0
screen_height = HEIGHT*(CELLSIZE+MARGIN)
screen_width = WIDTH*(CELLSIZE+MARGIN)
size = (screen_width, screen_height)  

myStack = []
visited = set() 

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

print(myStack)


while True:
    screen = pygame.display.set_mode(size)
    screen.fill(WHITE)
    draw_board(screen, CELLSIZE, maze, MARGIN)
    depth_first(maze, startPosition[0], startPosition[1], myStack, visited, screen)
    maze[startPosition[1]][startPosition[0]] = "P"
    maze[endPosition[1]][endPosition[0]] = "."
    draw_board(screen, CELLSIZE, maze, MARGIN)

