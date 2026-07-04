import pytest
from arcadia.graphql.test_util import ArcadiaGraphqlTests

@pytest.mark.django_db
class TestMiruGraphql(ArcadiaGraphqlTests):

    app_domain = 'miru'

    def test_anime_query(self, anime_fixture):
        query = """
            query($id: Int!) {
                miru {
                    anime(pk: $id) {
                        title
                    }
                }
            }
        """
        variables = { "id": anime_fixture.id }
        response = self.get_response(self.client, query, variables)

        self.assert_no_errors(response)
        data = self.get_data(response)
        assert data['anime']['title'] == anime_fixture.title

    def test_anime_query_not_found(self):
        query = """
            query($id: Int!) {
                miru {
                    anime(pk: $id) {
                        title
                    }
                }
            }
        """
        variables = { "id": 9999 }
        response = self.get_response(self.client, query, variables, False)
        
        self.assert_errors_exist(response)