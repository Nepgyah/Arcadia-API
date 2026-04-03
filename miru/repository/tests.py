import pytest
from .miru_repository import MiruRepository
from miru.models.list_entry import AnimeListEntry
from miru.models.anime import Anime
from miru.exceptions import AnimeNotFoundError
# Declares that the tests have database acccess
@pytest.mark.django_db
class TestRepository:

    def test_get_anime_by_id_returns_anime(self, anime_fixture):
        anime = MiruRepository.get_anime_by_id(anime_fixture.id)
        assert anime.slug == 'bocchi-the-rock'

    def test_get_anime_by_id_returns_none(self, anime_fixture):
        non_existent_id = 9999

        with pytest.raises(AnimeNotFoundError) as exception:
            MiruRepository.get_anime_by_id(non_existent_id)

        assert exception.value.status_code == 404
        assert str(non_existent_id) in str(exception.value.detail)

    def test_get_characters_by_anime(self, anime_fixture, bocchi_character_fixtures):
        characters = MiruRepository.get_characters_by_anime(anime_fixture.id)
        assert bocchi_character_fixtures[0] in characters

    def test_get_characters_by_anime_returns_none(self, anime_fixture, bocchi_character_fixtures):
        non_existent_id = 9999

        with pytest.raises(AnimeNotFoundError) as exception:
            MiruRepository.get_characters_by_anime(non_existent_id)

        assert exception.value.status_code == 404
        assert str(non_existent_id) in str(exception.value.detail)

    def test_create_anime_list_entry_success(self, anime_fixture, user_fixture):
        test_details = {
            'current_episode': 1,
            'score': 9,
        }
        MiruRepository.create_anime_list_entry(
            user=user_fixture,
            anime=anime_fixture,
            status=0,
            details=test_details
        )

        assert AnimeListEntry.objects.filter(
            user=user_fixture,
            anime=anime_fixture,
            status=0
        ).exists() == True

    def test_create_anime_list_entry_already_created(self, anime_fixture, user_fixture, anime_list_entry_fixture):
        test_details = {
            'current_episode': 1,
            'score': 9,
        }
        MiruRepository.create_anime_list_entry(
            user=user_fixture,
            anime=anime_fixture,
            status=2,
            details=test_details
        )

        assert AnimeListEntry.objects.filter(anime=anime_fixture, user=user_fixture).count() == 1

    def test_update_anime_list_success(self, user_fixture, anime_fixture):
        AnimeListEntry.objects.create(
            anime=anime_fixture,
            user=user_fixture,
            status=0
        )

        MiruRepository.update_anime_list_entry(
            user=user_fixture,
            anime=anime_fixture,
            status=3,
            details={}
        )

        assert AnimeListEntry.objects.filter(
            user=user_fixture,
            anime=anime_fixture,
            status=3
        ).exists()

    def test_update_anime_list_not_found(self, user_fixture, anime_fixture, anime_sequel_fixture):
        AnimeListEntry.objects.create(
            anime=anime_fixture,
            user=user_fixture,
            status=0
        )

        MiruRepository.update_anime_list_entry(
            user=user_fixture,
            anime=anime_sequel_fixture,
            status=3,
            details={}
        )

        assert AnimeListEntry.objects.filter(
            anime=anime_fixture,
            user=user_fixture,
            status=0
        ).exists() == True

    def test_delete_anime_list_entry_success(self, user_fixture, anime_fixture):
        AnimeListEntry.objects.create(
            anime=anime_fixture,
            user=user_fixture,
            status=0
        )

        MiruRepository.delete_anime_list_entry(
            user=user_fixture,
            anime=anime_fixture
        )

        assert AnimeListEntry.objects.filter(
            user=user_fixture,
            anime=anime_fixture
        ).exists() == False

    def test_delete_anime_list_entry_not_found(self, user_fixture, anime_fixture, anime_sequel_fixture):
        AnimeListEntry.objects.create(
            anime=anime_fixture,
            user=user_fixture,
            status=0
        )

        MiruRepository.delete_anime_list_entry(
            user=user_fixture,
            anime=anime_sequel_fixture
        )

        assert AnimeListEntry.objects.filter(
            user=user_fixture,
            anime=anime_fixture
        ).exists() == True

    def test_update_anime_list_entry_success(self, user_fixture, anime_fixture):
        AnimeListEntry.objects.create(
            anime=anime_fixture,
            user=user_fixture,
            status=0
        )

        test_details = {
            'current_episode': 12,
            'score': 10,
            'start_watch_date': '2026-03-30',
            'end_watch_date': '2026-04-20'
        }

        MiruRepository.update_anime_list_entry(
            anime=anime_fixture,
            user=user_fixture,
            status=3,
            details=test_details
        )

        assert AnimeListEntry.objects.filter(
            user=user_fixture,
            anime=anime_fixture,
            status=3
        ).exists() == True 

    def test_update_anime_list_entry_not_found(self, user_fixture, anime_fixture, anime_sequel_fixture):
        AnimeListEntry.objects.create(
            anime=anime_fixture,
            user=user_fixture,
            status=0
        )

        test_details = {
            'current_episode': 12,
            'score': 10,
            'start_watch_date': '2026-03-30',
            'end_watch_date': '2026-04-20'
        }

        assert MiruRepository.update_anime_list_entry(
            anime=anime_sequel_fixture,
            user=user_fixture,
            status=3,
            details=test_details
        ) == None