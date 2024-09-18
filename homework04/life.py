import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, size: tp.Tuple[int, int], randomize: bool = True, max_generations: tp.Optional[float] = float("inf")) -> None:
        self.rows, self.cols = size
        self.prev_generation = self.create_grid()
        self.curr_generation = self.create_grid(randomize=randomize)
        self.max_generations = max_generations
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        else:
            return [[0 for _ in range(self.cols)] for _ in range(self.rows)]


    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Получить соседей для данной клетки.
        """
        x, y = cell
        neighbours = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.rows and 0 <= ny < self.cols:
                    neighbours.append(self.curr_generation[nx][ny])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        """
        next_gen = [[0] * self.cols for _ in range(self.rows)]
        for x in range(self.rows):
            for y in range(self.cols):
                alive_neighbors = sum(self.get_neighbours((x, y)))
                if self.curr_generation[x][y] == 1:
                    next_gen[x][y] = 1 if alive_neighbors in (2, 3) else 0
                else:
                    next_gen[x][y] = 1 if alive_neighbors == 3 else 0
        return next_gen

    def step(self) -> None:
    """
    Выполнить один шаг игры.
    """
    if not self.is_max_generations_exceeded:
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

@property
def is_max_generations_exceeded(self) -> bool:
    """
    Не превысило ли текущее число поколений максимально допустимое.
    """
    return self.generations > self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, 'r') as file:
            lines = file.readlines()
        grid = [list(map(int, line.strip().split())) for line in lines]
        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0
        game = GameOfLife(size=(rows, cols), randomize=False)
        game.curr_generation = grid
        game.prev_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, 'w') as file:
            for row in self.curr_generation:
                file.write(' '.join(map(str, row)) + '\n')
