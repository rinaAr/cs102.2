from copy import deepcopy
from random import choice, randint
from typing import List, Tuple, Union
import pandas as pd

def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]

def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    grid = create_grid(rows, cols)
    
    # Place entrance and exit
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"
    
    # Generating the maze using binary tree algorithm
    for x in range(1, rows, 2):
        for y in range(1, cols, 2):
            grid[x][y] = " "
            directions = []
            if x > 1:
                directions.append((-1, 0))
            if y > 1:
                directions.append((0, -1))
            if directions:
                direction = choice(directions)
                dx, dy = direction
                grid[x + dx][y + dy] = " "
    
    return grid

def get_neighbors(grid: List[List[Union[str, int]]], cell: Tuple[int, int]) -> List[Tuple[int, int]]:
    neighbors = []
    x, y = cell
    rows, cols = len(grid), len(grid[0])
    
    # Check four possible neighbors: up, down, left, right
    if x > 0 and grid[x - 1][y] != "■":
        neighbors.append((x - 1, y))
    if x < rows - 1 and grid[x + 1][y] != "■":
        neighbors.append((x + 1, y))
    if y > 0 and grid[x][y - 1] != "■":
        neighbors.append((x, y - 1))
    if y < cols - 1 and grid[x][y + 1] != "■":
        neighbors.append((x, y + 1))
    
    return neighbors

def solve_maze(grid: List[List[Union[str, int]]]) -> Tuple[List[List[Union[str, int]]], Union[Tuple[int, int], List[Tuple[int, int]]]]:
    start = None
    end = None
    
    # Find start (entrance) and end (exit) points
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "X":
                if start is None:
                    start = (i, j)
                else:
                    end = (i, j)
    
    if not (start and end):
        return grid, None
    
    # Implementing a simplified variation of Dijkstra's algorithm
    queue = [(start, [start])]
    visited = set()
    
    while queue:
        current, path = queue.pop(0)
        
        if current == end:
            for position in path[1:-1]:
                x, y = position
                grid[x][y] = "X"
            return grid, path
        
        if current not in visited:
            visited.add(current)
            for neighbor in get_neighbors(grid, current):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    
    return grid, None

def add_path_to_grid(grid: List[List[Union[str, int]]], path: Union[Tuple[int, int], List[Tuple[int, int]]]) -> List[List[Union[str, int]]]:
    if isinstance(path, tuple):
        path = [path]
    
    for x, y in path:
        grid[x][y] = "X"
    
    return grid

def visualize_grid(grid: List[List[Union[str, int]]]) -> None:
    df = pd.DataFrame(grid)
    print(df)

if __name__ == "__main__":
    # Generate maze
    maze = bin_tree_maze(15, 15)
    
    # Print initial maze
    print("Initial maze:")
    visualize_grid(maze)
    
    # Solve maze
    solved_maze, path = solve_maze(deepcopy(maze))
    
    # Print solved maze
    if path:
        print("\nSolved maze with path:")
        maze_with_path = add_path_to_grid(solved_maze, path)
        visualize_grid(maze_with_path)
    else:
        print("\nNo path found in maze.")

