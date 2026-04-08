import pytest
from miru.models.list_entry import AnimeListEntry

@pytest.mark.django_db
class TestMiruGraphqlQueries:
    
    @staticmethod
    def test_anime_by_id(graphql_client, anime_fixture):
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
    def test_anime_by_id_not_found(graphql_client, anime_fixture):
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
    def test_characters_by_anime(graphql_client, anime_fixture):
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
    def test_characters_by_anime_not_found(graphql_client, anime_fixture):
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
    def test_create_anime_list_entry_created(graphql_client, arcadia_user_fixture, anime_fixture):
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
    def test_create_anime_list_entry_no_anime(graphql_client, arcadia_user_fixture, anime_fixture):
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
    def test_create_anime_list_entry_no_user(graphql_client, arcadia_user_fixture, anime_fixture):
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
    def test_update_anime_list_entry_success(graphql_client, arcadia_user_fixture, anime_fixture):
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
    def test_update_anime_list_entry_no_user(graphql_client, arcadia_user_fixture, anime_fixture):
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
    def test_update_anime_list_entry_no_anime(graphql_client, arcadia_user_fixture, anime_fixture):
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
