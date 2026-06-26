import pytest
from rest_framework.exceptions import ValidationError
from main.exceptions import ArcadiaValidationError
from miru.repository import MiruRepository
from miru.models import AnimeListEntry, AnimeReview
from miru.exceptions import MiruNotFoundError, MiruError, MiruValidationError

@pytest.mark.django_db
class TestMiruAnimeRepository:

    @staticmethod
    def test_animeCount_returnsCount(anime_fixture):
        assert MiruRepository.anime.get_anime_count() == 1

    @staticmethod
    def test_getAnime_validID_returnsAnime(anime_fixture):
        assert MiruRepository.anime.get_anime(anime_fixture.id) == anime_fixture

    @staticmethod
    def test_getAnime_invalidID_raisesMiruNotFound():
        with pytest.raises(MiruNotFoundError):
            MiruRepository.anime.get_anime(9999)

    @staticmethod
    def test_doesAnimeExist_validID_returnsTrue(anime_fixture):
        assert MiruRepository.anime.does_anime_exist(anime_fixture.id) is True

    @staticmethod
    def test_doesAnimeExist_invalidID_returnsFalse():
        assert MiruRepository.anime.does_anime_exist(9999) is False

    @staticmethod
    def test_getCharacters_hasCharacters_returnsCharacterList(bocchi_character_fixture):
        characters, anime = bocchi_character_fixture
        assert len(MiruRepository.anime.get_characters(anime.id)) == len(characters)

    @staticmethod
    def test_getCharacters_noCharacters_returnsEmptyList(anime_fixture):
        assert len(MiruRepository.anime.get_characters(anime_fixture.id)) == 0

    @staticmethod
    def test_getAnilistData_validID_returnsMalData(anime_anilist_data_fixture):
        assert MiruRepository.anime.get_anilist_data(anime_anilist_data_fixture.anime.id) == anime_anilist_data_fixture

    @staticmethod
    def test_getAnilistData_invalidID_raiseMiruNotFound():
        with pytest.raises(MiruNotFoundError):
            MiruRepository.anime.get_anilist_data(9999)

    @staticmethod
    def test_getMALData_validID_returnsMalData(anime_mal_data_fixture):
        assert MiruRepository.anime.get_mal_data(anime_mal_data_fixture.anime.id) == anime_mal_data_fixture

    @staticmethod
    def test_getMALData_invalidID_raiseMiruNotFound():
        with pytest.raises(MiruNotFoundError):
            MiruRepository.anime.get_mal_data(9999)

@pytest.mark.django_db
class TestMiruEpisodeRepository:

    @staticmethod
    def test_getEpisode_validID_returnsEpisode(anime_episode_fixture):
        assert MiruRepository.episode.get_episode(anime_episode_fixture.id) == anime_episode_fixture

    @staticmethod
    def test_getEpisode_invalidID_raisesMiruNotFound():
        with pytest.raises(MiruNotFoundError):
            MiruRepository.episode.get_episode(1)
            
