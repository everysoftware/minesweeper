from fastapi import HTTPException
from starlette import status


class WrongMinesCountError(ValueError):
    def __init__(self):
        super().__init__("Mines count should be less than height * width")
