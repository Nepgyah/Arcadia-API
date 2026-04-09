import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestAuthRestEndpoints:

    @staticmethod
    def AdminLogin_OnSuccess_Should_ReturnTokens(rest_client):
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
    def AdminLogin_InvalidCredentials_Should_ReturnError(rest_client):
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
    def AdminLogin_MissingPasswordField_Should_ReturnError(rest_client):
        response = rest_client.post(
            reverse('auth-admin-login'),
            {
                'username': 'Admin',
            },
            format='json'
        )

        assert response.status_code == 400