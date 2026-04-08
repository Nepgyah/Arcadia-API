from main.exceptions import ArcadiaException

class MiruError(ArcadiaException):
    status_code = 400
    default_detail = 'An internal error occured within the Miru service.'
    default_code = 'miru_error'

class AnimeNotFoundError(MiruError):
    status_code = 404
    default_code = 'miru_anime_not_found'

    def __init__(self, anime_id: int):
        self.detail = f'Anime with ID: {anime_id} not found.'
        super().__init__(detail=self.detail)

class AnimeAndUserAlreadyCreatedError(MiruError):
    status_code = 400
    default_code = 'anime_user_already_created'

    def __init__(self, anime_id: int, user_id: int):
        self.detail = f'Anime ID: {anime_id} with User ID: {user_id} already exists'
        super().__init__(detail=self.detail)