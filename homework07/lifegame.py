import pygame
import random
from pygame.locals import *


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
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

        # Создаем сетку
        self.grid = self.create_grid(randomize=True)

        # Статус игры (на паузе или нет)
        self.paused = False

    def create_grid(self, randomize: bool = False) -> list:
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
        out : list
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid = []
        for i in range(self.cell_height):
            row = []
            for j in range(self.cell_width):
                if randomize:
                    row.append(random.randint(0, 1))  # Равновероятно 0 или 1
                else:
                    row.append(0)  # Все клетки мертвые
            grid.append(row)
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка клеток на экране.
        Живые клетки - зеленые, мертвые - белые.
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                color = pygame.Color('green') if self.grid[i][j] == 1 else pygame.Color('white')
                pygame.draw.rect(self.screen, color,
                                 (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))

    def draw_lines(self) -> None:
        """
        Отрисовка сетки на экране.
        """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def get_cell(self, mouse_pos: tuple) -> tuple:
        """
        Возвращает координаты клетки по позиции мыши.

        Parameters
        ----------
        mouse_pos : tuple
            Позиция мыши (x, y)

        Returns
        ----------
        out : tuple
            Координаты клетки в сетке (row, col)
        """
        x, y = mouse_pos
        return y // self.cell_size, x // self.cell_size

    def toggle_cell(self, row: int, col: int) -> None:
        """
        Переключение состояния клетки (живая/мертвая).

        Parameters
        ----------
        row : int
            Строка клетки в сетке.
        col : int
            Столбец клетки в сетке.
        """
        self.grid[row][col] = 1 if self.grid[row][col] == 0 else 0

    def update_grid(self) -> None:
        """
        Обновление состояния клеток по правилам игры "Жизнь".
        """
        new_grid = [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                # Количество живых соседей
                neighbors = sum([self.grid[i + di][j + dj] for di in [-1, 0, 1] for dj in [-1, 0, 1]
                                 if (di != 0 or dj != 0) and 0 <= i + di < self.cell_height and 0 <= j + dj < self.cell_width])

                # Правила игры "Жизнь"
                if self.grid[i][j] == 1:  # Если клетка жива
                    if neighbors == 2 or neighbors == 3:
                        new_grid[i][j] = 1  # Остается живой
                    else:
                        new_grid[i][j] = 0  # Умирает
                else:  # Если клетка мертва
                    if neighbors == 3:
                        new_grid[i][j] = 1  # Воскресает
        self.grid = new_grid

    def run(self) -> None:
        """
        Основной цикл игры.
        """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:  # Пауза при нажатии пробела
                        self.paused = not self.paused
                elif event.type == MOUSEBUTTONDOWN:  # Обработка кликов мыши
                    if event.button == 1:  # Левая кнопка мыши
                        row, col = self.get_cell(pygame.mouse.get_pos())
                        self.toggle_cell(row, col)

            self.screen.fill(pygame.Color('white'))
            self.draw_grid()
            self.draw_lines()

            if not self.paused:
                self.update_grid()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
