import pytest
import datetime
from api_wrappers.MP import (
    get_MP_ID, 
    get_MP, 
    get_name, 
    get_status, 
    get_reason, 
    get_club, 
    get_district, 
    get_other,
    get_mp_votings,
    get_mp_photo,
    get_mp_photo_mini
)

@pytest.fixture
def sample_mp():
    return {
        'term': 10,
        'name': "Golbik Marta",
        'details': {
            'id': 29,
            'district_num': 29,
            'district_name': "Katowice",
            'voivodeship': "śląskie",
            'club': "KO",
            'birth_date': datetime.date(1985, 4, 14),
            'birth_location': "Gliwice",
            'profession': "przedsiębiorca prywatny",
            'education_level': "wyższe",
            'number_of_votes': 19430
        }
}

def test_get_mp_details(sample_mp):
    mp_id = get_MP_ID(sample_mp['term'], sample_mp['name'])
    if mp_id:
        response = get_MP(sample_mp['term'], mp_id[0])
        
        # Verify basic details
        assert get_name(sample_mp['term'], mp_id[0], response) == "Marta Golbik"
        assert get_status(sample_mp['term'], mp_id[0], response) == True
        assert get_reason(sample_mp['term'], mp_id[0], response) == "None - MP is currently active"
        
        # Verify district information
        assert get_district(sample_mp['term'], mp_id[0], "district_num", response) == sample_mp['details']['district_num']
        assert get_district(sample_mp['term'], mp_id[0], "district_name", response) == sample_mp['details']['district_name']
        assert get_district(sample_mp['term'], mp_id[0], "voivodeship", response) == sample_mp['details']['voivodeship']
        
        # Verify additional details
        assert get_club(sample_mp['term'], mp_id[0], response) == sample_mp['details']['club']
        assert get_other(sample_mp['term'], mp_id[0], "birth_date", response) == sample_mp['details']['birth_date']
        assert get_other(sample_mp['term'], mp_id[0], "birth_location", response) == sample_mp['details']['birth_location']
        assert get_other(sample_mp['term'], mp_id[0], "profession", response) == sample_mp['details']['profession']
        assert get_other(sample_mp['term'], mp_id[0], "education_level", response) == sample_mp['details']['education_level']
        assert get_other(sample_mp['term'], mp_id[0], "number_of_votes", response) == sample_mp['details']['number_of_votes']
    else:
        pytest.skip("get_MP_ID returned an empty list")

def test_invalid_mp_id():
    invalid_id = 99999
    response = get_MP(10, invalid_id)
    assert response.status_code == 404

def test_mp_response_fields(sample_mp):
    mp_id = get_MP_ID(sample_mp['term'], sample_mp['name'])
    if mp_id:
        response = get_MP(sample_mp['term'], mp_id[0])
        data = response.json()
        
        # Verify response field types
        assert isinstance(data['id'], int)
        assert isinstance(data['firstLastName'], str)
        assert isinstance(data['lastFirstName'], str)
        assert isinstance(data['active'], bool)
        assert isinstance(data['club'], str)
        assert isinstance(data['districtNum'], int)
        assert isinstance(data['districtName'], str)
        assert isinstance(data['voivodeship'], str)
        assert isinstance(data['birthDate'], str)
        assert isinstance(data['birthLocation'], str)
        assert isinstance(data['educationLevel'], str)
        assert isinstance(data['numberOfVotes'], int)
    else:
        pytest.skip("get_MP_ID returned an empty list")

def test_get_mp_votings():
    term = 10
    mp_id = 1
    sitting = 1
    date = "2023-11-29"
    votings = get_mp_votings(term, mp_id, sitting, date)
    assert isinstance(votings, list)
    if votings:
        assert "votingNumber" in votings[0]
        assert "vote" in votings[0]

def test_get_mp_photos():
    term = 10
    mp_id = 1
    photo = get_mp_photo(term, mp_id)
    assert isinstance(photo, bytes)
    photo_mini = get_mp_photo_mini(term, mp_id)
    assert isinstance(photo_mini, bytes)
