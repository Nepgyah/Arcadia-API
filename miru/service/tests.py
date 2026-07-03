import pytest
from miru.service import MiruService
from miru.models import Anime

@pytest.mark.django_db
class TestAnimeSearch:

    # Additional fixture to create a diverse dataset for filtering/sorting tests
    @pytest.fixture(autouse=True)
    def setup_search_dataset(self, anime_fixture):
        """Populates additional records to verify filtering and sorting accuracy."""
        Anime.objects.create(
            title='Chainsaw Man',
            slug='chainsaw-man',
            type=0,  # TV
            status=2, # Finished Airing
            season_year=2022
        )
        Anime.objects.create(
            title='Kimi no Na wa',
            slug='kimi-no-na-wa',
            type=1,  # Movie
            status=2, # Finished Airing
            season_year=2016
        )
        Anime.objects.create(
            title='Cyberpunk: Edgerunners',
            slug='cyberpunk-edgerunners',
            type=3,  # Ona
            status=2, # Finished Airing
            season_year=2022
        )

    # --- Basic Search & Filters Tests ---

    @staticmethod
    def test_search_anime_no_arguments():
        """Ensure searching without arguments returns everything unmutilated."""
        results, pagination = MiruService.anime.search_anime()
        
        assert results.count() == 4
        assert pagination is None

    @staticmethod
    def test_search_anime_by_title_substring():
        """Ensure title searching uses an icontains check correctly."""
        filters = {'type': -1, 'status': -1, 'title': 'rock'}
        results, _ = MiruService.anime.search_anime(filters=filters)
        
        assert results.count() == 1
        assert results.first().title == 'Bocchi the rock'

    @staticmethod
    def test_search_anime_by_type_and_status():
        """Ensure explicit type and status filters filter out invalid results."""
        filters = {'type': 0, 'status': 2, 'title': ''} # TV and Finished Airing
        results, _ = MiruService.anime.search_anime(filters=filters)
        
        assert results.count() == 1
        assert results.first().title == 'Chainsaw Man'

    @staticmethod
    def test_search_anime_ignores_negative_one_and_empty_string_filters():
        """Ensure fields with values like -1 or '' bypass filtering."""
        filters = {'type': -1, 'status': -1, 'title': ''}
        results, _ = MiruService.anime.search_anime(filters=filters)
        
        assert results.count() == 4


    # --- Sorting Tests ---

    @staticmethod
    @pytest.mark.parametrize('direction, expected_first_title', [
        ('asc', 'Bocchi the rock'),
        ('desc', 'Kimi no Na wa')
    ])
    def test_search_anime_sorting_direction(direction, expected_first_title):
        """Verifies sorting category handles asc and desc directions properly."""
        sort = {'category': 'title', 'direction': direction}
        results, _ = MiruService.anime.search_anime(sort=sort)
        
        assert results.first().title == expected_first_title

    @staticmethod
    def test_search_anime_sorting_by_season_year():
        """Verifies sorting by secondary fields like season_year works."""
        sort = {'category': 'season_year', 'direction': 'asc'}
        results, _ = MiruService.anime.search_anime(sort=sort)
        
        # Elements missing the field float to the top or bottom depending on DB, 
        # but let's safely check explicit ordering on the elements that have them
        years = [a.season_year for a in results if a.season_year is not None]
        assert years == [2016, 2022, 2022]


    # --- Pagination Tests ---

    @staticmethod
    def test_search_anime_pagination_first_page():
        """Ensures pagination cuts datasets down and formats meta strings properly."""
        pagination = {'per_page': 2, 'target_page': 1}
        results, pagination_results = MiruService.anime.search_anime(pagination=pagination)
        
        assert len(results) == 2
        assert pagination_results['per_page'] == 2
        assert pagination_results['total_pages'] == 2
        assert pagination_results['total_items'] == 4
        