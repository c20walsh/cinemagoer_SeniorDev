import unittest
from imdb import Cinemagoer

class TestTechnicalInfoRetrieval(unittest.TestCase):
    def setUp(self):
        self.ia = Cinemagoer()
        self.movie = self.ia.get_movie('31193180')
        self.ia.update(self.movie, ['technical'])

    def test_tech_info_populated(self):
        # Ensure Tech Info is Populated After Updating a Movie with the Technical Infoset.
        tech_info = self.movie.get('tech')
        self.assertIsInstance(tech_info, dict)
        self.assertTrue(len(tech_info) > 0, "Technical info should not be empty.")

if __name__ == '__main__':
    unittest.main()
