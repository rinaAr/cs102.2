import typing as tp
import pathlib
import random

T = tp.TypeVar("T")

def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    return [values[i:i + n] for i in range(0, len(values), n)]

def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid

def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)

def display(grid: tp.List[tp.List[str]]) -> None:
    for row in range(len(grid)):
        if row in (3, 6):
            print("-" * 21)
        for col in range(len(grid[row])):
            if col in (3, 6):
                print("|", end=" ")
            print(grid[row][col], end=" ")
        print()

def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]

def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return [grid[row][pos[1]] for row in range(len(grid))]

def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    block_row = pos[0] // 3 * 3
    block_col = pos[1] // 3 * 3
    return [grid[r][c] for r in range(block_row, block_row + 3) for c in range(block_col, block_col + 3)]

def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '.':
                return row, col
    return None

def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    values = set("123456789")
    values -= set(get_row(grid, pos))
    values -= set(get_col(grid, pos))
    values -= set(get_block(grid, pos))
    return values

def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    pos = find_empty_positions(grid)
    if not pos:
        return grid
    row, col = pos
    for value in find_possible_values(grid, pos):
        grid[row][col] = value
        if solve(grid):
            return grid
        grid[row][col] = '.'
    return None

def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    for row in range(len(solution)):
        if set(solution[row]) != set("123456789"):
            return False
    for col in range(len(solution)):
        if set(get_col(solution, (0, col))) != set("123456789"):
            return False
    for block_row in range(0, 9, 3):
        for block_col in range(0, 9, 3):
            if set(get_block(solution, (block_row, block_col))) != set("123456789"):
                return False
    return True

def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    grid = [['.'] * 9 for _ in range(9)]
    solve(grid)
    filled_positions = [(r, c) for r in range(9) for c in range(9)]
    for _ in range(81 - N):
        pos = random.choice(filled_positions)
        filled_positions.remove(pos)
        grid[pos[0]][pos[1]] = '.'
    return grid

if __name__ == "__main__":
    for filename in ("puzzle1.txt", "puzzle2.txt", "puzzle3.txt"):
        grid = read_sudoku(filename)
        display(grid)
        solution = solve(grid)
        if solution:
            display(solution)
            assert check_solution(solution)
        else:
            print("No solution found")
