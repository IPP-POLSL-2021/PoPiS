import pytest
from api_wrappers.interpelation import get_interpelation, get_title, get_date, get_authors, get_receipent, get_replies, get_interpelation_body, get_reply_body, get_interpelations
from api_wrappers.MP import get_MP_ID, get_MP, get_name, get_status, get_reason, get_club, get_district, get_other, get_mp_votings, get_mp_photo, get_mp_photo_mini
import datetime

def test_get_mp_details():
    mp_id = get_MP_ID(10, "Golbik Marta")
    if mp_id:
        response = get_MP(10, mp_id[0])
        assert get_name(10, mp_id[0], response) == "Marta Golbik"
        assert get_status(10, mp_id[0], response) == True
        assert get_reason(10, mp_id[0], response) == "None - MP is currently active"
        assert get_district(10, mp_id[0], "district_num", response) == 29
        assert get_district(10, mp_id[0], "district_name", response) == "Katowice"
        assert get_district(10, mp_id[0], "voivodeship", response) == "śląskie"
        assert get_club(10, mp_id[0], response) == "KO"
        assert get_other(10, mp_id[0], "birth_date", response) == datetime.date(1985, 4, 14)
        assert get_other(10, mp_id[0], "birth_location", response) == "Gliwice"
        assert get_other(10, mp_id[0], "profession", response) == "przedsiębiorca prywatny"
        assert get_other(10, mp_id[0], "education_level", response) == "wyższe"
        assert get_other(10, mp_id[0], "number_of_votes", response) == 19430
    else:
        pytest.skip("get_MP_ID returned an empty list")

def test_get_interpelation():
    term = 9
    num = 14710
    interpelation = get_interpelation(term, num)
    assert get_title(term, num, interpelation) == "Interpelacja w sprawie trudnej sytuacji osób niepełnosprawnych z uwagi na kwarantannę nakładaną na ich opiekunów"
    assert get_date(term, num, "receipt_date", interpelation) == datetime.date(2020, 11, 16)
    assert get_date(term, num, "sent_date", interpelation) == datetime.date(2021, 1, 20)
    assert get_authors(term, num, interpelation) == ["Hanna Gill-Piątek"]
    assert get_receipent(term, num, interpelation) == ["minister rodziny i polityki społecznej", "minister zdrowia"]
    replies = get_replies(term, num, interpelation)
    assert len(replies[0]) == 1
    #assert replies[0][0] == "https://orka2.sejm.gov.pl/INT9.nsf/klucz/ATTBXWKH2/$FILE/i14710-o3.pdf"
    assert len(replies[1]) == 1
    assert "<!DOCTYPE html>" in replies[1][0]

def test_invalid_mp_id():
    invalid_id = 99999
    response = get_MP(10, invalid_id)
    assert response.status_code == 404

def test_invalid_interpelation():
    invalid_term = 99
    invalid_num = 99999
    response = get_interpelation(invalid_term, invalid_num)  
    assert response.status_code == 404

def test_mp_response_fields():
    mp_id = get_MP_ID(10, "Golbik Marta")
    if mp_id:
        response = get_MP(10, mp_id[0])
        data = response.json()
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

def test_get_interpelation_body():
    term = 9
    num = 14710
    body = get_interpelation_body(term, num)
    assert "<!DOCTYPE html>" in body

def test_get_reply_body():
    term = 9
    num = 14710
    key = "BW7JYC"
    body = get_reply_body(term, num, key)
    assert "<!DOCTYPE html>" in body

def test_get_interpelations_pagination():
    term = 9
    interpelations = get_interpelations(term, limit=10, offset=20).json()
    assert len(interpelations) == 10

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
