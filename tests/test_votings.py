import pytest
import requests
from api_wrappers.votings import (
    get_votings, 
    search_votings, 
    get_proceeding_votings, 
    get_voting_details,
    analyze_voting_results,
    group_votes_by_club
)

def test_get_votings():
    response = get_votings(10)
    assert response.status_code == 200, f"API returned status code {response.status_code}"
    
    try:
        votings = response.json()
        assert isinstance(votings, list)
        if votings:
            first_voting = votings[0]
            assert isinstance(first_voting['proceeding'], int)
            assert isinstance(first_voting['date'], str)
            assert isinstance(first_voting['votingsNum'], int)
    except ValueError:
        pytest.fail("Could not decode JSON response")

def test_search_votings():
    # Test with minimal parameters to reduce chance of error
    response = search_votings(10)
    assert response.status_code == 200, f"API returned status code {response.status_code}"
    
    try:
        votings = response.json()
        assert isinstance(votings, list)
        
        if votings:
            first_voting = votings[0]
            assert isinstance(first_voting['term'], int)
            assert isinstance(first_voting['title'], str)
    except ValueError:
        pytest.fail("Could not decode JSON response")

# 403 - Forbidden
#def test_search_votings_with_params():
#    # Try with minimal, known-good parameters
#    response = search_votings(10, limit=5)
#    assert response.status_code == 200, f"API returned status code {response.status_code}"
#    
#    try:
#        votings = response.json()
#        assert isinstance(votings, list)
#        assert len(votings) <= 5
#    except ValueError:
#        pytest.fail("Could not decode JSON response")

def test_get_proceeding_votings():
    # Using proceeding 1 as example
    response = get_proceeding_votings(10, 1)
    assert response.status_code == 200, f"API returned status code {response.status_code}"
    
    try:
        votings = response.json()
        assert isinstance(votings, list)
        if votings:
            first_voting = votings[0]
            assert isinstance(first_voting['term'], int)
            assert isinstance(first_voting['title'], str)
            assert isinstance(first_voting['votingNumber'], int)
    except ValueError:
        pytest.fail("Could not decode JSON response")

def test_get_voting_details():
    # Using proceeding 1, voting 1 as example
    response = get_voting_details(10, 1, 1)
    assert response.status_code == 200, f"API returned status code {response.status_code}"
    
    try:
        voting = response.json()
        assert isinstance(voting, dict)
        assert isinstance(voting['term'], int)
        assert isinstance(voting['title'], str)
        assert 'yes' in voting
        assert 'no' in voting
        assert 'abstain' in voting
        assert isinstance(voting['yes'], int)
        assert isinstance(voting['no'], int)
        assert isinstance(voting['abstain'], int)
    except ValueError:
        pytest.fail("Could not decode JSON response")

def test_voting_response_fields():
    response = get_votings(10)
    assert response.status_code == 200, f"API returned status code {response.status_code}"
    
    try:
        votings = response.json()
        if votings:
            voting = votings[0]
            assert 'proceeding' in voting
            assert 'date' in voting
            assert 'votingsNum' in voting
        else:
            pytest.skip("get_votings returned no votings")
    except ValueError:
        pytest.fail("Could not decode JSON response")

def test_analyze_voting_results():
    # Using proceeding 1, voting 1 as example
    response = get_voting_details(10, 1, 1)
    assert response.status_code == 200, f"API returned status code {response.status_code}"
    
    try:
        voting_details = response.json()
        analysis = analyze_voting_results(voting_details)
        
        assert isinstance(analysis, dict)
        assert 'total_votes' in analysis
        assert 'yes_percentage' in analysis
        assert 'no_percentage' in analysis
        assert 'abstain_percentage' in analysis
        assert 'not_participating_percentage' in analysis
        assert 'voting_kind' in analysis
        assert 'voting_title' in analysis
        assert 'voting_topic' in analysis
        
        assert 0 <= analysis['yes_percentage'] <= 100
        assert 0 <= analysis['no_percentage'] <= 100
        assert 0 <= analysis['abstain_percentage'] <= 100
        assert 0 <= analysis['not_participating_percentage'] <= 100
    except ValueError:
        pytest.fail("Could not decode JSON response")

def test_group_votes_by_club():
    # Using proceeding 1, voting 1 as example
    response = get_voting_details(10, 1, 1)
    assert response.status_code == 200, f"API returned status code {response.status_code}"
    
    try:
        voting_details = response.json()
        club_votes = group_votes_by_club(voting_details)
        
        assert isinstance(club_votes, dict)
        
        # Check that each club has the expected vote types
        for club, votes in club_votes.items():
            assert isinstance(club, str)
            assert isinstance(votes, dict)
            assert 'yes' in votes
            assert 'no' in votes
            assert 'abstain' in votes
            assert 'not_voting' in votes
            
            # Ensure vote counts are integers
            for vote_type, count in votes.items():
                assert isinstance(count, int)
                assert count >= 0
    except ValueError:
        pytest.fail("Could not decode JSON response")
