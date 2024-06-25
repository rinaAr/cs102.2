from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    x, y = coord
    grid[x][y] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for x, y in empty_cells:
        directions = []
        if x > 1:
            directions.append((-2, 0))
        if y > 1:
            directions.append((0, -2))
        if directions:
            dx, dy = choice(directions)
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                grid[(x + nx) // 2][(y + ny) // 2] = " "

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, 1
        x_out, y_out = rows - 1, cols - 2

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    exits = []
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == "X":
                exits.append((x, y))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    new_grid = deepcopy(grid)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == k:
                if i > 0 and grid[i-1][j] == " ":
                    new_grid[i-1][j] = k + 1
                if j > 0 and grid[i][j-1] == " ":
                    new_grid[i][j-1] = k + 1
                if i < len(grid) - 1 and grid[i+1][j] == " ":
                    new_grid[i+1][j] = k + 1
                if j < len(grid[i]) - 1 and grid[i][j+1] == " ":
                    new_grid[i][j+1] = k + 1
    return new_grid


def shortest_path(grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    x, y = exit_coord
    k = 0
    grid[x][y] = k

    while True:
        new_grid = make_step(grid, k)
        if new_grid == grid:
            break
        grid = new_grid
        k += 1

    path = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "X":
                path.append((i, j))

    if not path:
        return None

    path = [exit_coord]
    while k > 0:
        x, y = path[-1]
        if x > 0 and grid[x-1][y] == k - 1:
            path.append((x-1, y))
        elif y > 0 and grid[x][y-1] == k - 1:
            path.append((x, y-1))
        elif x < len(grid) - 1 and grid[x+1][y] == k - 1:
            path.append((x+1, y))
        elif y < len(grid[x]) - 1 and grid[x][y+1] == k - 1:
            path.append((x, y+1))
        k -= 1

    return path[::-1]


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    x, y = coord
    return (
        (x == 0 or grid[x-1][y] != " ") and
        (y == 0 or grid[x][y-1] != " ") and
        (x == len(grid) - 1 or grid[x+1][y] != " ") and
        (y == len(grid[0]) - 1 or grid[x][y+1] != " ")
    )


def solve_maze(grid: List[List[Union[str, int]]]) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    exits = get_exits(grid)
    if not exits or encircled_exit(grid, exits[1]):
        return grid, None
    path = shortest_path(deepcopy(grid), exits[1])
    return grid, path


def add_path_to_grid(grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]) -> List[List[Union[str, int]]]:
    if path:
        for (i, j) in path:
            if grid[i][j] != "X":
                grid[i][j] = "."
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
