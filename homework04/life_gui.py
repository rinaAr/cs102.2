import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI

class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = life.cols * cell_size
        self.height = life.rows * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game of Life")

    def draw_lines(self) -> None:
        """ Отобразить линии сетки. """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, (200, 200, 200), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, (200, 200, 200), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """ Отобразить состояние клеток. """
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                color = (0, 255, 0) if self.life.curr_generation[i][j] == 1 else (0, 0, 0)
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                )

    def run(self) -> None:
        """ Запуск игрового процесса и отрисовка состояния. """
        clock = pygame.time.Clock()
        running = True

        while running and not self.life.is_max_generations_exceeded:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.life.step()
                    elif event.key == K_q:
                        running = False

            self.screen.fill((0, 0, 0))  # Очистить экран
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()  # Обновить экран

            clock.tick(self.speed)  # Задержка для управления частотой обновления

        pygame.quit()
