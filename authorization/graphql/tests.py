import pytest

@pytest.mark.django_db
class TestGraphqlMutations:

    @staticmethod
    def test_admin_login_success(graphql_client, arcadia_user_fixture):
        mutation = '''
        mutation AdminLogin($username: String!, $password: String!) {
            adminLogin(username: $username, password: $password) {
                refreshToken,
                accessToken
            }
        }
        '''
        variables = {
            'username': arcadia_user_fixture.admin_user.username,
            'password': 'TestPassword123'
        }
        response = graphql_client(
            mutation,
            variables=variables
        )
        content = response.json()

        assert 'errors' not in content
        assert content['data']['adminLogin']['refreshToken'] is not None
        assert content['data']['adminLogin']['accessToken'] is not None

    @staticmethod
    def test_admin_login_invalid_credentials(graphql_client, arcadia_user_fixture):
        mutation = '''
        mutation AdminLogin($username: String!, $password: String!) {
            adminLogin(username: $username, password: $password) {
                refreshToken,
                accessToken
            }
        }
        '''
        variables = {
            'username': 'IncorrectUsername',
            'password': 'TestPassword123'
        }
        response = graphql_client(
            mutation,
            variables=variables
        )
        content = response.json()

        assert 'errors' in content
        assert content['data']['adminLogin'] is None

    @staticmethod
    def test_admin_login_no_arcadia_user(graphql_client, admin_user_fixture):
        mutation = '''
        mutation AdminLogin($username: String!, $password: String!) {
            adminLogin(username: $username, password: $password) {
                refreshToken,
                accessToken
            }
        }
        '''
        variables = {
            'username': admin_user_fixture.username,
            'password': 'TestPassword123'
        }
        response = graphql_client(
            mutation,
            variables=variables
        )
        content = response.json()

        assert 'errors' in content
        assert content['data']['adminLogin'] is None