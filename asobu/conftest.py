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
     