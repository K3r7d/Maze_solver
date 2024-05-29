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

def generate_maze(rows, cols):
    # Sample maze
    maze = [[0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
            [0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1],
            [0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1],
            [1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1],
            [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
            [0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1],
            [0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,1],
            [1,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1],
            [0,0,0,1,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,1],
            [0,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1],
            [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,1],
            [0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1],
            [0,1,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1],
            [0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1],
            [0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1],
            [0,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1],
            [0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
            [0,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1],
            [0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
            [0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1],
            [0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1],
            [0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1],
            [0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
            [0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1],
            [0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,1],
            [0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1],
            [0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
            [0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1],
            [0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,1],
            [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1],
            [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1],
            [0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1],
            [0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1],
            [1,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1],
            [0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,1],
            [0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1],
            [0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1],
            [0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1],
            [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1],
            [1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,1,1,0,1],
            [0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,1],
            [0,1,1,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1],
            [0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,0,0,1],
            [0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1],
            [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,1],
            [0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1],
            [0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1],
            [1,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,1],
            [1,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1],
            [0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1],
            [0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1],
            [0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
            [1,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1],
            [0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
            [0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            ]



    ########################################################   
    #dfs
    # maze = [[1 for _ in range(cols)] for _ in range(rows)]
    # stack = [(0, 0)]
    # maze[0][0] = 0

    # while stack:
    #     current = stack[-1]
    #     row, col = current
    #     directions = random.sample(DIRECTIONS, len(DIRECTIONS))
    #     moved = False

    #     for dr, dc in directions:
    #         new_row, new_col = row + 2 * dr, col + 2 * dc

    #         if 0 <= new_row < rows and 0 <= new_col < cols and maze[new_row][new_col] == 1:
    #             maze[row + dr][col + dc] = 0
    #             maze[new_row][new_col] = 0
    #             stack.append((new_row, new_col))
    #             moved = True
    #             break

    #     if not moved:
    #         stack.pop()

    ########################################################

    #bfs
    # maze = [[1 for _ in range(cols)] for _ in range(rows)]
    # queue = [(random.randint(0, rows - 1) // 2 * 2, random.randint(0, cols - 1) // 2 * 2)]
    # maze[queue[0][0]][queue[0][1]] = 0

    # while queue:
    #     current = queue.pop(0)
    #     row, col = current
    #     directions = random.sample(DIRECTIONS, len(DIRECTIONS))

    #     for dr, dc in directions:
    #         new_row, new_col = row + 2 * dr, col + 2 * dc

    #         if 0 <= new_row < rows and 0 <= new_col < cols and maze[new_row][new_col] == 1:
    #             if random.random() < 0.75:  # Introduce a bias to create dead ends
    #                 maze[row + dr][col + dc] = 0
    #                 maze[new_row][new_col] = 0
    #                 queue.append((new_row, new_col))
    #             else:
    #                 maze[row + dr][col + dc] = 0
    
    ########################################################

    return maze

def draw_grid(screen, maze, offset):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if maze[row][col] == 0 else BLACK
            pygame.draw.rect(screen, color, (offset[0] + col * CELL_SIZE, offset[1] + row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def dfs_2(maze, start, end, screen, offset):
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

def bfs_2(maze, start, end, screen, offset):
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

if __name__ == "__main__":
    game_loop()
