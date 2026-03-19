from miru.models.relations import AnimeCharacter
from talent.models import Character
def SyncCharacters(anime_obj, data):

    character_data = data.get("characters").get('edges')
    
    anime_characters_list = []
    for character in character_data:
        first_name = character.get('node').get('name').get('first')
        last_name = character.get('node').get('name').get('last')
        if last_name == '':
            last_name = None
        try:
            arcadia_character = Character.objects.get(
                first_name=first_name,
                last_name=last_name
            )
            print(f"Character found: {arcadia_character}")
        except Character.DoesNotExist:
            arcadia_character = Character.objects.create(
                first_name=first_name,
                last_name=last_name
            )
            print(f"New character created: {arcadia_character}")

        if character.get('role') == 'MAIN':
            role = 0
        else:
            role = 1

        temp_anime_character = AnimeCharacter(
            anime=anime_obj,
            role=role,
            character=arcadia_character
        )

        anime_characters_list.append(temp_anime_character)

    AnimeCharacter.objects.bulk_create(anime_characters_list)
        


