import unittest
import requests_mock
import requests
from Controller.current_number import get_term_number, get_sitting_number, get_voting_number


class TestCurrentNumber(unittest.TestCase):
    def test_get_term_number_success(self):
        """Test get_term_number with successful API response"""
        with requests_mock.Mocker() as m:
            # Mock API response with current term
            m.get('https://api.sejm.gov.pl/sejm/term', json=[
                {'num': 10, 'current': False},
                {'num': 11, 'current': True}
            ])

            result = get_term_number()
            self.assertEqual(result, 11)

    def test_get_sitting_number_success(self):
        """Test get_sitting_number with successful API response"""
        with requests_mock.Mocker() as m:
            # Mock term number retrieval
            m.get('https://api.sejm.gov.pl/sejm/term', json=[
                {'num': 10, 'current': True}
            ])
            
            # Mock proceedings retrieval
            m.get('https://api.sejm.gov.pl/sejm/term10/proceedings/', json=[
                {'number': 16},
                {'number': 17}
            ])

            result = get_sitting_number()
            self.assertEqual(result, 17)

    def test_get_voting_number_success(self):
        """Test get_voting_number with successful API response"""
        with requests_mock.Mocker() as m:
            # Mock term number retrieval
            m.get('https://api.sejm.gov.pl/sejm/term', json=[
                {'num': 10, 'current': True}
            ])
            
            # Mock sitting number retrieval
            m.get('https://api.sejm.gov.pl/sejm/term10/proceedings/', json=[
                {'number': 16}
            ])
            
            # Mock votings retrieval
            m.get('https://api.sejm.gov.pl/sejm/term10/votings/16', json=[
                {'id': 1}, {'id': 2}  # Simulating two votings
            ])

            result = get_voting_number()
            self.assertEqual(result, 2)

    def test_get_term_number_with_specific_term(self):
        """Test get_term_number with a specific term"""
        with requests_mock.Mocker() as m:
            # Mock API response with current term
            m.get('https://api.sejm.gov.pl/sejm/term', json=[
                {'num': 10, 'current': False},
                {'num': 11, 'current': True}
            ])

            result = get_term_number()
            self.assertEqual(result, 11)

    def test_get_sitting_number_with_specific_term(self):
        """Test get_sitting_number with a specific term"""
        with requests_mock.Mocker() as m:
            # Mock proceedings retrieval
            m.get('https://api.sejm.gov.pl/sejm/term10/proceedings/', json=[
                {'number': 16},
                {'number': 17}
            ])

            result = get_sitting_number(term=10)
            self.assertEqual(result, 17)

    def test_get_voting_number_with_specific_term_and_sitting(self):
        """Test get_voting_number with specific term and sitting"""
        with requests_mock.Mocker() as m:
            # Mock votings retrieval
            m.get('https://api.sejm.gov.pl/sejm/term10/votings/16', json=[
                {'id': 1}, {'id': 2}  # Simulating two votings
            ])

            result = get_voting_number(term=10, sitting=16)
            self.assertEqual(result, 2)


if __name__ == '__main__':
    unittest.main()
