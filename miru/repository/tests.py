import pytest
from .miru_repository import MiruRepository

# Declares that the tests have database acccess
@pytest.mark.django_db
class TestRepository:

    def test_get_anime_by_id_returns_anime(self, anime_fixture):
        anime = MiruRepository.get_anime_by_id(anime_fixture.id)
        assert anime.slug == 'bocchi-the-rock'

    def test_get_anime_by_id_returns_none(self, anime_fixture):
        anime = MiruRepository.get_anime_by_id(99)
        assert anime == None

    def test_get_characters_by_anime(self, anime_fixture, bocchi_character_fixtures):
        characters = MiruRepository.get_characters_by_anime(id=anime_fixture.id)
        assert bocchi_character_fixtures[0] in characters

    def test_get_characters_by_anime_returns_none(self, anime_fixture, bocchi_character_fixtures):
        characters = MiruRepository.get_characters_by_anime(0)
        assert characters == []