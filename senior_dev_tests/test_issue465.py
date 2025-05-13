import unittest
import os
import sys

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from awards import get_movie_awards

class TestGetMovieAwards(unittest.TestCase):
    
    def test_matrix_awards(self):
        # Test The Matrix has at least one award and includes a known win
        awards = get_movie_awards("tt0133093")
        self.assertTrue(awards)
        expected = {"category": "Academy Awards, USA", "award": "Best Film Editing", "result": "Winner"}
        self.assertIn(expected, awards)

    def test_invalid_imdb_id(self):
        awards = get_movie_awards("tt0000000")
        self.assertEqual(len(awards), 0)

    def test_non_award_sections_skipped(self):
        awards = get_movie_awards("tt0133093")
        non_award_sections = ["contribute", "recently viewed", "editorial", "user lists", "user polls"]
        for award in awards:
            self.assertFalse(
                any(section in award["category"].lower() for section in non_award_sections)
            )

if __name__ == '__main__':
    unittest.main()