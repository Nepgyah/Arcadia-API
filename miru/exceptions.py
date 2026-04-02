from rest_framework.exceptions import APIException

class MiruError(APIException):
    status_code = 400
    detail = 'An internal error occured.'
    default_code = 'internal_error'

    def __init__(self, detail=None, code=None):
        if detail:
            self.detail = detail
        if code:
            self.code = code
        super().__init__(self.detail, self.code)

class AnimeNotFoundError(MiruError):
    status_code = 404

    def __init__(self, anime_id: int):
        super().__init__(
            detail=f'Anime with ID: {anime_id} not found.',
            code='anime_not_found'
        )