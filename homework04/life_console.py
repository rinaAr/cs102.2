import curses
from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        h, w = screen.getmaxyx()
        # Отрисовать верхнюю и нижнюю границы
        screen.addch(0, 0, '+')
        screen.addch(0, w - 1, '+')
        screen.addch(h - 1, 0, '+')
        screen.addch(h - 1, w - 1, '+')
        for x in range(1, w - 1):
            screen.addch(0, x, '-')
            screen.addch(h - 1, x, '-')
        for y in range(1, h - 1):
            screen.addch(y, 0, '|')
            screen.addch(y, w - 1, '|')

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        h, w = screen.getmaxyx()
        grid_height = self.life.rows
        grid_width = self.life.cols
        cell_height = h // grid_height
        cell_width = w // grid_width

        for i in range(grid_height):
            for j in range(grid_width):
                ch = ' ' if self.life.curr_generation[i][j] == 0 else '*'
                screen.addch(i * cell_height + 1, j * cell_width + 1, ch)

    def run(self) -> None:
        """ Запуск игрового процесса и отрисовка состояния. """
        curses.curs_set(0)  # Скрыть курсор
        screen = curses.initscr()
        curses.noecho()  # Не отображать вводимые символы
        curses.cbreak()  # Входные данные обрабатываются сразу
        screen.nodelay(1)  # Не блокировать ввод

        try:
            while not self.life.is_max_generations_exceeded and self.life.is_changing:
                screen.clear()
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.refresh()

                ch = screen.getch()
                if ch == ord('q'):  # Нажатие 'q' для выхода
                    break
                elif ch == ord(' '):  # Нажатие пробела для перехода к следующему поколению
                    self.life.step()

                curses.napms(100)  # Задержка между обновлениями экрана

        finally:
            curses.endwin()  # Завершить работу с curses
