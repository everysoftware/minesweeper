from uuid import uuid4

from src.exceptions import GameNotFoundError, GameCompletedError
from src.schemes import NewGameRequest, GameInfoResponse, GameTurnRequest
from src.services.minesweeper import Minesweeper


class GameService:
    games: dict[str, Minesweeper] = {}

    def new_game(self, new_game_request: NewGameRequest) -> GameInfoResponse:
        game = Minesweeper(
            new_game_request.width,
            new_game_request.height,
            mines_count=new_game_request.mines_count,
        )
        game_id = str(uuid4())
        self.games[game_id] = game

        return GameInfoResponse(
            game_id=game_id,
            height=new_game_request.height,
            width=new_game_request.width,
            mines_count=new_game_request.mines_count,
            field=game.field,
        )

    def turn(self, game_turn_request: GameTurnRequest) -> GameInfoResponse:
        game_id = str(game_turn_request.game_id)

        if game_id not in self.games:
            raise GameNotFoundError()

        game = self.games[game_id]

        if game.completed:
            raise GameCompletedError()

        game.make_move(game_turn_request.col, game_turn_request.row)

        return GameInfoResponse(
            game_id=game_turn_request.game_id,
            height=game.height,
            width=game.width,
            mines_count=game.mines_count,
            field=game.field,
            completed=game.completed,
        )
