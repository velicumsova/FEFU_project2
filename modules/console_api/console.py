import curses


class Console:
    def __init__(self, width=150, height=49):
        self.stdscr = curses.initscr()
        self.max_width = width # ширина терминала
        self.max_height = height # высота терминала

        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        # получаем высоту и ширину терманала пользователя
        current_console_height, current_console_width = self.stdscr.getmaxyx()

        if current_console_width < self.max_width:
            raise Exception(f'Ширина консоли = {current_console_width}. Меньше {self.max_width}')

        if current_console_height < self.max_height:
            raise Exception(f'Высота консоли = {current_console_height}. Меньше {self.max_height}')

    def finish_work(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def clear(self):
        # Очищает консоль
        self.stdscr.clear()

    def refresh(self):
        # Обновляет консоль, вносит все сделанные изменения
        self.stdscr.refresh()

    def napms(self, time_to_sleep=100):
        # Задержка на 100 миллисекунд
        curses.napms(time_to_sleep)

    def get_char(self):
        # Возвращает ASCII-код нажатой клавиши
        key = self.stdscr.getch()
        return key

    @staticmethod
    def clear_buffer():
        # очищает буфер клавиатуры, удаляя все нажатые, но еще не обработанные символы.
        curses.flushinp()

    def write_line(self, x: int, y: int, line: str):
        # Вывод строки в консоль
        if len(line)+x > self.max_width:
            line = line[:(self.max_width-x)]
        if len(line) == 0:
            return
        if x >= self.max_width or y >= self.max_height:
            return

        self.stdscr.addstr(y, x, line)

    def write_column(self, x: int, y: int, column: str):
        # выводит колонку
        if len(column) > self.max_height:
            column = column[:(self.max_height-y)]
        if len(column) == 0:
            return
        if x >= self.max_width or y >= self.max_height:
            return

        for i in range(len(column)):
            self.stdscr.addstr(y, x, column[i])
            y+=1

    def write_object_by_list_of_string(self, x: int, y: int, list_of_string: list):
        # выводит список со строками
        for i in range(len(list_of_string)):
            self.write_line(x, y, list_of_string[i])
            y += 1

    def write_object_by_long_string(self, x: int, y: int, big_string: str):
        # выводит длинноу строку с переносами строк
        list_of_string = big_string.split('\n')
        for i in range(len(list_of_string)):
            self.write_line(x, y, list_of_string[i])
            y += 1
    def get_long_string_size(self, big_string: str):
        # возвращает размеры большой строки
        S = big_string.split('\n')
        if len(S) == 0:
            return 0, 0
        return len(S[0]), len(S)

    def write_border(self, x: int, y: int, width: int, height: int):
        # рисует рамку
        self.write_line(x, y, f'┌{"─" * (width-2)}┐')
        self.write_line(x, y+height-1, f'└{"─" * (width-2)}┘')
        self.write_column(x, y+1, '│'*(height-2))
        self.write_column(x+width-1, y+1, '│'*(height-2))

    def del_border(self, x: int, y: int, width: int, height: int):
        # удаляет рамку
        self.write_line(x, y, width * ' ')
        self.write_line(x, y+height-1, width * ' ')
        self.write_column(x, y+1, ' '*(height-2))
        self.write_column(x+width-1, y+1, ' '*(height-2))


if __name__ == '__main__':
    console1 = Console()
    # input()
    print(console1.get_char())







