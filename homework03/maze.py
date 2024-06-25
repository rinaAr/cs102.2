from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], current: Tuple[int, int], direction: Tuple[int, int]):
    x, y = current
    dx, dy = direction
    grid[x + dx][y + dy] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    grid = create_grid(rows, cols)
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
                grid = remove_wall(grid, (x, y), direction)

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
                if i > 0 and grid[i - 1][j] == " ":
                    new_grid[i - 1][j] = k + 1
                if j > 0 and grid[i][j - 1] == " ":
                    new_grid[i][j - 1] = k + 1
                if i < len(grid) - 1 and grid[i + 1][j] == " ":
                    new_grid[i + 1][j] = k + 1
                if j < len(grid[i]) - 1 and grid[i][j + 1] == " ":
                    new_grid[i][j + 1] = k + 1
    return new_grid


def shortest_path(
    grid: List[List[Union[str, int]]], start_coord: Tuple[int, int], end_coord: Tuple[int, int]
) -> Optional[List[Tuple[int, int]]]:
    x_start, y_start = start_coord
    x_end, y_end = end_coord
    grid[x_start][y_start] = 0

    k = 0
    while grid[x_end][y_end] == " ":
        new_grid = make_step(grid, k)
        if new_grid == grid:
            return None
        grid = new_grid
        k += 1

    path = [(x_end, y_end)]
    while k > 0:
        x, y = path[-1]
        if x > 0 and grid[x - 1][y] == k - 1:
            path.append((x - 1, y))
        elif y > 0 and grid[x][y - 1] == k - 1:
            path.append((x, y - 1))
        elif x < len(grid) - 1 and grid[x + 1][y] == k - 1:
            path.append((x + 1, y))
        elif y < len(grid[x]) - 1 and grid[x][y + 1] == k - 1:
            path.append((x, y + 1))
        k -= 1

    return path[::-1]


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    x, y = coord
    return (
        (x == 0 or grid[x - 1][y] != " ")
        and (y == 0 or grid[x][y - 1] != " ")
        and (x == len(grid) - 1 or grid[x + 1][y] != " ")
        and (y == len(grid[0]) - 1 or grid[x][y + 1] != " ")
    )


def solve_maze(
    grid: List[List[Union[str, int]]]
) -> Tuple[List[List[Union[str, int]]], Optional[List[Tuple[int, int]]]]:
    exits = get_exits(grid)
    if len(exits) < 2 or encircled_exit(grid, exits[1]):
        return grid, None
    path = shortest_path(deepcopy(grid), exits[0], exits[1])
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[List[Tuple[int, int]]]
) -> List[List[Union[str, int]]]:
    if path:
        for i, j in path:
            if grid[i][j] != "X":
                grid[i][j] = "."
    return grid


if __name__ == "__main__":
    maze = bin_tree_maze(15, 15)
    print(pd.DataFrame(maze))
    _, path = solve_maze(maze)
    maze_with_path = add_path_to_grid(maze, path)
    print(pd.DataFrame(maze_with_path))
