import unittest
import requests_mock
from unittest.mock import patch
import streamlit as st
from View.test import load_numbers, check_new_voting, check_interpellation_replies
from Controller.current_number import get_term_number, get_sitting_number, get_voting_number


class TestViewFunctions(unittest.TestCase):
    def setUp(self):
        # Reset Streamlit session state before each test
        st.session_state.clear()

    def test_load_numbers(self):
        """Test load_numbers function with actual API interaction simulation"""
        with requests_mock.Mocker() as m:
            # Mock API responses for term, sitting, and voting numbers
            m.get('https://api.sejm.gov.pl/sejm/term10', status_code=200)
            m.get('https://api.sejm.gov.pl/sejm/term11', status_code=404)
            m.get('https://api.sejm.gov.pl/sejm/term10/proceedings/16', status_code=200)
            m.get('https://api.sejm.gov.pl/sejm/term10/proceedings/17', status_code=404)
            m.get('https://api.sejm.gov.pl/sejm/term10/votings/16/85', status_code=200)
            m.get('https://api.sejm.gov.pl/sejm/term10/votings/16/86', status_code=404)

            # Call the actual functions
            term = get_term_number()
            sitting = get_sitting_number(term)
            voting = get_voting_number(term, sitting)

            # Verify the results
            self.assertEqual(term, 10)
            self.assertEqual(sitting, 16)
            self.assertEqual(voting, 85)

    def test_check_new_voting(self):
        """Test check_new_voting function"""
        # Simulate initial state
        st.session_state.last_voting = (0, 0, 0)

        with requests_mock.Mocker() as m:
            # Mock API responses for term, sitting, and voting numbers
            m.get('https://api.sejm.gov.pl/sejm/term10', status_code=200)
            m.get('https://api.sejm.gov.pl/sejm/term11', status_code=404)
            m.get('https://api.sejm.gov.pl/sejm/term10/proceedings/16', status_code=200)
            m.get('https://api.sejm.gov.pl/sejm/term10/proceedings/17', status_code=404)
            m.get('https://api.sejm.gov.pl/sejm/term10/votings/16/85', status_code=200)
            m.get('https://api.sejm.gov.pl/sejm/term10/votings/16/86', status_code=404)

            result = check_new_voting()
            self.assertTrue(result)
            self.assertEqual(st.session_state.last_voting, (10, 16, 85))

            # Reset mocks for second check
            m.get('https://api.sejm.gov.pl/sejm/term10', status_code=200)
            m.get('https://api.sejm.gov.pl/sejm/term11', status_code=404)
            m.get('https://api.sejm.gov.pl/sejm/term10/proceedings/16', status_code=200)
            m.get('https://api.sejm.gov.pl/sejm/term10/proceedings/17', status_code=404)
            m.get('https://api.sejm.gov.pl/sejm/term10/votings/16/85', status_code=200)
            m.get('https://api.sejm.gov.pl/sejm/term10/votings/16/86', status_code=404)

            # Test with same voting numbers
            result = check_new_voting()
            self.assertFalse(result)

    @patch('Controller.interpelation.get_replies')
    @patch('Controller.interpelation.get_title')
    def test_check_interpellation_replies(self, mock_get_title, mock_get_replies):
        """Test check_interpellation_replies function"""
        # Simulate initial state
        st.session_state.clear()

        # Setup mock data
        # Mocking get_replies to return a tuple of lists: (file_urls, htmls)
        mock_get_replies.return_value = (
            ['https://orka2.sejm.gov.pl/INT10.nsf/klucz/ATTCYXJH3/$FILE/i00001-o1.pdf'], 
            ['<html>Reply content</html>']
        )
        mock_get_title.return_value = "Test Interpellation"

        # First check should return True (new replies)
        result = check_interpellation_replies(10, 1)
        self.assertTrue(result)
        self.assertEqual(
            st.session_state.get('last_replies_10_1'), 
            ['https://orka2.sejm.gov.pl/INT10.nsf/klucz/ATTCYXJH3/$FILE/i00001-o1.pdf']
        )

        # Second check with same replies should return False
        result = check_interpellation_replies(10, 1)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
