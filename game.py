import pygame
import random

# Maze dimensions
ROWS, COLS = 40, 80
CELL_SIZE = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DESTINATION = (0, 255, 0)
SOURCE = (255, 0, 0)
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
generate_maze function: use randomized depth-first search to generate a maze
@param rows: number of rows in the maze
@param cols: number of columns in the maze
@return: list of lists representing the maze
"""
def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    stack = [(0, 0)]
    maze[0][0] = 0

    while stack:
        current = stack[-1]
        row, col = current
        directions = random.sample(DIRECTIONS, len(DIRECTIONS))
        moved = False

        for dr, dc in directions:
            new_row, new_col = row + 2 * dr, col + 2 * dc

            if 0 <= new_row < rows and 0 <= new_col < cols and maze[new_row][new_col] == 1:
                maze[row + dr][col + dc] = 0
                maze[new_row][new_col] = 0
                stack.append((new_row, new_col))
                moved = True
                break

        if not moved:
            stack.pop()

    # Ensure connectivity for the left and bottom borders
    for r in range(2, rows, 2):
        maze[r][0] = 0
    for c in range(2, cols, 2):
        maze[0][c] = 0

    return maze
    
    

   


"""
dfs function: use a depth-first search to find the next move to the target position
@param maze: list of lists representing the maze
@param position: tuple representing the current position
@param target: tuple representing the target position
@param visited: set of tuples representing the visited positions
@return: true if the target position is reached, false otherwise
"""
def dfs(maze, position, target, visited, path):
    if position == target:
        path.append(position)
        return True

    row, col = position
    if not (0 <= row < len(maze) and 0 <= col < len(maze[0])) or maze[row][col] != 0 or position in visited:
        return False

    visited.add(position)
    path.append(position)

    for dr, dc in DIRECTIONS:
        new_position = (row + dr, col + dc)
        if dfs(maze, new_position, target, visited, path):
            return True

    path.pop()
    return False


"""
bfs function: use bfs search to find the next move to the target position
@param maze: list of lists representing the maze
@param position: tuple representing the current position
@param target: tuple representing the target position
@return: true if the target position is reached, false otherwise
"""
def bfs(maze, position, target,visited,path):
    queue = [position]
    parent = {position: None}
    visited.add(position)
    while queue:
        current = queue.pop(0)
        if current == target:
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return True
        row, col = current
        for dr, dc in DIRECTIONS:
            new_position = (row + dr, col + dc)
            if is_valid_move(maze, new_position) and new_position not in visited:
                queue.append(new_position)
                visited.add(new_position)
                parent[new_position] = current
    return False

    
    
    


"""
Get the path from the source to the destination
@param maze: list of lists representing the maze
@param source: tuple representing the source position
@param destination: tuple representing the destination position
"""
def get_path(maze, source, destination):
    #initialize visited set and path list
    visited = set()
    path = []

    # depth-first search
    if dfs(maze, source, destination, visited, path):
        return path

    # breadth-first search
    # if bfs(maze, source, destination,visited, path):
    #     print("Path found:[row, col]")
    #     for i in path:
    #         print(i)
    #     return path


    # print("No path found")
    return []     
    

    


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
            # pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

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
    
    start = (0, 0)
    end = (ROWS - 2, COLS - 2)
    visited = set()
    maze = generate_maze(ROWS, COLS)
    path = get_path(maze, start, end)
    print_maze(maze)  # Debug print to see the generated maze in the console
    
    running = True

    current_index = 0
    draw_grid(screen, maze)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if current_index < len(path):
            current_pos = path[current_index]
            current_index += 1
        else:
            current_pos = end

        
        
        # Draw the source and destination
        pygame.draw.rect(screen, SOURCE, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, DESTINATION, (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Draw the moving object
        pygame.draw.rect(screen, PATH_COLOR, (current_pos[1] * CELL_SIZE, current_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()
        clock.tick(80)  # Adjust speed of the moving object


if __name__ == "__main__":
    game_loop()
