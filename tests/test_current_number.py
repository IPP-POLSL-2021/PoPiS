import unittest
import requests_mock
from Controller.current_number import get_term_number, get_sitting_number, get_voting_number


class TestCurrentNumber(unittest.TestCase):
    def test_get_term_number_success(self):
        """Test get_term_number with successful API responses"""
        with requests_mock.Mocker() as m:
            # Mock successful responses for terms 10, 11, 12
            m.get('https://api.sejm.gov.pl/sejm/term10', status_code=200)
            m.get('https://api.sejm.gov.pl/sejm/term11', status_code=200)
            m.get('https://api.sejm.gov.pl/sejm/term12', status_code=404)

            result = get_term_number(current_term_number=10)
            self.assertEqual(result, 11)

    def test_get_term_number_initial_failure(self):
        """Test get_term_number when initial term is not found"""
        with requests_mock.Mocker() as m:
            m.get('https://api.sejm.gov.pl/sejm/term10', status_code=404)

            result = get_term_number(current_term_number=10)
            self.assertEqual(result, 9)

    def test_get_sitting_number_success(self):
        """Test get_sitting_number with successful API responses"""
        with requests_mock.Mocker() as m:
            # Mock successful responses for sittings 16, 17
            m.get('https://api.sejm.gov.pl/sejm/term10/proceedings/16', status_code=200)
            m.get('https://api.sejm.gov.pl/sejm/term10/proceedings/17', status_code=200)
            m.get('https://api.sejm.gov.pl/sejm/term10/proceedings/18', status_code=404)

            result = get_sitting_number(term=10, current_sitting_number=16)
            self.assertEqual(result, 17)

    def test_get_sitting_number_initial_failure(self):
        """Test get_sitting_number when initial sitting is not found"""
        with requests_mock.Mocker() as m:
            m.get('https://api.sejm.gov.pl/sejm/term10/proceedings/16', status_code=404)

            result = get_sitting_number(term=10, current_sitting_number=16)
            self.assertEqual(result, 15)

    def test_get_voting_number_success(self):
        """Test get_voting_number with successful API responses"""
        with requests_mock.Mocker() as m:
            # Mock successful responses for votings 85, 86
            m.get('https://api.sejm.gov.pl/sejm/term10/votings/16/85', status_code=200)
            m.get('https://api.sejm.gov.pl/sejm/term10/votings/16/86', status_code=200)
            m.get('https://api.sejm.gov.pl/sejm/term10/votings/16/87', status_code=404)

            result = get_voting_number(term=10, sitting=16, current_voting_number=85)
            self.assertEqual(result, 86)

    def test_get_voting_number_initial_failure(self):
        """Test get_voting_number when initial voting is not found"""
        with requests_mock.Mocker() as m:
            m.get('https://api.sejm.gov.pl/sejm/term10/votings/16/85', status_code=404)

            result = get_voting_number(term=10, sitting=16, current_voting_number=85)
            self.assertEqual(result, 84)

if __name__ == '__main__':
    unittest.main()
