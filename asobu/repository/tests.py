import pytest
from asobu.repository import AsobuRepository
from asobu.exceptions import GameNotFoundError
from asobu.conftest import create_video_game_characters

@pytest.mark.django_db
class TestAsobuRepository:

    @staticmethod
    def test_getGameByID_existingGame_returnGame(game_fixture):
        game = AsobuRepository.get_game_by_id(game_fixture.id)
        assert game.id == game_fixture.id

    @staticmethod
    def test_getGameByID_nonExistentGame_raisesGameNotFoundError():
        non_existent_id = 9999

        with pytest.raises(GameNotFoundError) as exception:
            AsobuRepository.get_game_by_id(non_existent_id)

        assert exception.value.status_code == 404
        assert str(non_existent_id) in str(exception.value.detail)

    @staticmethod
    def test_getCharactersByGame_existingCharacters_returnsCharacterList(game_fixture):
        created_characters = create_video_game_characters(game_fixture)
        result = AsobuRepository.get_characters_by_game(game_fixture.id)
        assert result[0].game.id == game_fixture.id

    @staticmethod
    def test_getCharactersByGame_nonExistingGame_returnsEmptyList(game_fixture):
        result = AsobuRepository.get_characters_by_game(game_fixture.id)
        assert len(result) == 0