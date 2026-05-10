import pytest
import psycopg2
from asobu.models import Review
from asobu.repository import AsobuRepository
from asobu.exceptions import GameNotFoundError, AsobuError, AsobuNotFound
from asobu.conftest import create_video_game_characters

@pytest.mark.django_db(transaction=True)
class TestAsobuRepository:

    # GAME
    @staticmethod
    def test_getGameByID_existingGame_returnGame(game_fixture):
        game = AsobuRepository.game.get_game(game_fixture.id)
        assert game.id == game_fixture.id

    @staticmethod
    def test_getGameByID_nonExistentGame_raisesGameNotFoundError():
        non_existent_id = 9999

        with pytest.raises(GameNotFoundError) as exception:
            AsobuRepository.game.get_game(non_existent_id)

        assert exception.value.status_code == 404
        assert str(non_existent_id) in str(exception.value.detail)

    #DLC
    @staticmethod
    def test_getDLCByGameID_existingGame_returnsDLCList(game_dlc_fixture):
        dlcs = AsobuRepository.game.get_dlc(game_dlc_fixture.game.id)
        assert len(dlcs) != 0
    
    @staticmethod
    def test_getDLCByGameID_nonExistentGame_returnsEmptyList():
        dlcs = AsobuRepository.game.get_dlc(-1)
        assert len(dlcs) == 0

    # Characters
    @staticmethod
    def test_getCharactersByGame_existingCharacters_returnsCharacterList(game_fixture):
        create_video_game_characters(game_fixture)
        result = AsobuRepository.game.get_characters(game_fixture.id)
        assert result[0].game.id == game_fixture.id

    @staticmethod
    def test_getCharactersByGame_nonExistingGame_returnsEmptyList(game_fixture):
        result = AsobuRepository.game.get_characters(game_fixture.id)
        assert len(result) == 0

    # Gamelist Entry
    @staticmethod
    def test_createGameListEntry_newEntry_returnsEntryObject(arcadia_user_fixture, game_fixture):
        details = {
            'score': 10,
            'note': 'Umazing',
            'review': 'If you get boxed, you get boxed',
            'start_play_date': '2024-4-20'
        }

        entry = AsobuRepository.list_entry.create_entry(arcadia_user_fixture, game_fixture, 10, **details)
        assert entry.user == arcadia_user_fixture
        assert entry.game == game_fixture
        assert entry.score == 10
        assert entry.note == 'Umazing'

    @staticmethod
    def test_createGameListEntry_alreadyExists_raisesError(arcadia_user_fixture, game_list_entry_fixture):
        with pytest.raises(AsobuError) as exception:
            AsobuRepository.list_entry.create_entry(
                user=arcadia_user_fixture,
                game=game_list_entry_fixture.game,
                status=10
            )

        assert exception.value.status_code == 400
        assert exception.value.default_code == AsobuError.default_code

    # Review
    @staticmethod
    def test_getGameReview_validReview_returnsReview(game_review_fixture):
        review = AsobuRepository.review.get_review(game_review_fixture.id)
        assert review.id == game_review_fixture.id

    @staticmethod
    def test_getGameReview_invalidID_returnsNone():
        review = AsobuRepository.review.get_review(0)
        assert review is None
        
    @staticmethod
    def test_getUserGameReview_validID_returnsReview(game_review_fixture):
        review = AsobuRepository.review.get_review_by_user(game_review_fixture.user.id, game_review_fixture.game.id)
        assert review == game_review_fixture

    @staticmethod
    def test_createGameReview_validInput_returnsNewReview(arcadia_user_fixture, game_fixture):
        review_text = 'Umazing'
        review = AsobuRepository.review.create_review(arcadia_user_fixture.id, game_fixture.id, review_text)
        assert isinstance(review, Review) is True

    @staticmethod
    def test_createGameReview_invalidGameID_raiseAsobuError(arcadia_user_fixture):
        review_text = 'Umazing'
        with pytest.raises(AsobuError) as exception:
            AsobuRepository.review.create_review(arcadia_user_fixture.id, 99999, review_text)

        assert exception.value.status_code == 400

    @staticmethod
    def test_updateGameReview_validInput_returnsUpdatedReview(game_review_fixture):
        new_text = 'Tazuna is a uma but i cant prove it'
        updated_review = AsobuRepository.review.update_review(
            game_review_fixture.user.id,
            game_review_fixture.game.id,
            new_text
        )
        
        assert updated_review.text == new_text

    @staticmethod
    def test_updateGameReview_reviewNotFound_raisesAsobuNotFoundError(game_review_fixture):
        new_text = 'Random text go'
        with pytest.raises(AsobuNotFound) as exception:
            AsobuRepository.review.update_review(
                game_review_fixture.user.id,
                999,
                new_text
            )

        assert exception.value.status_code == 404

    @staticmethod
    def test_updateGameReview_invalidText_raisesAsobuError(game_review_fixture):
        with pytest.raises(AsobuError) as exception:
            AsobuRepository.review.update_review(
                game_review_fixture.user.id,
                game_review_fixture.game.id,
                None
            )

        assert exception.value.status_code == 400

    @staticmethod
    def test_deleteGameReivew_validInput_deletesReview(game_review_fixture):
        AsobuRepository.review.delete_review(
            game_review_fixture.user.id,
            game_review_fixture.game.id
        )

        review = AsobuRepository.review.get_review(game_review_fixture.id)
        assert review is None

    @staticmethod
    def test_deleteGameReview_invalidInput_raisesAsobuNotFound(game_review_fixture):
        with pytest.raises(AsobuNotFound) as exception:
            AsobuRepository.review.delete_review(
                game_review_fixture.user.id,
                -1
            )

        assert exception.value.status_code == 404