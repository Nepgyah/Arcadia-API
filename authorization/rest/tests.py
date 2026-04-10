import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestAuthRestEndpoints:

    @staticmethod
    def test_adminLogin_onSuccess_should_returnTokens(rest_client):
        response = rest_client.post(
            reverse('auth-admin-login'),
            {
                'username': 'Admin',
                'password': 'TestPassword123'
            },
            format='json'
        )

        content = response.json()
        assert response.status_code == 200
        assert content['access_token'] is not None
        assert content['refresh_token'] is not None

    @staticmethod
    def test_adminLogin_invalidCredentials_should_returnError(rest_client):
        response = rest_client.post(
            reverse('auth-admin-login'),
            {
                'username': 'Admin',
                'password': 'Invalid'
            },
            format='json'
        )

        assert response.status_code == 400

    @staticmethod
    def test_adminLogin_missingPassword_should_returnError(rest_client):
        response = rest_client.post(
            reverse('auth-admin-login'),
            {
                'username': 'Admin',
            },
            format='json'
        )

        assert response.status_code == 400