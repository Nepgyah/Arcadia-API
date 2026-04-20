import pytest
from asobu.repository import AsobuRepository
from asobu.exceptions import GameNotFoundError, AsobuError
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

    @staticmethod
    def test_createGameListEntry_newEntry_returnsEntryObject(arcadia_user_fixture, game_fixture):
        details = {
            'score': 10,
            'note': 'Umazing',
            'review': 'If you get boxed, you get boxed',
            'start_play_date': '2024-4-20'
        }

        entry = AsobuRepository.create_game_list_entry(arcadia_user_fixture, game_fixture, 10, **details)
        assert entry.user == arcadia_user_fixture
        assert entry.game == game_fixture
        assert entry.score == 10
        assert entry.note == 'Umazing'

    @staticmethod
    def test_createGameListEntry_alreadyExists_raisesError(arcadia_user_fixture, game_list_entry_fixture):
        with pytest.raises(AsobuError) as exception:
            entry = AsobuRepository.create_game_list_entry(
                user=arcadia_user_fixture,
                game=game_list_entry_fixture.game,
                status=10
            )

        assert exception.value.status_code == 400
        assert exception.value.default_code == AsobuError.default_code

        