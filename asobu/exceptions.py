from main.exceptions import ArcadiaException

class AsobuError(ArcadiaException):
    status_code = 400
    default_detail = 'An internal error occured within the Asobu service.'
    default_code = 'asobu_error'

class AsobuNotFound(AsobuError):
    status_code = 404

class GameNotFoundError(AsobuError):
    status_code = 404
    default_code = 'asobu_gane_not_found_error'

    def __init__(self, game_id: int):
        if not game_id:
            self.detail = 'Game not found'
        else:
            self.detail = f'Game with id f{game_id} not found.'
        super().__init__(detail=self.detail)

