import pytest
from miru.repository import MiruRepository
from miru.models import AnimeListEntry
from miru.exceptions import MiruNotFoundError, MiruError

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
            "score": 10,
            "note": "",
            "current_episode": 1,
            "start_watch_date": None,
            "end_watch_date": None
        }

        updated_entry = MiruRepository.list.update_entry(
            anime_list_entry_fixture,
            **data
        )

        assert updated_entry.score == 10
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

