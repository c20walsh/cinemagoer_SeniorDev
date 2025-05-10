import pytest
from cinemagoer_SeniorDev import movie_charts
from imdb import Cinemagoer

ia = Cinemagoer()


@pytest.fixture
def bottom100_movies():
    return movie_charts.get_bottom100_movies()


def test_bottom_chart_should_contain_100_entries(bottom100_movies):
    assert len(bottom100_movies) == 100


def test_bottom_chart_entries_should_have_rank(bottom100_movies):
    for i, movie in enumerate(bottom100_movies):
        assert movie["rank"] == i + 1


def test_bottom_chart_entries_should_have_movie_id(bottom100_movies):
    for movie in bottom100_movies:
        search_results = ia.search_movie(movie["title"])  # Get search results

        assert search_results

        # Ensure first result has a valid IMDb ID
        imdb_id = search_results[0].movieID if search_results else None
        assert imdb_id and imdb_id.isdigit()


def test_bottom_chart_entries_should_have_title(bottom100_movies):
    assert all(
        "title" in movie and isinstance(movie["title"], str) and movie["title"].strip() for movie in bottom100_movies)


def test_bottom_chart_entries_should_be_movies(bottom100_movies):
    edge_cases = [bottom100_movies[0], bottom100_movies[-1]]  # First & Last movie

    for movie in edge_cases:
        search_results = ia.search_movie(movie["title"])  # Search IMDb by title
        assert search_results, f"IMDb search failed for {movie['title']}"

        # Retrieve full movie details using IMDb ID
        movie_data = ia.get_movie(search_results[0].movieID)

        # Ensure 'kind' exists and confirms it's a movie
        assert "kind" in movie_data and movie_data["kind"] == "movie", \
            f"Invalid kind for {movie['title']}: {movie_data.get('kind')}"


def test_bottom_chart_entries_should_have_year(bottom100_movies):
    edge_cases = [bottom100_movies[0], bottom100_movies[-1]]  # First & Last movie

    for movie in edge_cases:
        search_results = ia.search_movie(movie["title"])  # Get search results
        assert search_results

        # Retrieve full movie details using IMDb ID
        movie_data = ia.get_movie(search_results[0].movieID)

        # Ensure year exists and is an integer
        assert "year" in movie_data and isinstance(movie_data["year"], int)


def test_bottom_chart_entries_should_have_low_ratings(bottom100_movies):
    edge_cases = [bottom100_movies[0], bottom100_movies[-1]]  # First & Last movie

    for movie in edge_cases:
        search_results = ia.search_movie(movie["title"])  # Get search results
        assert search_results

        # Retrieve full movie details using IMDb ID
        movie_data = ia.get_movie(search_results[0].movieID)

        # Ensure rating exists and is a valid float below 5.0
        assert "rating" in movie_data and isinstance(movie_data["rating"], float) and movie_data["rating"] < 5.0


def test_bottom_chart_entries_should_have_minimal_number_of_votes(bottom100_movies):
    edge_cases = [bottom100_movies[0], bottom100_movies[-1]]  # First & Last movie

    for movie in edge_cases:
        search_results = ia.search_movie(movie["title"])  # Get search results
        assert search_results, f"IMDb search failed for {movie['title']}"

        # Retrieve full movie details using IMDb ID
        movie_data = ia.get_movie(search_results[0].movieID)

        # Ensure vote count exists and is at least 1,500
        assert "votes" in movie_data and isinstance(movie_data["votes"], int) and movie_data["votes"] >= 1500
