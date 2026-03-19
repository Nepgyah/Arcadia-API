from miru.models.relations import AnimeCharacter
from talent.models import Character
from miru.anilist.syncVoiceActor import SyncVoiceActor

def SyncCharacters(anime_obj, data):

    character_data = data.get("characters").get('edges')
    
    anime_characters_list = []
    for character in character_data:
        va_data = character.get('voiceActors')

        if va_data:
            va_object = SyncVoiceActor(va_data[0])
        else:
            print('No voice actor data found')
            va_object = None
            
        first_name = character.get('node').get('name').get('first')
        last_name = character.get('node').get('name').get('last')

        if last_name == '':
            last_name = None
        try:
            arcadia_character = Character.objects.get(
                first_name=first_name,
                last_name=last_name,
                voice_actor=va_object
            )
            print(f"Character found: {arcadia_character}")
            
        except Character.DoesNotExist:
            arcadia_character = Character.objects.create(
                first_name=first_name,
                last_name=last_name,
                cover_img_url=character.get('node').get('image').get('large'),
                voice_actor=va_object
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
        


