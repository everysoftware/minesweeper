import random
from enum import auto, Enum

from src.exceptions import OutOfBoundsError, AlreadyOpenedError, NoMinesProvidedError
from src.schemes.responses import Cell, CellStatus


class GameStatus(Enum):
    CONTINUE = auto()
    WIN = auto()
    LOSE = auto()


class Minesweeper:
    width: int
    height: int
    mines_count: int
    field: list[list[Cell]]
    completed: bool
    mines: set[tuple[int, int]]

    def __init__(
        self,
        width: int,
        height: int,
        *,
        mines_count: int | None = None,
        mines: set[tuple[int, int]] | None = None,
        field: list[list[Cell]] | None = None,
    ):
        if mines_count is None and mines is None:
            raise NoMinesProvidedError()

        self.width = width
        self.height = height
        self.mines_count = mines_count
        self.completed = False

        if field is None:
            self.field = [
                [CellStatus.EMPTY for _ in range(width)] for _ in range(height)
            ]
        else:
            self.field = field

        if mines is None:
            self.mines = set()

            # Закладываем мины
            while len(self.mines) < mines_count:
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)

                self.mines.add((x, y))
        else:
            self.mines = mines
            self.mines_count = len(mines)

    def in_bounds(self, x: int, y: int) -> bool:
        """Проверка, что координаты находятся в пределах поля"""
        return 0 <= x < self.width and 0 <= y < self.height

    def count_mines_around(self, x: int, y: int) -> int:
        """Подсчет количества мин вокруг клетки (x, y)"""
        count = 0

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == dy == 0:
                    continue
                if self.in_bounds(x + dx, y + dy) and (x + dx, y + dy) in self.mines:
                    count += 1

        return count

    def _make_move(self, x: int, y: int) -> GameStatus | None:
        """Рекурсия для открытия клетки (x, y)"""
        if not self.in_bounds(x, y) or self.field[y][x] != CellStatus.EMPTY:
            return

        if (x, y) in self.mines:
            self.field[y][x] = CellStatus.EXPLODED_MINE
            self.completed = True

            # Открываем все клетки
            for x in range(self.width):
                for y in range(self.height):
                    self._make_move(x, y)

            return GameStatus.LOSE

        # Считаем количество мин вокруг
        count = self.count_mines_around(x, y)
        self.field[y][x] = str(count)

        # Если вокруг клетки нет мин, открываем все соседние клетки
        if count == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == dy == 0:
                        continue
                    if self.in_bounds(x + dx, y + dy):
                        status = self._make_move(x + dx, y + dy)

                        if status in (GameStatus.LOSE, GameStatus.WIN):
                            return status

        # Если все клетки открыты, игра завершена
        empty = sum(row.count(CellStatus.EMPTY) for row in self.field)
        if not self.completed and empty == self.mines_count:
            self.completed = True

            for mine in self.mines:
                self.field[mine[1]][mine[0]] = CellStatus.MINE

            return GameStatus.WIN

        return GameStatus.CONTINUE

    def make_move(self, x: int, y: int) -> GameStatus:
        """Открытие клетки (x, y) и обработка результата игры"""
        if not self.in_bounds(x, y):
            raise OutOfBoundsError()

        if self.field[y][x] != CellStatus.EMPTY:
            raise AlreadyOpenedError()

        return self._make_move(x, y)
