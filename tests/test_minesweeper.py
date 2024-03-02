import pytest

from src.schemes.responses import CellStatus, Cell
from src.services.minesweeper import Minesweeper, GameStatus


@pytest.mark.parametrize(
    "width, height, mines_count",
    [(5, 5, 5), (10, 10, 20), (15, 15, 30), (10, 15, 20), (15, 10, 30)],
)
def test_minesweeper_init(width: int, height: int, mines_count: int):
    game = Minesweeper(width, height, mines_count=mines_count)

    assert game.width == width
    assert game.height == height
    assert game.mines_count == mines_count
    assert len(game.mines) == mines_count
    assert not game.completed
    assert all(
        game.field[y][x] == CellStatus.EMPTY
        for y in range(height)
        for x in range(width)
    )


@pytest.mark.parametrize(
    "x, y",
    [
        (0, 0),
        (4, 0),
        (0, 9),
        (4, 9),
    ],
)
def test_minesweeper_in_bounds(x: int, y: int):
    game = Minesweeper(5, 10, mines_count=5)

    assert game.in_bounds(x, y)


@pytest.mark.parametrize(
    "x, y",
    [
        (0, -1),
        (-1, 0),
        (-1, -1),
        (5, 0),
        (5, 9),
        (5, 5),
        (0, 10),
        (4, 10),
        (10, 10),
    ],
)
def test_minesweeper_in_bounds_negative(x: int, y: int):
    game = Minesweeper(5, 10, mines_count=5)

    assert not game.in_bounds(x, y)


@pytest.mark.parametrize(
    "w, h, mines, x, y, expected",
    [
        # Угловая ячейка с двумя минами вокруг на поле 5x5
        (
            5,
            5,
            {(0, 0), (0, 1), (1, 0)},
            0,
            0,
            2,
        ),
        # Ячейка с тремя минами вокруг на поле 5x5
        (
            5,
            5,
            {(0, 0), (0, 1), (1, 0)},
            1,
            1,
            3,
        ),
        # Угловая ячейка без мин вокруг на поле 5x10
        (5, 5, {(0, 0), (0, 1), (1, 0)}, 2, 2, 0),
        (
            5,
            10,
            {(0, 0), (0, 1), (1, 0), (4, 9)},
            4,
            9,
            0,
        ),
        # Угловая ячейка с двумя минами вокруг на поле 5x10
        (
            5,
            10,
            {(0, 0), (0, 1), (1, 0), (4, 9)},
            0,
            0,
            2,
        ),
    ],
)
def test_count_mines_around(
    w: int, h: int, mines: set[tuple[int, int]], x: int, y: int, expected: int
):
    game = Minesweeper(w, h, mines=mines)

    assert game.count_mines_around(x, y) == expected


@pytest.mark.parametrize(
    "move, expected_status, expected_field",
    [
        # Тест на продолжение игры: открываем безопасную ячейку
        (
            (1, 1),
            GameStatus.CONTINUE,
            [
                [CellStatus.EMPTY, CellStatus.EMPTY, CellStatus.EMPTY],
                [CellStatus.EMPTY, "1", CellStatus.EMPTY],
                [CellStatus.EMPTY, CellStatus.EMPTY, CellStatus.EMPTY],
            ],
        ),
        # Тест на победу: открываем все безопасные ячейки
        (
            (2, 2),
            GameStatus.WIN,
            [
                [CellStatus.MINE, "1", "0"],
                ["1", "1", "0"],
                ["0", "0", "0"],
            ],
        ),
        # Тест на проигрыш: открываем ячейку с миной
        (
            (0, 0),
            GameStatus.LOSE,
            [
                [CellStatus.EXPLODED_MINE, "1", "0"],
                ["1", "1", "0"],
                ["0", "0", "0"],
            ],
        ),
    ],
)
def test_make_move(
    move: tuple[int, int],
    expected_status: GameStatus,
    expected_field: list[list[Cell]],
):
    game = Minesweeper(3, 3, mines={(0, 0)})
    status = game.make_move(*move)

    assert status == expected_status
    assert game.field == expected_field
