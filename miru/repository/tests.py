## Dev Note: This file is mostly curated by AI and thus not fully verified for its correctness
import pytest
from rest_framework.exceptions import ValidationError
from miru.repository import MiruRepository
from miru.models import AnimeListEntry, FavoriteAnime, CustomAnimeList
from miru.exceptions import MiruNotFoundError, MiruError, MiruValidationError

@pytest.mark.django_db
class TestAnimeModule:

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
class TestAnimeEpisodeModule:

    @staticmethod
    def test_getEpisode_validID_returnsEpisode(anime_episode_fixture):
        assert MiruRepository.episode.get_episode(anime_episode_fixture.id) == anime_episode_fixture

    @staticmethod
    def test_getEpisode_invalidID_raisesMiruNotFound():
        with pytest.raises(MiruNotFoundError):
            MiruRepository.episode.get_episode(1)
            
@pytest.mark.django_db
class TestAnimeListModule:

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
class TestFavoriteModule:

    @staticmethod
    def test_add_favorite_anime_success(arcadia_profile_fixture, anime_fixture):
        """Should successfully link an anime to a profile's favorites list."""
        MiruRepository.favorite.add_favorite_anime(
            profile_id=arcadia_profile_fixture.id, 
            anime=anime_fixture
        )

        # Verify it now exists in the database
        assert FavoriteAnime.objects.filter(
            profile_id=arcadia_profile_fixture.id, 
            anime=anime_fixture
        ).exists()

    @staticmethod
    def test_add_favorite_anime_duplicate_raises_validation_error(
        arcadia_profile_fixture, anime_fixture, favorite_anime_fixture
    ):
        """Should raise MiruValidationError if the user has already favorited this specific anime."""
        with pytest.raises(MiruValidationError) as exc_info:
            MiruRepository.favorite.add_favorite_anime(
                profile_id=arcadia_profile_fixture.id, 
                anime=anime_fixture
            )
        assert str(exc_info.value) == "You have already favorited this anime"

    # ==========================================
    # REMOVE_FAVORITE_ANIME TESTS
    # ==========================================

    @staticmethod
    def test_remove_favorite_anime_success(arcadia_profile_fixture, favorite_anime_fixture):
        """Should successfully delete the FavoriteAnime record if it exists."""
        # Ensure it exists before running the method
        assert FavoriteAnime.objects.filter(
            profile_id=favorite_anime_fixture.profile_id, 
            anime=favorite_anime_fixture.anime
        ).exists()

        MiruRepository.favorite.remove_favorite_anime(
            profile_id=favorite_anime_fixture.profile_id, 
            anime=favorite_anime_fixture.anime
        )

        # Verify it is gone
        assert not FavoriteAnime.objects.filter(
            profile_id=favorite_anime_fixture.profile_id, 
            anime=favorite_anime_fixture.anime
        ).exists()

    @staticmethod
    def test_remove_favorite_anime_not_found_raises_validation_error(
        arcadia_profile_fixture, anime_fixture
    ):
        """Should raise MiruValidationError if attempting to unfavorite an un-favorited anime."""
        with pytest.raises(MiruValidationError) as exc_info:
            MiruRepository.favorite.remove_favorite_anime(
                profile_id=arcadia_profile_fixture.id, 
                anime=anime_fixture
            )
        assert str(exc_info.value) == "Could not find anime to remove from favorites"

    # ==========================================
    # GET_FAVORITE_ANIME TESTS
    # ==========================================

    @staticmethod
    def test_get_favorite_anime_returns_list(arcadia_profile_fixture, favorite_anime_fixture):
        """Should return a QuerySet listing all favorites tied to this profile id."""
        favorites = MiruRepository.favorite.get_favorite_anime(profile_id=arcadia_profile_fixture.id)
        
        # Check that it returns a collection with our item inside
        assert len(favorites) == 1
        assert favorites[0].id == favorite_anime_fixture.id

    @staticmethod
    def test_get_favorite_anime_empty_list(arcadia_profile_fixture):
        """Should return an empty QuerySet if the user has no favorites yet."""
        favorites = MiruRepository.favorite.get_favorite_anime(profile_id=arcadia_profile_fixture.id)
        
        assert len(favorites) == 0

