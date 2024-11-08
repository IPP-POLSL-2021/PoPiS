import pytest
from Controller.interpelation import get_interpelation, get_title, get_date, get_authors, get_receipent, get_replies
from Controller.MP import get_MP_ID, get_MP, get_name, get_status, get_reason, get_club, get_district, get_other
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
    assert get_authors(term, num, interpelation) == ["Tomasz Głogowski"]
    assert get_receipent(term, num, interpelation) == ["minister rodziny i polityki społecznej", "minister zdrowia"]
    replies = get_replies(term, num, interpelation)
    assert len(replies[0]) == 2
    #assert replies[0][0] == "https://orka2.sejm.gov.pl/INT9.nsf/klucz/ATTBXWKH2/$FILE/i14710-o3.pdf"
    assert len(replies[1]) == 1
    assert "<!DOCTYPE html>" in replies[1][0]

