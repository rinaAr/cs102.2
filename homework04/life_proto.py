import random
import typing as tp
import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]

class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Инициализация сетки клеток
        self.grid = self.create_grid(randomize=True)
    
    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.
        """
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        else:
            return [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующие цвета.
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                color = (0, 255, 0) if self.grid[i][j] == 1 else (0, 0, 0)
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.
        """
        x, y = cell
        neighbours = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cell_height and 0 <= ny < self.cell_width:
                    neighbours.append(self.grid[nx][ny])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        """
        next_gen = [[0] * self.cell_width for _ in range(self.cell_height)]
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                alive_neighbors = sum(self.get_neighbours((i, j)))
                if self.grid[i][j] == 1:
                    next_gen[i][j] = 1 if alive_neighbors in (2, 3) else 0
                else:
                    next_gen[i][j] = 1 if alive_neighbors == 3 else 0
        return next_gen

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.grid = self.get_next_generation()

            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
        
        pygame.quit()
