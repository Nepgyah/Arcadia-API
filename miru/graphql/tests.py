import pytest
from miru.models.list_entry import AnimeListEntry

@pytest.mark.django_db
class TestMiruGraphqlQueries:
    
    @staticmethod
    def AnimeByID_ValidID_Should_ReturnAnimeObject(graphql_client, anime_fixture):
        response = graphql_client(
            query = '''
                query GetAnime($id: ID!) {
                    animeById(animeId: $id) {
                        id
                        title
                        score
                    }
                }
            ''',
            variables = {'id': str(anime_fixture.id)}
        )

        content = response.json()
        assert 'errors' not in content

    @staticmethod
    def AnimeByID_InvalidID_Should_ReturnNone(graphql_client, anime_fixture):
        response = graphql_client(
            query = '''
                query GetAnime($id: ID!) {
                    animeById(animeId: $id) {
                        id
                        title
                        score
                    }
                }
            ''',
            variables = {'id': str(0)}
        )
        content = response.json()

        assert 'errors' in content
        assert content['data']['animeById'] is None

    @staticmethod
    def CharsByAnime_ValidAnime_Should_ReturnAnimeCharList(graphql_client, anime_fixture):
        response = graphql_client(
            query = '''
                query GetCharactersByAnime($id: ID!) {
                    charactersByAnime(animeId: $id) {
                        id
                    }
                }
            ''',
            variables = {'id': str(anime_fixture.id)}
        )
        content = response.json()

        assert 'errors' not in content

    @staticmethod
    def CharsByAnime_InvalidAnime_Should_ReturnNone(graphql_client, anime_fixture):
        response = graphql_client(
            query = '''
                query GetCharactersByAnime($id: ID!) {
                    charactersByAnime(animeId: $id) {
                        id
                    }
                }
            ''',
            variables = {'id': str(0)}
        )
        content = response.json()

        assert 'errors' in content
        assert content['data']['charactersByAnime'] == None

@pytest.mark.django_db
class TestMiruGraphqlMutations:

    @staticmethod
    def CreateListEntry_ValidData_Should_CreateEntry(graphql_client, arcadia_user_fixture, anime_fixture):
        query =  '''
        mutation AddAnimeEntry($animeId: ID!, $status: Int!, $details: AnimeListEntryMetaData! ){
            addAnimeListEntry(animeId: $animeId, status: $status, details: $details) {
                message,
                animeEntry {
                    id,
                    anime {
                        id
                    }
                }
            }
        }
        '''
        variables = {
            'animeId': anime_fixture.id,
            'status': 1,
            'details' : {
                'currentEpisode': 1,
                'score': 10,
            }
        }
        response = graphql_client(
            query=query,
            variables=variables,
            user=arcadia_user_fixture
        )

        content = response.json()
        assert 'errors' not in content
        assert content['data']['addAnimeListEntry']['animeEntry']['anime']['id'] == str(anime_fixture.id)

    @staticmethod
    def CreateListEntry_InvalidAnime_Should_ReturnNone(graphql_client, arcadia_user_fixture, anime_fixture):
        query =  '''
        mutation AddAnimeEntry($animeId: ID!, $status: Int!, $details: AnimeListEntryMetaData! ){
            addAnimeListEntry(animeId: $animeId, status: $status, details: $details) {
                message,
                animeEntry {
                    id,
                    anime {
                        id
                    }
                }
            }
        }
        '''
        variables = {
            'animeId': -1,
            'status': 1,
            'details' : {
                'currentEpisode': 1,
                'score': 10,
            }
        }
        response = graphql_client(
            query=query,
            variables=variables,
            user=arcadia_user_fixture
        )

        content = response.json()
        assert 'errors' in content
        assert content['data']['addAnimeListEntry'] is None

    @staticmethod
    def CreateListEntry_NoUser_Should_ReturnNone(graphql_client, arcadia_user_fixture, anime_fixture):
        query =  '''
        mutation AddAnimeEntry($animeId: ID!, $status: Int!, $details: AnimeListEntryMetaData! ){
            addAnimeListEntry(animeId: $animeId, status: $status, details: $details) {
                message,
                animeEntry {
                    id,
                    anime {
                        id
                    }
                }
            }
        }
        '''
        variables = {
            'animeId': anime_fixture.id,
            'status': 1,
            'details' : {
                'currentEpisode': 1,
                'score': 10,
            }
        }
        response = graphql_client(
            query=query,
            variables=variables,
        )

        content = response.json()
        assert 'errors' in content
        assert content['data']['addAnimeListEntry'] is None

    @staticmethod
    def UpdateListEntry_ValidData_Should_ReturnEntryData(graphql_client, arcadia_user_fixture, anime_fixture):
        AnimeListEntry.objects.create(
            user=arcadia_user_fixture,
            anime=anime_fixture,
            status=0
        )

        query =  '''
        mutation UpdateAnimeEntry($animeId: ID!, $status: Int!, $details: AnimeListEntryMetaData! ){
            updateAnimeListEntry(animeId: $animeId, status: $status, details: $details) {
                message,
                animeEntry {
                    id,
                    anime {
                        id
                    }
                }
            }
        }
        '''
        variables = {
            'animeId': anime_fixture.id,
            'status': 1,
            'details' : {
                'currentEpisode': 1,
                'score': 10,
            }
        }

        response = graphql_client(
            query=query,
            variables=variables,
            user=arcadia_user_fixture
        )

        content = response.json()
        update_fixture = AnimeListEntry.objects.get(
            user=arcadia_user_fixture,
            anime=anime_fixture
        )
        assert 'errors' not in content
        assert content['data']['updateAnimeListEntry'] is not None
        assert update_fixture.status == 1

    @staticmethod
    def UpdateListEntry_NoUser_Should_ReturnNone(graphql_client, arcadia_user_fixture, anime_fixture):
        AnimeListEntry.objects.create(
            user=arcadia_user_fixture,
            anime=anime_fixture,
            status=0
        )

        query =  '''
        mutation UpdateAnimeEntry($animeId: ID!, $status: Int!, $details: AnimeListEntryMetaData! ){
            updateAnimeListEntry(animeId: $animeId, status: $status, details: $details) {
                message,
                animeEntry {
                    id,
                    anime {
                        id
                    }
                }
            }
        }
        '''
        variables = {
            'animeId': anime_fixture.id,
            'status': 1,
            'details' : {
                'currentEpisode': 1,
                'score': 10,
            }
        }

        response = graphql_client(
            query=query,
            variables=variables,
        )

        content = response.json()
        assert 'errors' in content

    @staticmethod
    def UpdateListEntry_NoAnime_Should_ReturnNone(graphql_client, arcadia_user_fixture, anime_fixture):
        AnimeListEntry.objects.create(
            user=arcadia_user_fixture,
            anime=anime_fixture,
            status=0
        )

        query =  '''
        mutation UpdateAnimeEntry($animeId: ID!, $status: Int!, $details: AnimeListEntryMetaData! ){
            updateAnimeListEntry(animeId: $animeId, status: $status, details: $details) {
                message,
                animeEntry {
                    id,
                    anime {
                        id
                    }
                }
            }
        }
        '''
        variables = {
            'animeId': -1,
            'status': 1,
            'details' : {
                'currentEpisode': 1,
                'score': 10,
            }
        }

        response = graphql_client(
            query=query,
            variables=variables,
            user=arcadia_user_fixture
        )

        content = response.json()
        update_fixture = AnimeListEntry.objects.get(
            user=arcadia_user_fixture,
            anime=anime_fixture
        )
        assert 'errors' in content
