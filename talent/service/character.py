from talent.repository.character import CharacterRepository
from talent.models import Character
from talent.exceptions import TalentValidationError

class CharacterService:

    @staticmethod
    def get_character(character_id: int) -> Character:
        return CharacterRepository.get_character(character_id)

    @staticmethod
    def search_characters(name: str) -> list[Character]:
        if len(name) < 3:
            raise TalentValidationError("Query must be greater than 3 characters")
        return CharacterRepository.search_characters(name=name)

    @staticmethod
    def get_characters_by_id(character_ids: list, get_va_data = False) -> list:
        """
        Filters and returns character map with ID/Key acccess
        """
        if get_va_data is True:
            characters = CharacterRepository.get_character(
                character_ids = character_ids,
                get_va_data=True
            )
        else:
            characters = CharacterRepository.get_character(
                character_ids = character_ids,
                get_va_data=False
            )
        return {
            character.id: character for character in characters
        }