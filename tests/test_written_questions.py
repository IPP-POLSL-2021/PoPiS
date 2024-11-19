import pytest
from api_wrappers.written_questions import (
    get_written_questions, 
    get_written_question, 
    get_question_body, 
    get_reply_body,
    get_title,
    get_date,
    get_authors,
    get_receipent,
    get_replies
)

def test_get_written_questions():
    response = get_written_questions(10, limit=5)
    assert response.status_code == 200
    questions = response.json()
    assert isinstance(questions, list)
    assert len(questions) <= 5

# Api Endpoint with Parameters yields SupportIDs indicitating some kind of auth error or I don't know
#def test_get_written_questions_with_filters():
#    response = get_written_questions(9, 
#        from_mp='9',           # Filter by MP
#        limit=5,                # Limit results
#        offset=0,               # Starting point
#        since='2022-01-15',     # Start date
#        till='2022-01-25',      # End date
#        title='kodeksu pracy',  # Title filter
#        to='minister finansów'  # Recipient filter
#    )
#    assert response.status_code == 200
#    questions = response.json()
#    assert isinstance(questions, list)

def test_get_written_question():
    # Using a known question number
    response = get_written_question(10, "1")
    assert response.status_code == 200
    question = response.json()
    assert isinstance(question, dict)
    assert 'title' in question
    assert 'from' in question
    assert 'to' in question

def test_get_question_body():
    body = get_question_body(10, "1")
    assert isinstance(body, str)
    assert "<!DOCTYPE html>" in body

def test_get_reply_body():
    # Note: You'll need a valid key for this test
    body = get_reply_body(10, "1", "D2VJKX")
    assert isinstance(body, str)
    assert "<!DOCTYPE html>" in body

def test_get_title():
    response = get_written_question(10, "1")
    title = get_title(10, "1", response)
    assert isinstance(title, str)
    assert len(title) > 0

def test_get_date():
    response = get_written_question(10, "1")
    receipt_date = get_date(10, "1", 'receipt_date', response)
    sent_date = get_date(10, "1", 'sent_date', response)
    assert hasattr(receipt_date, 'year')
    assert hasattr(sent_date, 'year')

def test_get_authors():
    response = get_written_question(10, "1")
    authors = get_authors(10, "1", response)
    assert isinstance(authors, list)

def test_get_receipent():
    response = get_written_question(10, "1")
    recipients = get_receipent(10, "1", response)
    assert isinstance(recipients, list)

def test_get_replies():
    response = get_written_question(10, "1")
    file_urls, htmls = get_replies(10, "1", response)
    assert isinstance(file_urls, list)
    assert isinstance(htmls, list)
