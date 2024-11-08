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

def test_specific_interpellation_details(specific_interpellation):
    term = specific_interpellation['term']
    num = specific_interpellation['num']
    
    # Get the interpellation
    interpelation = get_interpelation(term, num)
    
    # Test title
    assert get_title(term, num, interpelation) == specific_interpellation['title']
    
    # Test dates
    assert get_date(term, num, "receipt_date", interpelation) == specific_interpellation['receipt_date']
    assert get_date(term, num, "sent_date", interpelation) == specific_interpellation['sent_date']
    
    # Test authors and recipients
    assert get_authors(term, num, interpelation) == specific_interpellation['authors']
    assert get_receipent(term, num, interpelation) == specific_interpellation['recipients']
    
    # Test replies
    replies = get_replies(term, num, interpelation)
    assert len(replies[0]) == 1  # File URLs
    assert len(replies[1]) == 1  # HTML replies
    assert "<!DOCTYPE html>" in replies[1][0]

def test_get_interpelation_body(specific_interpellation):
    body = get_interpelation_body(specific_interpellation['term'], specific_interpellation['num'])
    assert "<!DOCTYPE html>" in body

def test_get_reply_body(specific_interpellation):
    body = get_reply_body(
        specific_interpellation['term'], 
        specific_interpellation['num'], 
        specific_interpellation['reply_key']
    )
    assert "<!DOCTYPE html>" in body

def test_invalid_interpellation():
    invalid_term = 99
    invalid_num = 99999
    response = get_interpelation(invalid_term, invalid_num)  
    assert response.status_code == 404

def test_general_interpellation_methods(sample_term, sample_interpellation_num):
    # Test methods with a different interpellation
    response = get_interpelation(sample_term, sample_interpellation_num)
    
    # Basic method tests
    title = get_title(sample_term, sample_interpellation_num, response)
    assert isinstance(title, str)
    assert len(title) > 0
    
    receipt_date = get_date(sample_term, sample_interpellation_num, 'receipt_date', response)
    sent_date = get_date(sample_term, sample_interpellation_num, 'sent_date', response)
    last_modified = get_date(sample_term, sample_interpellation_num, 'last_modified', response)
    
    assert isinstance(receipt_date, datetime.date)
    assert isinstance(sent_date, datetime.date)
    assert isinstance(last_modified, datetime.date)
    
    # Additional method tests
    authors = get_authors(sample_term, sample_interpellation_num, response)
    recipients = get_receipent(sample_term, sample_interpellation_num, response)
    
    assert isinstance(authors, list)
    assert isinstance(recipients, list)
    
    file_urls, htmls = get_replies(sample_term, sample_interpellation_num, response)
    assert isinstance(file_urls, list)
    assert isinstance(htmls, list)
    
    # Optional methods
    repeated = get_repeated_interpellations(sample_term, sample_interpellation_num, response)
    is_repeated = is_repeated_interpellation(sample_term, sample_interpellation_num, response)
    
    assert isinstance(repeated, list)
    assert isinstance(is_repeated, bool)
