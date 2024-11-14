import pytest
import datetime
from api_wrappers.interpelation import (
    get_interpelations,
    get_interpelation,
    get_interpelation_body,
    get_reply_body,
    get_title,
    get_date,
    get_authors,
    get_receipent,
    get_replies,
    get_repeated_interpellations,
    is_repeated_interpellation
)

@pytest.fixture
def sample_term():
    return 10

@pytest.fixture
def sample_interpellation_num():
    return "3999"

@pytest.fixture
def specific_interpellation():
    return {
        'term': 9,
        'num': 14710,
        'title': "Interpelacja w sprawie trudnej sytuacji osób niepełnosprawnych z uwagi na kwarantannę nakładaną na ich opiekunów",
        'receipt_date': datetime.date(2020, 11, 16),
        'sent_date': datetime.date(2021, 1, 20),
        'authors': ["Hanna Gill-Piątek"],
        'recipients': ["minister rodziny i polityki społecznej", "minister zdrowia"],
        'reply_key': "BW7JYC"
    }

def test_get_interpelations(sample_term):
    response = get_interpelations(sample_term, limit=5)
    assert response.status_code == 200
    interpellations = response.json()
    assert isinstance(interpellations, list)
    assert len(interpellations) <= 5

def test_get_interpelations_pagination(specific_interpellation):
    interpelations = get_interpelations(specific_interpellation['term'], limit=10, offset=20).json()
    assert len(interpelations) == 10


def test_invalid_interpellation():
    invalid_term = 99
    invalid_num = 99999
    response = get_interpelation(invalid_term, invalid_num)  
    assert response.status_code == 404

