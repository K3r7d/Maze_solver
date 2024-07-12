# Maze Solver - DFS and BFS
This project is a visualization of maze generation and solving algorithms using Depth-First Search (DFS) and Breadth-First Search (BFS). The maze is generated using either the DFS or BFS algorithm, and then both algorithms are used to find a path from the start to the end of the maze.

# Features
Maze Generation: Generates a random maze using either DFS or BFS algorithm.
Maze Solving: Visualizes the process of solving the maze using both DFS and BFS algorithms.
Pygame Visualization: Uses Pygame to draw the maze and animate the solving process.
Threading: Utilizes Python threading to run both algorithms simultaneously for comparison.
Prerequisites
Python 3.x
Pygame
Installation
Clone the repository:

```
git clone https://github.com/yourusername/maze-solver.git
cd maze-solver
```
Install Pygame
```
pip install pygame
```
Usage
Run the script:

python maze_solver.py
Choose the algorithm for maze generation:

The maze generation uses the DFS algorithm by default. You can also choose the BFS algorithm.

Visualize the maze solving process:

The script will visualize the solving process of the maze using both DFS and BFS algorithms simultaneously.

Code Overview
generate_maze
Generates a maze using either DFS or BFS algorithm. The maze is represented as a 2D list where 1 represents a wall and 0 represents a path.

draw_grid
Draws the maze on the Pygame screen.

dfs_2
Solves the maze using the DFS algorithm. It visualizes the pathfinding process by coloring the path.

bfs_2
Solves the maze using the BFS algorithm. It visualizes the pathfinding process by coloring the path.

game_loop
Main loop of the game that initializes Pygame, generates the maze, and runs the solving algorithms in separate threads for simultaneous visualization.

Customization
Maze Dimensions: You can change the ROWS, COLS, and CELL_SIZE variables to customize the size of the maze.
Algorithm Selection: You can modify the algorithm parameter in generate_maze to choose between DFS and BFS for maze generation.
Visualization Speed: Adjust the time.sleep() values in dfs_2 and bfs_2 functions to change the speed of the visualization.
Contributing
Contributions are welcome! Please create a pull request or open an issue to discuss your ideas.

License
This project is licensed under the MIT License. See the LICENSE file for details.






