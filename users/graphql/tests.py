import pytest

@pytest.mark.django_db
class TestUsersAppGraphql:

    def test_user_query(_self, graphql_client, arcadia_user_fixture):
        response = graphql_client(
            query = 
            '''
            query GetUser($id: ID!){
                User(userId: $id){
                    id,
                }
            }
            ''',
            variables = { 'id': str(arcadia_user_fixture.id)}
        )

        data = response.json()
        assert 'errors' not in data
        assert int(data['data']['User']['id']) == arcadia_user_fixture.id

    def test_user_query_not_found(_self, graphql_client, arcadia_user_fixture):
        response = graphql_client(
            query = 
            '''
            query GetUser($id: ID!){
                User(userId: $id){
                    id,
                }
            }
            ''',
            variables = { 'id': str(999)}
        )

        data = response.json()
        assert 'errors' in data