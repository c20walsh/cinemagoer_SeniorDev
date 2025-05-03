import pytest
from cinemagoer_SeniorDev import movie_charts
from imdb import Cinemagoer

ia = Cinemagoer()

@pytest.fixture
def popular100_movies():
    return movie_charts.get_popular100_movies()


def test_popular_movies_chart_should_contain_100_entries(popular100_movies):
    assert len(popular100_movies) == 100


def test_popular_movies_chart_entries_should_have_rank(popular100_movies):
    for i, movie in enumerate(popular100_movies):
        assert movie["rank"] == i + 1


def test_popular_movies_chart_entries_should_have_movie_id(popular100_movies):
    for movie in popular100_movies:
        search_results = ia.search_movie(movie["title"])  # Get search results

        assert search_results, f"IMDb search failed for {movie['title']}"

        # Ensure first result has a valid IMDb ID
        imdb_id = search_results[0].movieID if search_results else None
        assert imdb_id and imdb_id.isdigit()


def test_popular_movies_chart_entries_should_have_title(popular100_movies):
    assert all("title" in movie and isinstance(movie["title"], str) and movie["title"].strip() for movie in popular100_movies)


def test_popular_movies_chart_entries_should_be_movies(popular100_movies):
    edge_cases = [popular100_movies[0], popular100_movies[-1]]  # First & Last movie

    for movie in edge_cases:
        search_results = ia.search_movie(movie["title"])  # Search IMDb by title
        assert search_results, f"IMDb search failed for {movie['title']}"

        # Retrieve full movie details using IMDb ID
        movie_data = ia.get_movie(search_results[0].movieID)

        # Ensure 'kind' exists and confirms it's a movie
        assert "kind" in movie_data and movie_data["kind"] == "movie"
