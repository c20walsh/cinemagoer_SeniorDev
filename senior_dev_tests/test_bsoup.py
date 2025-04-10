import unittest
from imdb import Cinemagoer
from cinemagoer_SeniorDev.bsoup import filmography
# Assuming this is your custom function or data

class TestJasonStathamData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ia = Cinemagoer()
        person_search = ia.search_person("Jason Statham")
        cls.person_id = person_search[0].personID
        cls.person_info = ia.get_person(cls.person_id)
        cls.person_info['filmography'] = filmography  # Mock or real input

    def test_keys_exist(self):
        expected_keys = ['filmography']
        for key in expected_keys:
            with self.subTest(key=key):
                self.assertIn(key, self.person_info)

    def test_filmography_has_roles(self):
        roles = ['actor', 'producer', 'stunts', 'thanks', 'self', 'archive footage']
        filmography_keys = self.person_info['filmography'].keys()
        for role in roles:
            with self.subTest(role=role):
                self.assertIn(role, filmography_keys)

    def test_filmography_role_types(self):
        for role in ['actor', 'producer', 'stunts', 'thanks', 'self', 'archive footage']:
            with self.subTest(role=role):
                role_data = self.person_info['filmography'].get(role, [])
                self.assertIsInstance(role_data, list)


if __name__ == '__main__':
    unittest.main()