@pytest.mark.django_db
class TestListRepository:

    @staticmethod
    def test_createEntry_validData_returnsEntry(anime_fixture, arcadia_profile_fixture):
        data = {
            "status": 1,
            "score": 10,
            "note": "",
            "current_episode": 1,
            "start_watch_date": None,
            "end_watch_date": None
        }
        entry = MiruRepository.list.create_entry(
            profile_id=arcadia_profile_fixture.id,
            anime_id=anime_fixture.id,
            **data
        )

        assert AnimeListEntry.objects.filter(id=entry.id).exists() is True

    @staticmethod
    def test_getEntry_validID_returnsEntry(anime_list_entry_fixture):
        assert MiruRepository.list.get_entry(
            anime_list_entry_fixture.profile_id, 
            anime_list_entry_fixture.anime.id
        ) == anime_list_entry_fixture

    @staticmethod
    def test_getEntry_invalidID_raisesNotFound():
        with pytest.raises(MiruNotFoundError):
            MiruRepository.list.get_entry(1,1)

    @staticmethod
    def test_updateEntry_validData_returnsEntry(anime_list_entry_fixture):
        data = {
            "status": 1,
            "note": "",
            "current_episode": 1,
            "start_watch_date": None,
            "end_watch_date": None
        }

        updated_entry = MiruRepository.list.update_entry(
            anime_list_entry_fixture,
            **data
        )

        assert updated_entry.status == 1

    @staticmethod
    def test_deleteEntry_validEntry_deletesEntry(anime_list_entry_fixture):
        MiruRepository.list.delete_entry(anime_list_entry_fixture)

        assert AnimeListEntry.objects.filter(id=anime_list_entry_fixture.id).exists() is False

    @staticmethod
    def test_deleteEntry_errorOccurs_raisesMiruError():
        with pytest.raises(MiruError):
            MiruRepository.list.delete_entry(None)
        
    @staticmethod
    def test_getUserList_hasList_returnsList(anime_list_entry_fixture):
        assert len(MiruRepository.list.get_user_list(anime_list_entry_fixture.profile_id)) == 1

    @staticmethod
    def test_getUserList_noList_returnsEmpty():
        assert len(MiruRepository.list.get_user_list(1)) == 0

@pytest.mark.django_db
class TestAnimeReview:

    @staticmethod
    def test_get_review_success(arcadia_profile_fixture, anime_fixture, anime_review_fixture):
        """Should successfully return the review if it exists."""
        review = MiruRepository.review.get_review(
            profile_id=arcadia_profile_fixture.id, 
            anime_id=anime_fixture.id
        )
        assert review is not None
        assert review.id == anime_review_fixture.id

    @staticmethod
    def test_get_review_not_found(arcadia_profile_fixture, anime_fixture):
        """Should return None if no review matches the profile and anime."""
        review = MiruRepository.review.get_review(
            profile_id=arcadia_profile_fixture.id, 
            anime_id=anime_fixture.id
        )
        assert review is None

    @staticmethod
    def test_create_review_success(arcadia_profile_fixture, anime_fixture, anime_review_detail_fixture):
        """Should successfully create and return a review given valid data."""
        review = MiruRepository.review.create(
            profile_id=arcadia_profile_fixture.id,
            anime_id=anime_fixture.id,
            **anime_review_detail_fixture
        )
        
        assert isinstance(review, AnimeReview)
        assert review.profile_id == arcadia_profile_fixture.id
        assert review.anime_id == anime_fixture.id
        assert review.score == anime_review_detail_fixture["score"]

    @staticmethod
    def test_create_review_duplicate_raises_miru_validation_error(
        arcadia_profile_fixture, anime_fixture, anime_review_detail_fixture, anime_review_fixture
    ):
        """Should raise MiruValidationError if a unique constraint error happens on serializer level."""
        with pytest.raises(MiruValidationError) as exc_info:
            MiruRepository.review.create(
                profile_id=arcadia_profile_fixture.id,
                anime_id=anime_fixture.id,
                **anime_review_detail_fixture
            )
        assert str(exc_info.value) == "Review already exists"

    @staticmethod
    def test_update_review_success(anime_review_fixture):
        """Should patch and return the updated review model."""
        updated_data = {"score": 9.0, "text": "Actually, changing my mind. It is a 9/10."}
        
        updated_review = MiruRepository.review.update(anime_review_fixture, **updated_data)
        
        assert updated_review.score == 9.0
        assert updated_review.text == "Actually, changing my mind. It is a 9/10."

    @staticmethod
    def test_update_review_validation_error(anime_review_fixture):
        """Should propagate Django Rest Framework ValidationError if given out-of-bounds data."""
        # Score is validated out of bounds (1-10)
        invalid_data = {"score": 15.0} 
        
        with pytest.raises(ValidationError):
            MiruRepository.review.update(anime_review_fixture, **invalid_data)

    @staticmethod
    def test_delete_review_success(anime_review_fixture):
        """Should delete the review object successfully from the database."""
        review_id = anime_review_fixture.id
        MiruRepository.review.delete(anime_review_fixture)
        
        assert not AnimeReview.objects.filter(id=review_id).exists()
