from pydantic import UUID4, Field, model_validator

from src.exceptions import WrongMinesCountError
from src.schemes.base import SBase, MAX_HEIGHT, MAX_WIDTH


class NewGameRequest(SBase):
    height: int = Field(ge=2, le=MAX_HEIGHT, example=10)
    width: int = Field(ge=2, le=MAX_WIDTH, example=10)
    mines_count: int = Field(ge=1, lt=MAX_HEIGHT * MAX_WIDTH, example=10)

    @model_validator(mode="after")
    def check_mines_count(self):
        if self.mines_count >= self.height * self.width:
            raise WrongMinesCountError()

        return self


class GameTurnRequest(SBase):
    game_id: UUID4 = Field(example="550e8400-e29b-41d4-a716-446655440000")
    row: int = Field(ge=0, lt=MAX_HEIGHT, example=0)
    col: int = Field(ge=0, lt=MAX_WIDTH, example=1)
