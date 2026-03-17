import json
import pytest
from graphene_django.utils.testing import graphql_query

@pytest.fixture
def client_query(client):
    def func(query, variables=None):
        return graphql_query(query, variables=variables, client=client, graphql_url='/graphql/')
    return func

@pytest.mark.django_db
def test_anime_by_id(client_query, anime_fixture):
    response = client_query(
        query = '''
            query GetAnime($id: ID!) {
                animeById(id: $id) {
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

@pytest.mark.django_db
def test_anime_by_id_not_found(client_query, anime_fixture):
    response = client_query(
        query = '''
            query GetAnime($id: ID!) {
                animeById(id: $id) {
                    id
                    title
                    score
                }
            }
        ''',
        variables = {'id': str(0)}
    )
    content = response.json()

    assert 'errors' not in content
    assert content['data']['animeById'] == None

@pytest.mark.django_db
def test_characters_by_anime(client_query, anime_fixture):
    response = client_query(
        query = '''
            query GetCharactersByAnime($id: ID!) {
                charactersByAnime(id: $id) {
                    id
                }
            }
        ''',
        variables = {'id': str(anime_fixture.id)}
    )
    content = response.json()

    assert 'errors' not in content

@pytest.mark.django_db
def test_characters_by_anime_not_found(client_query, anime_fixture):
    response = client_query(
        query = '''
            query GetCharactersByAnime($id: ID!) {
                charactersByAnime(id: $id) {
                    id
                }
            }
        ''',
        variables = {'id': str(0)}
    )
    content = response.json()

    assert 'errors' not in content
    assert content['data']['charactersByAnime'] == []