import pytest
from cinemagoer_SeniorDev import movie_charts
from imdb import Cinemagoer

ia = Cinemagoer()

@pytest.fixture
def top250_movies():
    return movie_charts.get_top250_movies()


def test_top250_chart_should_contain_250_entries(top250_movies):
    assert len(top250_movies) == 250


def test_top250_chart_entries_should_have_rank(top250_movies):
    for i, movie in enumerate(top250_movies):
        assert movie["rank"] == i + 1


def test_top250_chart_entries_should_have_movie_id(top250_movies):
    for movie in top250_movies:
        search_results = ia.search_movie(movie["title"])  # Get search results

        assert search_results

        # Ensure first result has a valid IMDb ID
        imdb_id = search_results[0].movieID if search_results else None
        assert imdb_id and imdb_id.isdigit()


def test_top250_chart_entries_should_have_title(top250_movies):
    assert all("title" in movie and isinstance(movie["title"], str) and movie["title"].strip() for movie in top250_movies)


def test_top250_chart_entries_should_be_movies(top250_movies):
    edge_cases = [top250_movies[0], top250_movies[-1]]  # First & Last movie

    for movie in edge_cases:
        search_results = ia.search_movie(movie["title"])  # Search IMDb by title
        assert search_results

        # Retrieve full movie details using IMDb ID
        movie_data = ia.get_movie(search_results[0].movieID)

        # Ensure 'kind' exists and confirms it's a movie
        assert "kind" in movie_data and movie_data["kind"] == "movie"


def test_top250_chart_entries_should_have_year(top250_movies):
    edge_cases = [top250_movies[0], top250_movies[-1]]  # First & Last movie

    for movie in edge_cases:
        search_results = ia.search_movie(movie["title"])  # Get search results
        assert search_results

        # Retrieve full movie details using IMDb ID
        movie_data = ia.get_movie(search_results[0].movieID)

        # Ensure year exists and is an integer
        assert "year" in movie_data and isinstance(movie_data["year"], int)


def test_top250_chart_entries_should_have_high_ratings(top250_movies):
    edge_cases = [top250_movies[0], top250_movies[-1]]  # First & Last movie

    for movie in edge_cases:
        search_results = ia.search_movie(movie["title"])  # Get search results
        assert search_results

        # Retrieve full movie details using IMDb ID
        movie_data = ia.get_movie(search_results[0].movieID)

        # Ensure rating exists and is a valid float below 5.0
        assert "rating" in movie_data and isinstance(movie_data["rating"], float) and movie_data["rating"] > 7.5


def test_top250_chart_entries_should_have_minimal_number_of_votes(top250_movies):
    edge_cases = [top250_movies[0], top250_movies[-1]]  # First & Last movie

    for movie in edge_cases:
        search_results = ia.search_movie(movie["title"])  # Get search results
        assert search_results

        # Retrieve full movie details using IMDb ID
        movie_data = ia.get_movie(search_results[0].movieID)

        # Ensure vote count exists and is at least 1,500
        assert "votes" in movie_data and isinstance(movie_data["votes"], int) and movie_data["votes"] >= 25000
