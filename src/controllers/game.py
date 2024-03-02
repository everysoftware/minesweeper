from fastapi import APIRouter, Depends

from src.dependencies import game_service
from src.schemes import NewGameRequest, GameInfoResponse, GameTurnRequest
from src.services import GameService

router = APIRouter()


@router.post("/new", response_model=GameInfoResponse)
async def new_game(
    new_game_request: NewGameRequest, service: GameService = Depends(game_service)
):
    return service.new_game(new_game_request)


@router.post("/turn", response_model=GameInfoResponse)
async def turn(
    turn_request: GameTurnRequest, service: GameService = Depends(game_service)
):
    return service.turn(turn_request)
