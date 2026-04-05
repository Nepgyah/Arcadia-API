import pytest

@pytest.mark.django_db
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

@pytest.mark.django_db
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

@pytest.mark.django_db
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

@pytest.mark.django_db
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