@pytest.mark.django_db
class TestCustomAnimeListRepository:

    # ==========================================
    # GET_CUSTOM_ANIME_LIST TESTS
    # ==========================================

    @staticmethod
    def test_get_custom_anime_list_success(arcadia_profile_fixture, custom_anime_list_fixture):
        """Should return the custom list if both list ID and profile ID match."""
        result = MiruRepository.list.get_custom_anime_list(
            profile_id=arcadia_profile_fixture.id,
            list_id=custom_anime_list_fixture.id
        )
        assert result is not None
        assert result.id == custom_anime_list_fixture.id
        assert result.title == custom_anime_list_fixture.title

    @staticmethod
    def test_get_custom_anime_list_not_found(arcadia_profile_fixture):
        """Should return None and log info if the list does not exist or profile mismatch occurs."""

        with pytest.raises(MiruNotFoundError):
            MiruRepository.list.get_custom_anime_list(
                profile_id=arcadia_profile_fixture.id,
                list_id=99999  # Non-existent ID
            )

    # ==========================================
    # CREATE TESTS
    # ==========================================

    @staticmethod
    def test_create_custom_anime_list_success(arcadia_profile_fixture):
        """Should validate data through serializer, save, and return the new list instance."""
        payload = {
            "profile_id": arcadia_profile_fixture.id,
            "title": "Shounen Hype List"
        }
        
        new_list = MiruRepository.list.create_custom_anime_list(**payload)
        
        assert isinstance(new_list, CustomAnimeList)
        assert new_list.title == "Shounen Hype List"
        assert new_list.profile_id == arcadia_profile_fixture.id

    @staticmethod
    def test_create_custom_anime_list_validation_error():
        """Should bubble up DRF ValidationError if input payloads violate serializer rules."""
        # Supplying an illegally long title or missing required data
        invalid_payload = {
            "title": "x" * 130  # Max length is 125
        }
        
        with pytest.raises(ValidationError):
            MiruRepository.list.create_custom_anime_list(**invalid_payload)

    # ==========================================
    # UPDATE TESTS
    # ==========================================

    @staticmethod
    def test_update_custom_anime_list_details_success(custom_anime_list_fixture):
        """Should seamlessly run partial updates on titles or visibility settings."""
        updated_data = {"title": "Updated Watchlist Title"}
        
        updated_list = MiruRepository.list.update_custom_anime_list_details(
            custom_anime_list_fixture, 
            **updated_data
        )
        
        assert updated_list.title == "Updated Watchlist Title"

    # ==========================================
    # DELETE TESTS
    # ==========================================

    @staticmethod
    def test_delete_custom_anime_list_success(custom_anime_list_fixture):
        """Should safely purge the target custom list record from the database."""
        list_id = custom_anime_list_fixture.id
        
        MiruRepository.list.delete_custom_anime_list(custom_anime_list_fixture)
        
        assert not CustomAnimeList.objects.filter(id=list_id).exists()

    # ==========================================
    # MANY-TO-MANY (ADD/REMOVE) TESTS
    # ==========================================

    @staticmethod
    def test_add_to_custom_anime_list(custom_anime_list_fixture, anime_fixture):
        """Should add an Anime reference to the ManyToMany relationship."""
        # Ensure it's empty to start
        assert custom_anime_list_fixture.anime.count() == 0
        
        MiruRepository.list.add_to_custom_anime_list(custom_anime_list_fixture, anime_fixture)
        
        assert custom_anime_list_fixture.anime.count() == 1
        assert custom_anime_list_fixture.anime.filter(id=anime_fixture.id).exists()

    @staticmethod
    def test_remove_from_custom_anime_list_success(custom_anime_list_fixture, anime_fixture):
        """Should remove an associated Anime reference from the ManyToMany field mapping."""
        # Pre-seed the M2M mapping
        custom_anime_list_fixture.anime.add(anime_fixture)
        assert custom_anime_list_fixture.anime.count() == 1
        
        MiruRepository.list.remove_from_custom_anime_list(custom_anime_list_fixture, anime_fixture)
        
        assert custom_anime_list_fixture.anime.count() == 0