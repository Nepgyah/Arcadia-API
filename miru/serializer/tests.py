import pytest
from miru.exceptions import MiruValidationError
from miru.serializer import AnimeListEntrySerializer

@pytest.mark.django_db
class TestAnimeListEntrySerializer:

    @staticmethod
    def test_save_validData_createsEntry(anime_fixture, arcadia_profile_fixture):
        data = {
            'profile_id': arcadia_profile_fixture.id,
            'anime': anime_fixture.id,
            "status": 1,
            "note": "",
            "current_episode": 1,
            "start_watch_date": None,
            "end_watch_date": None
        }
        serializer = AnimeListEntrySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        entry = serializer.save()

        assert entry.profile_id == arcadia_profile_fixture.id
        assert entry.anime == anime_fixture
        assert entry.status == 1
        assert entry.current_episode == 1
        assert entry.start_watch_date is None
        assert entry.end_watch_date is None

    @staticmethod
    def test_validateProfileID_invalidID_raisesValidation(anime_fixture):
        data = {
            'profile_id': 1,
            'anime': anime_fixture,
            "status": 1,
            "note": "",
            "current_episode": 1,
            "start_watch_date": None,
            "end_watch_date": None
        }

        serializer = AnimeListEntrySerializer(data=data)
        with pytest.raises(MiruValidationError):
            serializer.is_valid(raise_exception=True)

    @staticmethod
    def test_validateDates_invalidDates_raisesValidation(anime_fixture, arcadia_profile_fixture):
        data = {
            'profile_id': arcadia_profile_fixture.id,
            'anime': anime_fixture.id,
            "status": 1,
            "note": "",
            "current_episode": 1,
            "start_watch_date": "2024-10-10",
            "end_watch_date": "2020-10-10"
        }
        serializer = AnimeListEntrySerializer(data=data)
        with pytest.raises(MiruValidationError):
            serializer.is_valid(raise_exception=True)
