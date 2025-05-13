import os
import sys
# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from imdb import Cinemagoer
import unittest
from unittest.mock import patch


class TestFilmographyKind(unittest.TestCase):
    @patch('builtins.input', return_value='nm0005458')
    def test_non_movie_kinds_present(self, mock_input):
        from imdb import bsoup  # Import after mocking input
        self.person_info['filmography'] = bsoup.filmography
        actor_filmography = self.person_info['filmography'].get('actor', [])
        non_movie_kinds = {'tv series', 'tv episode', 'video game', 'short'}
        kinds_found = {entry.get('kind') for entry in actor_filmography}
        self.assertTrue(non_movie_kinds & kinds_found)