from enum import StrEnum
from typing import Literal

from pydantic import UUID4, Field, model_validator

from src.exceptions import WrongMinesCountError
from src.schemes.base import SBase, MAX_HEIGHT, MAX_WIDTH


class CellStatus(StrEnum):
    EMPTY = " "
    MINE = "M"
    EXPLODED_MINE = "X"


Cell = CellStatus | Literal["0", "1", "2", "3", "4", "5", "6", "7", "8"]


class GameInfoResponse(SBase):
    game_id: UUID4 = Field(example="550e8400-e29b-41d4-a716-446655440000")
    height: int = Field(ge=2, le=MAX_HEIGHT, example=10)
    width: int = Field(ge=2, le=MAX_WIDTH, example=10)
    mines_count: int = Field(ge=1, lt=MAX_HEIGHT * MAX_WIDTH, example=10)
    completed: bool = False
    field: list[list[Cell]]

    @model_validator(mode="after")
    def check_mines_count(self):
        if self.mines_count >= self.height * self.width:
            raise WrongMinesCountError()

        return self


class ErrorResponse(SBase):
    error: str = "Произошла непредвиденная ошибка"
