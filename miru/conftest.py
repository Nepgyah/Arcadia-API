import pytest
from miru.models.anime import Anime, MyAnimeListData, AniListData
from miru.models.list import AnimeListEntry
from miru.models.relations import AnimeCharacter, AnimeEpisode
from miru.models.review import AnimeReview
from miru.models.favorite import FavoriteAnime
from talent.models import Character

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
def anime_sequel_fixture(anime_fixture):
    anime = Anime.objects.create(
        title='Bocchi the rock Season 2',
        slug='bocchi-the-rock-season-2',
        prev_anime=anime_fixture,
        type=0
    )

    return anime

@pytest.fixture
def bocchi_character_fixture(anime_fixture):
    """
        Returns both the list of characters and the original anime object
    """

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
    return animeCharacters, anime_fixture

@pytest.fixture
def anime_list_entry_fixture(anime_fixture, arcadia_profile_fixture):
    list_entry = AnimeListEntry.objects.create(
        profile_id=arcadia_profile_fixture.id,
        anime=anime_fixture,
        status=0
    )

    return list_entry

@pytest.fixture
def anime_mal_data_fixture(anime_fixture):

    return MyAnimeListData.objects.create(
        anime=anime_fixture,
        mal_id=1,
        rank_score=1,
        rank_popular=2
    )

@pytest.fixture
def anime_anilist_data_fixture(anime_fixture):

    return AniListData.objects.create(
        anime=anime_fixture,
        anilist_id=1,
        rank_score=1,
        rank_popular=2
    )

@pytest.fixture
def anime_episode_fixture(anime_fixture):
    return AnimeEpisode.objects.create(
        number=1,
        title="Lonely Rolling Bocchi",
        anime=anime_fixture
    )

@pytest.fixture
def anime_review_detail_fixture():
    """Returns a valid dictionary of extra fields for the review."""
    return {
        "score": 8.5,
        "text": "This anime was absolutely amazing! Highly recommended.",
        "like_count": 0,
        "dislike_count": 0,
    }


@pytest.fixture
def anime_review_fixture(arcadia_profile_fixture, anime_fixture, anime_review_detail_fixture):
    """Pre-saves a review in the DB for read/update/delete test scenarios."""
    return AnimeReview.objects.create(
        profile_id=arcadia_profile_fixture.id,
        anime=anime_fixture,
        **anime_review_detail_fixture
    )

@pytest.fixture
def favorite_anime_fixture(arcadia_profile_fixture, anime_fixture):
    """Creates a FavoriteAnime entry ahead of time for unique constraint and removal tests."""
    return FavoriteAnime.objects.create(
        profile_id=arcadia_profile_fixture.id,
        anime=anime_fixture
    )