import pytest
from base.models import Genre
from miru.exceptions import MiruError, MiruNotFoundError
from miru.service import MiruService
from miru.models import Anime, AnimeListEntry

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

@pytest.mark.django_db
class TestGetSimilarAnime:

    @pytest.fixture
    def genre_fixtures(self):
        """Creates a couple of genres for testing similarity mapping."""
        slice_of_life = Genre.objects.create(name='Slice of Life')
        music = Genre.objects.create(name='Music')
        action = Genre.objects.create(name='Action')
        return {
            'slice_of_life': slice_of_life,
            'music': music,
            'action': action
        }

    @pytest.fixture
    def setup_similarity_dataset(self, anime_fixture, genre_fixtures):
        """Sets up a network of animes sharing genres with Bocchi the Rock."""
        # Bocchi the Rock (Origin) gets Slice of Life + Music
        anime_fixture.genres.add(genre_fixtures['slice_of_life'], genre_fixtures['music'])

        # Similar Anime 1: Shares both genres
        k_on = Anime.objects.create(title='K-On!', slug='k-on', type=0)
        k_on.genres.add(genre_fixtures['slice_of_life'], genre_fixtures['music'])

        # Similar Anime 2: Shares only one genre (Slice of Life)
        yuru_camp = Anime.objects.create(title='Yuru Camp', slug='yuru-camp', type=0)
        yuru_camp.genres.add(genre_fixtures['slice_of_life'])

        # Unrelated Anime: Shares no genres (Action only)
        chainsaw_man = Anime.objects.create(title='Chainsaw Man', slug='chainsaw-man', type=0)
        chainsaw_man.genres.add(genre_fixtures['action'])

        return anime_fixture

    # --- Business Logic Clamping Tests ---

    @staticmethod
    def test_get_similar_anime_clamps_negative_count(setup_similarity_dataset):
        """Ensure a count below 0 is clamped to 0, returning an empty list."""
        origin_anime = setup_similarity_dataset
        
        # Passing -5 should clamp to 0 inside the service method
        results = MiruService.anime.get_similar_anime(anime_id=origin_anime.id, count=-5)
        
        assert len(results) == 0

    @staticmethod
    def test_get_similar_anime_clamps_excessive_count(setup_similarity_dataset):
        """Ensure a count above 10 is clamped to 10."""
        origin_anime = setup_similarity_dataset
        
        # Create 12 quick generic matching placeholder records to check the cap limit
        genre = origin_anime.genres.first()
        for i in range(12):
            a = Anime.objects.create(title=f'Placeholder {i}', slug=f'placeholder-{i}', type=0)
            a.genres.add(genre)

        # Passing 99 should clamp down to 10 records maximum
        results = MiruService.anime.get_similar_anime(anime_id=origin_anime.id, count=99)
        
        assert len(results) == 10

    # --- Integration Extraction Tests ---

    @staticmethod
    def test_get_similar_anime_returns_correct_matches(setup_similarity_dataset):
        """Ensure it returns related anime records while excluding the target origin anime itself."""
        origin_anime = setup_similarity_dataset
        
        results = MiruService.anime.get_similar_anime(anime_id=origin_anime.id, count=5)
        
        # Should return K-On! and Yuru Camp, but completely exclude Chainsaw Man and Bocchi itself
        assert len(results) == 2
        
        result_titles = [anime.title for anime in results]
        assert 'K-On!' in result_titles
        assert 'Yuru Camp' in result_titles
        assert 'Bocchi the rock' not in result_titles
        assert 'Chainsaw Man' not in result_titles

@pytest.mark.django_db
class TestListModule:

    @pytest.fixture(autouse=True)
    def setup_search_dataset(self, arcadia_profile_fixture):
        """Populates additional records to verify filtering and sorting accuracy."""
        chainsaw_anime = Anime.objects.create(
            title='Chainsaw Man',
            slug='chainsaw-man',
            type=0,  # TV
            status=2, # Finished Airing
            season_year=2022
        )
        AnimeListEntry.objects.create(
            profile_id=arcadia_profile_fixture.id,
            anime=chainsaw_anime,
            status=1
        )
        yourname_anime = Anime.objects.create(
            title='Kimi no Na wa',
            slug='kimi-no-na-wa',
            type=1,  # Movie
            status=2, # Finished Airing
            season_year=2016
        )
        AnimeListEntry.objects.create(
            profile_id=arcadia_profile_fixture.id,
            anime=yourname_anime,
            status=2
        )
        cyberpunk_anime = Anime.objects.create(
            title='Cyberpunk: Edgerunners',
            slug='cyberpunk-edgerunners',
            type=3,  # Ona
            status=2, # Finished Airing
            season_year=2022
        )
        AnimeListEntry.objects.create(
            profile_id=arcadia_profile_fixture.id,
            anime=cyberpunk_anime,
            status=3
        )

    @staticmethod
    def test_create_entry_success(arcadia_profile_fixture, anime_fixture, anime_list_entry_detail_fixture):
        result = MiruService.list.create_entry(arcadia_profile_fixture.id, anime_fixture.id, anime_list_entry_detail_fixture)
        assert isinstance(result, AnimeListEntry) is True

    @staticmethod
    def test_create_entry_no_details_raises_error(arcadia_profile_fixture, anime_fixture):
        with pytest.raises(MiruError):
            MiruService.list.create_entry(arcadia_profile_fixture.id, anime_fixture.id, None)

    @staticmethod
    def test_create_entry_missing_anime_raises_error(arcadia_profile_fixture):
        with pytest.raises(MiruNotFoundError):
            MiruService.list.create_entry(arcadia_profile_fixture.id, 9999, None)

    @staticmethod
    def test_get_user_list_success(anime_list_entry_fixture):
        user_list = MiruService.list.get_user_list(anime_list_entry_fixture.profile_id)
        assert len(user_list['watching']) == 1
        assert len(user_list['completed']) == 1
        assert len(user_list['plan_to']) == 1
        assert len(user_list['on_hold']) == 1

    @staticmethod
    def test_get_user_list_no_entries():
        user_list = MiruService.list.get_user_list(9999)
        assert len(user_list['watching']) == 0
        assert len(user_list['completed']) == 0
        assert len(user_list['plan_to']) == 0
        assert len(user_list['on_hold']) == 0
