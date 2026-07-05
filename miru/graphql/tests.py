import pytest
from arcadia.graphql.test_util import ArcadiaGraphqlTests
from miru.models import AnimeListEntry

@pytest.mark.django_db
class TestMiruGraphqlQuery(ArcadiaGraphqlTests):

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

    def test_user_anime_list_success(
        self,
        anime_fixture,
        arcadia_profile_fixture,
        csn_anime_fixture, 
        yourname_anime_fixture, 
        edgerunners_anime_fixture
    ):  
        AnimeListEntry.objects.create(
            profile_id=arcadia_profile_fixture.id,
            anime=anime_fixture,
            status=0
        )
        AnimeListEntry.objects.create(
            profile_id=arcadia_profile_fixture.id,
            anime=csn_anime_fixture,
            status=1
        )
        AnimeListEntry.objects.create(
            profile_id=arcadia_profile_fixture.id,
            anime=yourname_anime_fixture,
            status=2
        )
        AnimeListEntry.objects.create(
            profile_id=arcadia_profile_fixture.id,
            anime=edgerunners_anime_fixture,
            status=3
        )

        query = """
            query($id: Int!) {
                miru {
                    userAnimeList(profileId: $id) {
                        watching {
                            anime {
                                title
                            }
                        },
                        completed {
                            anime {
                                title
                            }
                        },
                        onHold {
                            anime {
                                title
                            }
                        },
                        planTo {
                            anime {
                                title
                            }
                        }
                    }
                }
            }
        """

        variables = { "id": arcadia_profile_fixture.id }
        response = self.get_response(self.client, query, variables)
        
        self.assert_no_errors(response)
        data = self.get_data(response)
        assert data['userAnimeList']['watching'][0]['anime']['title'] == anime_fixture.title
        assert data['userAnimeList']['completed'][0]['anime']['title'] == csn_anime_fixture.title
        assert data['userAnimeList']['planTo'][0]['anime']['title'] == yourname_anime_fixture.title
        assert data['userAnimeList']['onHold'][0]['anime']['title'] == edgerunners_anime_fixture.title

    def test_user_anime_list_emptylist(self):
        query = """
            query($id: Int!) {
                miru {
                    userAnimeList(profileId: $id) {
                        watching {
                            anime {
                                title
                            }
                        },
                        completed {
                            anime {
                                title
                            }
                        },
                        onHold {
                            anime {
                                title
                            }
                        },
                        planTo {
                            anime {
                                title
                            }
                        }
                    }
                }
            }
        """

        variables = { "id": 9999 }
        response = self.get_response(self.client, query, variables, assert_no_errors=False)
        
        self.assert_errors_exist(response)
