from talent.repository.character import CharacterRepository

class CharacterService:

    @staticmethod
    def get_character_by_id(character_id):
        return CharacterRepository.get_character_by_id(character_id)