import pygame
import random

# Maze dimensions
ROWS, COLS = 20, 20
CELL_SIZE = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PATH_COLOR = (0, 0, 255)

# Directions for movement
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


"""
is_valid_move function:
@param maze: list of lists representing the maze
@param position: tuple representing the position to check
@return: True if the position is a valid move, False otherwise
"""

def is_valid_move(maze, position):
    row, col = position
    return 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] == 1


"""
mark_path function:
@param maze: list of lists representing the maze
@param path: list of tuples representing the path to mark
@return: list of lists representing the maze with the path marked
"""
def mark_path(maze, path):
    new_maze = [row[:] for row in maze]
    for row, col in path:
        new_maze[row][col] = 2
    return new_maze

def print_maze(maze):
    for row in maze:
        print(" ".join(str(cell) for cell in row))

"""
generate_maze function: use Prim's algorithm to generate a maze
@param rows: number of rows in the maze
@param cols: number of columns in the maze
@return: list of lists representing the maze
"""
def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    start_row, start_col = random.randint(0, rows - 1), random.randint(0, cols - 1)
    maze[start_row][start_col] = 0
    walls = []
    for dr, dc in DIRECTIONS:
        row, col = start_row + dr, start_col + dc
        if 0 <= row < rows and 0 <= col < cols:
            walls.append((row, col))
    while walls:
        row, col = walls.pop(random.randint(0, len(walls) - 1))
        if maze[row][col] == 1:
            maze[row][col] = 0
            for dr, dc in DIRECTIONS:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < rows and 0 <= new_col < cols and maze[new_row][new_col] == 0:
                    maze[row + dr // 2][col + dc // 2] = 0
                    walls.append((new_row, new_col))
    return maze
    

   


"""
next_move function: use a depth-first search to find the next move to the target position
@param maze: list of lists representing the maze
@param position: tuple representing the current position
@param target: tuple representing the target position
@param visited: set of tuples representing the visited positions
@return: list of tuples representing the path to the target position
"""
def find_path(maze, position, target, visited):
    pass
    


"""
draw_grid function:
@param screen: pygame.Surface object
@param maze: list of lists representing the maze
"""
def draw_grid(screen, maze):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if maze[row][col] == 0 else BLACK
            if maze[row][col] == 2:
                color = PATH_COLOR
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

"""
draw_path function:
@param screen: pygame.Surface object
@param path: list of tuples representing the path to draw
"""
def draw_path(screen, path):
    for row, col in path:
        pygame.draw.rect(screen, PATH_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))



"""
game_loop function:
"""
def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((COLS * CELL_SIZE, ROWS * CELL_SIZE))
    pygame.display.set_caption("Maze Solver")
    clock = pygame.time.Clock()
    
    visited = set()
    maze = generate_maze(ROWS, COLS)
    path = find_path(maze, (0, 0), (ROWS - 1, COLS - 1), visited)
    print_maze(maze)  # Debug print to see the generated maze in the console
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            draw_grid(screen, maze)

            if path:
                draw_path(screen, path)
            pygame.display.flip()
            clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    game_loop()
