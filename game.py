import pygame
import random
import time
import threading

# Maze dimensions
ROWS, COLS = 60, 40
CELL_SIZE = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DESTINATION = (0, 255, 0)
SOURCE = (255, 0, 0)
PATH_COLOR = (0, 0, 255)

# Directions for movement
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def is_valid_move(maze, position):
    row, col = position
    return 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] == 0

def print_maze(maze):
    print("[", end="")
    for row in maze:
        print("[" + ",".join("0" if cell == 0 else "1" for cell in row) + "],")
    print("]")

def generate_maze(rows, cols, algorithm="dfs"): 
    
    #initialize maze with all walls
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    
    #dfs
    # 1. Choose the initial cell, mark it as visited and push it to the stack
    # 2. While the stack is not empty
    #     1. Pop a cell from the stack and make it a current cell
    #     2. If the current cell has any neighbours which have not been visited
    #         1. Push the current cell to the stack
    #         2. Choose one of the unvisited neighbours
    #         3. Remove the wall between the current cell and the chosen cell
    #         4. Mark the chosen cell as visited and push it to the stack

    while True:
        if algorithm == "dfs":
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
            return maze

        #bfs
        # 1. Choose the initial cell, mark it as visited and enqueue it
        # 2. While the queue is not empty
        #     1. Dequeue a cell from the queue and make it a current cell
        #     2. If the current cell has any neighbours which have not been visited
        #         1. Enqueue the neighbour
        #         2. Mark the neighbour as visited
        #         3. Set the neighbour's parent as the current cell

        elif algorithm == "bfs":
            queue = [(random.randint(0, rows - 1) // 2 * 2, random.randint(0, cols - 1) // 2 * 2)]
            maze[queue[0][0]][queue[0][1]] = 0

            while queue:
                current = queue.pop(0)
                row, col = current
                directions = random.sample(DIRECTIONS, len(DIRECTIONS))

                for dr, dc in directions:
                    new_row, new_col = row + 2 * dr, col + 2 * dc

                    if 0 <= new_row < rows and 0 <= new_col < cols and maze[new_row][new_col] == 1:
                        if random.random() < 0.75:  # Introduce a bias to create dead ends
                            maze[row + dr][col + dc] = 0
                            maze[new_row][new_col] = 0
                            queue.append((new_row, new_col))
                        else:
                            maze[row + dr][col + dc] = 0
            return maze

        #handle invalid algorithm
        elif algorithm == "exit":
            break
        else:
            print("Invalid algorithm, please choose either 'dfs' or 'bfs'")
            print("Or leave it empty to use the default algorithm (dfs)")
            print("If you want to exit the program, type 'exit'")     
            algorithm = input("Enter the algorithm you want to use: ") 
    return None

# Draw the maze on the screen
def draw_grid(screen, maze, offset):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if maze[row][col] == 0 else BLACK
            pygame.draw.rect(screen, color, (offset[0] + col * CELL_SIZE, offset[1] + row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# DFS sovler
def dfs_2(maze, start, end, screen, offset):
    # 1. Choose the initial cell, mark it as visited and push it to the stack
    # 2. While the stack is not empty
    #     1. Pop a cell from the stack and make it a current cell
    #     2. If the current cell has any neighbours which have not been visited
    #         1. Push the current cell to the stack
    #         2. Choose one of the unvisited neighbours
    #         3. Remove the wall between the current cell and the chosen cell
    #         4. Mark the chosen cell as visited and push it to the stack

    visited = set()
    def dfs(i, j):
        if (i, j) == end:
            return True
        if (0 <= i < ROWS and 0 <= j < COLS) and maze[i][j] == 0 and (i, j) not in visited:
            visited.add((i, j))
            pygame.draw.rect(screen, PATH_COLOR, (offset[0] + j * CELL_SIZE, offset[1] + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.flip()
            time.sleep(0.005)  # Adjust speed of the visualization

            if dfs(i + 1, j) or dfs(i, j + 1) or dfs(i - 1, j) or dfs(i, j - 1):
                return True

            # Backtracking
            # visited.remove((i, j))
            pygame.draw.rect(screen, WHITE, (offset[0] + j * CELL_SIZE, offset[1] + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.flip()
            time.sleep(0.005)  # Adjust speed of the visualization
        return False

    dfs(start[0], start[1])

# BFS solver
def bfs_2(maze, start, end, screen, offset):
    # 1. Choose the initial cell, mark it as visited and enqueue it
    # 2. While the queue is not empty
    #     1. Dequeue a cell from the queue and make it a current cell
    #     2. If the current cell has any neighbours which have not been visited
    #         1. Enqueue the neighbour
    #         2. Mark the neighbour as visited
    #         3. Set the neighbour's parent as the current cell
    
    queue = [start]
    visited = set()
    parent = {}

    while queue:
        i, j = queue.pop(0)
        
        if (i, j) == end:
            path = []
            while (i, j) != start:
                path.append((i, j))
                i, j = parent[(i, j)]
            path.append(start)
            path.reverse()
            for (i, j) in path:
                pygame.draw.rect(screen, PATH_COLOR, (offset[0] + j * CELL_SIZE, offset[1] + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.display.flip()
                time.sleep(0.005)
            return True
        
        if (0 <= i < ROWS and 0 <= j < COLS) and maze[i][j] == 0 and (i, j) not in visited:
            visited.add((i, j))
            pygame.draw.rect(screen, PATH_COLOR, (offset[0] + j * CELL_SIZE, offset[1] + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.flip()
            time.sleep(0.005)
            
            for (ni, nj) in [(i + 1, j), (i, j + 1), (i - 1, j), (i, j - 1)]:
                if (0 <= ni < ROWS and 0 <= nj < COLS) and maze[ni][nj] == 0 and (ni, nj) not in visited:
                    queue.append((ni, nj))
                    parent[(ni, nj)] = (i, j)
    
    return False

def game_loop():
    
    pygame.init()
    screen = pygame.display.set_mode((COLS * CELL_SIZE * 2, ROWS * CELL_SIZE))
    pygame.display.set_caption("Maze Solver - DFS and BFS")
    
    clock = pygame.time.Clock()
    
    start = (0, COLS - 2)
    end = (ROWS - 2, 0)
    maze_dfs = generate_maze(ROWS, COLS)
    maze_bfs = [row[:] for row in maze_dfs]  # Copy of the maze for BFS
    
    print_maze(maze_dfs)  # Debug print to see the generated maze in the console
    
    draw_grid(screen, maze_dfs, (0, 0))
    draw_grid(screen, maze_bfs, (COLS * CELL_SIZE, 0))

    # Create threads for DFS and BFS
    dfs_thread = threading.Thread(target=dfs_2, args=(maze_dfs, start, end, screen, (0, 0)))
    bfs_thread = threading.Thread(target=bfs_2, args=(maze_bfs, start, end, screen, (COLS * CELL_SIZE, 0)))

    # Start the threads
    dfs_thread.start()
    bfs_thread.start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the source and destination on both mazes
        pygame.draw.rect(screen, SOURCE, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, DESTINATION, (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        pygame.draw.rect(screen, SOURCE, (COLS * CELL_SIZE + start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, DESTINATION, (COLS * CELL_SIZE + end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()
        clock.tick(80)  # Adjust speed of the moving object

    pygame.quit()


    #Give user the option to choose the algorithm
    #Still need to fix the bug where the maze is not displayed
    #Also need to fix the bug where the path is not displayed
    # pygame.init()
    # screen = pygame.display.set_mode((COLS * CELL_SIZE, ROWS * CELL_SIZE))
    # pygame.display.set_caption("Maze Solver - BFS and DFS")

    # clock = pygame.time.Clock()

    # start = (0, COLS - 2)
    # end = (ROWS - 2, 0)
    # maze = generate_maze(ROWS, COLS)

    # print_maze(maze)  # Debug print to see the generated maze in the console

    # draw_grid(screen, maze, (0, 0))

    # print("Options: BFS, DFS, BFS and DFS comparison and exit")
    # print("If you want to exit the program, type 'exit'")
    # print("If you want to see the maze, type 'maze'")

    # choose = input("Enter the your choice: ")
    
    # if choose == "BFS":
    #     bfs_2(maze, start, end, screen, (0, 0))
    # elif choose == "DFS":
    #     dfs_2(maze, start, end, screen, (0, 0))
    # elif choose == "BFS and DFS comparison":
    #     print_maze(maze_dfs)  # Debug print to see the generated maze in the console
    
    #     draw_grid(screen, maze_dfs, (0, 0))
    #     draw_grid(screen, maze_bfs, (COLS * CELL_SIZE, 0))

    #     # Create threads for DFS and BFS
    #     dfs_thread = threading.Thread(target=dfs_2, args=(maze_dfs, start, end, screen, (0, 0)))
    #     bfs_thread = threading.Thread(target=bfs_2, args=(maze_bfs, start, end, screen, (COLS * CELL_SIZE, 0)))

    #     # Start the threads
    #     dfs_thread.start()
    #     bfs_thread.start()

    #     running = True
    #     while running:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 running = False

    #         # Draw the source and destination on both mazes
    #         pygame.draw.rect(screen, SOURCE, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    #         pygame.draw.rect(screen, DESTINATION, (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
    #         pygame.draw.rect(screen, SOURCE, (COLS * CELL_SIZE + start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    #         pygame.draw.rect(screen, DESTINATION, (COLS * CELL_SIZE + end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    #         pygame.display.flip()
    #         clock.tick(80)  # Adjust speed of the moving object

    # pygame.quit()
        

if __name__ == "__main__":
    game_loop()
