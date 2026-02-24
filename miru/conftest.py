import pytest
from miru.models import Anime, AnimeCharacter
from characters.models import Character

# Conftest allows you to declare fixtures and have every test below in the tree access them
# Fixtures define steps and the data as part of the arrange phase of testing
@pytest.fixture
def anime_fixture():
    anime = Anime.objects.create(
        title='Bocchi the rock',
        slug='bocchi-the-rock',
        type=0
    )

    return anime

@pytest.fixture
def bocchi_character_fixtures(anime_fixture):
    characters = [
        Character(first_name='Hitori', last_name='Gotoh',slug='hitori-gotoh'),
        Character(first_name='Ikuyo', last_name='Kita', slug='ikuyo-kita'),
        Character(first_name='Nijika', last_name='Ichiji', slug='nijika-ichiji'),
        Character(first_name='Ryo', last_name='Yamada', slug='ryo-yamada'),
    ]
    characters = Character.objects.bulk_create(characters)

    bulk_anime_characters = [
        AnimeCharacter(anime=anime_fixture, character=characters[0], role=0),
        AnimeCharacter(anime=anime_fixture, character=characters[1], role=0),
        AnimeCharacter(anime=anime_fixture, character=characters[2], role=0),
        AnimeCharacter(anime=anime_fixture, character=characters[3], role=0)
    ]

    animeCharacters = AnimeCharacter.objects.bulk_create(bulk_anime_characters)
    return animeCharacters