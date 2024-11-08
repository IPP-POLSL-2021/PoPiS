import pytest
import requests
from api_wrappers.votings import get_votings, search_votings, get_proceeding_votings, get_voting_details

def test_get_votings():
    votings = get_votings(10).json()
    assert isinstance(votings, list)
    if votings:
        first_voting = votings[0]
        assert isinstance(first_voting['proceeding'], int)
        assert isinstance(first_voting['date'], str)
        assert isinstance(first_voting['votingsNum'], int)

def test_search_votings():
    # Test with minimal parameters to reduce chance of error
    response = search_votings(10)
    
    # Check response status
    assert response.status_code == 200, f"API returned status code {response.status_code}"
    
    # Check response content
    try:
        votings = response.json()
        
        # If it's a list, validate its contents
        if isinstance(votings, list):
            if votings:
                first_voting = votings[0]
                assert isinstance(first_voting['term'], int)
                assert isinstance(first_voting['title'], str)
        # If it's a dict, it might be an error response
        elif isinstance(votings, dict):
            # Print out the dict to understand the error
            print("Unexpected response:", votings)
            pytest.fail("Search votings returned a dictionary instead of a list")
        else:
            pytest.fail(f"Unexpected response type: {type(votings)}")
    except ValueError as e:
        # This catches JSON decoding errors
        pytest.fail(f"Could not decode JSON response: {str(e)}")

#def test_search_votings_with_params():
#    # Try with minimal, known-good parameters
#    response = search_votings(10, limit=5)
#    
#    #assert response.status_code == 200, f"API returned status code {response.status_code}"
#    
#    try:
#        votings = response.json()
#        assert isinstance(votings, list)
#       assert len(votings) <= 5
#   except ValueError as e:
#        pytest.fail(f"Could not decode JSON response: {str(e)}")

def test_get_proceeding_votings():
    # Using proceeding 1 as example
    votings = get_proceeding_votings(10, 1).json()
    assert isinstance(votings, list)
    if votings:
        first_voting = votings[0]
        assert isinstance(first_voting['term'], int)
        assert isinstance(first_voting['title'], str)
        assert isinstance(first_voting['votingNumber'], int)

def test_get_voting_details():
    # Using proceeding 1, voting 1 as example
    voting = get_voting_details(10, 1, 1).json()
    assert isinstance(voting, dict)
    assert isinstance(voting['term'], int)
    assert isinstance(voting['title'], str)
    assert 'yes' in voting
    assert 'no' in voting
    assert 'abstain' in voting
    assert isinstance(voting['yes'], int)
    assert isinstance(voting['no'], int)
    assert isinstance(voting['abstain'], int)

def test_voting_response_fields():
    votings = get_votings(10).json()
    if votings:
        voting = votings[0]
        assert 'proceeding' in voting
        assert 'date' in voting
        assert 'votingsNum' in voting
    else:
        pytest.skip("get_votings returned no votings")
