import pytest
from lifegame import GameOfLife

def test_create_grid_default():
    game = GameOfLife(320, 240, 20)
    grid = game.create_grid(randomize=False)
    assert len(grid) == game.cell_height
    assert len(grid[0]) == game.cell_width
    assert all(cell == 0 for row in grid for cell in row)

def test_create_grid_random():
    game = GameOfLife(320, 240, 20)
    grid = game.create_grid(randomize=True)
    assert len(grid) == game.cell_height
    assert len(grid[0]) == game.cell_width
    assert any(cell == 1 for row in grid for cell in row)

def test_toggle_cell():
    game = GameOfLife(320, 240, 20)
    row, col = 0, 0
    assert game.grid[row][col] == 0
    game.toggle_cell(row, col)
    assert game.grid[row][col] == 1
    game.toggle_cell(row, col)
    assert game.grid[row][col] == 0
