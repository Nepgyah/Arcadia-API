import pytest
from talent.models import Character
from asobu.models import Game, GameListEntry, GameCharacter

@pytest.fixture
def game_fixture():
    game = Game.objects.create(
        title='Uma Musume: Pretty derby'
    )
    return game

def create_video_game_characters(game_obj):

    characters = [
        Character(first_name='Oguri Cap', slug='oguri-cap'),
        Character(first_name='Super Creek', slug='super-creek'),
        Character(first_name='Maruzensky', slug='maruzensky'),
        Character(first_name='Gentilldonna', slug='gentilldonna')
    ]
    created_characters = Character.objects.bulk_create(characters)

    bluk_create_game_characters = []
    for character in created_characters:
        bluk_create_game_characters.append(
            GameCharacter(
                game=game_obj,
                character=character,
                is_playable=True,
                role=0
            )
        )

    return GameCharacter.objects.bulk_create(bluk_create_game_characters)

@pytest.fixture 
def game_list_entry_fixture(arcadia_user_fixture, game_fixture):
    game_entry = GameListEntry.objects.create(
        user=arcadia_user_fixture,
        game=game_fixture,
        status=1,
        score=10,
        note='Umazing',
        review='If you get boxed, you get boxed',
        start_play_date='2024-4-20',
        end_play_date=None
    )

    return game_entry