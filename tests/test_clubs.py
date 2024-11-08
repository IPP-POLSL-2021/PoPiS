import pytest
from api_wrappers.clubs import get_clubs, get_club, get_club_logo

def test_get_clubs():
    clubs = get_clubs(10).json()
    assert isinstance(clubs, list)
    if clubs:
        first_club = clubs[0]
        assert isinstance(first_club['name'], str)
        assert isinstance(first_club['membersCount'], int)
        assert isinstance(first_club['phone'], str)
        assert isinstance(first_club['email'], str)

def test_get_club():
    # Using KO as an example club
    club = get_club(10, "KO").json()
    assert isinstance(club, dict)
    assert isinstance(club['name'], str)
    assert isinstance(club['membersCount'], int)
    assert isinstance(club['phone'], str)
    assert isinstance(club['email'], str)

def test_get_club_logo():
    # Using KO as an example club
    logo = get_club_logo(10, "KO")
    assert isinstance(logo, bytes)

def test_invalid_club():
    response = get_club(10, "INVALID_CLUB")
    assert response.status_code == 404
