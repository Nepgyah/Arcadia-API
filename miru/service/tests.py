import pytest
from miru.service.miru_service import MiruService

@pytest.mark.django_db
class TestService:

    def test_search_anime_filters(self, anime_fixture):
        filters = {
            "type" : None,
            "status" : None,
            "title" : None
        }
        pagination = {
            "per_page": 1,
            "current_page": 1
        }
        animes, page_count, current_page = MiruService.search_anime(
            filters,
            None,
            pagination
        )
        assert anime_fixture in animes

        filters = {
            "type" : 1,
            "status" : None,
            "title" : None
        }
        animes, page_count, current_page = MiruService.search_anime(
            filters,
            None,
            pagination
        )
        assert anime_fixture not in animes