from strawberry_django.test.client import TestClient

class ArcadiaGraphqlTests:

    app_domain: str = None
    client = TestClient('/graphql/')
    
    @staticmethod
    def get_response(client: TestClient, query: str, variables: dict = None, assert_no_errors: bool = True, headers: dict = None):
        return client.query(
            query, 
            variables=variables, 
            headers=headers,
            assert_no_errors=assert_no_errors
        )
    
    def get_data(self, response: dict):
        if self.app_domain is None:
            return response.data
        return response.data[self.app_domain]

    @staticmethod
    def assert_no_errors(response):
        assert response.errors is None

    @staticmethod
    def assert_errors_exist(response):
        assert response.errors is not None
