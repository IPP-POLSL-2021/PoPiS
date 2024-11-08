import pytest
from Controller.transcripts import get_statements, get_pdf_transcript, get_statement
from datetime import datetime

def test_get_statements():
    # Using example values from test_sejm_api.py
    statements = get_statements(10, 1, "2023-11-29").json()
    assert isinstance(statements, dict)
    if 'statements' in statements:
        assert isinstance(statements['statements'], list)
        if statements['statements']:
            first_statement = statements['statements'][0]
            assert isinstance(first_statement['num'], int)
            if 'name' in first_statement:
                assert isinstance(first_statement['name'], str)
            if 'function' in first_statement:
                assert isinstance(first_statement['function'], str)

def test_get_pdf_transcript():
    # Using example values
    pdf = get_pdf_transcript(10, 1, "2023-11-29")
    assert isinstance(pdf, bytes)

def test_get_statement():
    # Using example values
    statement = get_statement(10, 1, "2023-11-29", 15)
    assert isinstance(statement, str)
    assert "<!DOCTYPE html>" in statement

def test_invalid_proceeding():
    response = get_statements(10, 999999, "2023-11-29")
    assert bool(response.text)

def test_statement_response_fields():
    statements = get_statements(10, 1, "2023-11-29").json()
    if 'statements' in statements and statements['statements']:
        first_statement = statements['statements'][0]
        assert 'num' in first_statement
        if 'startDateTime' in first_statement:
            assert isinstance(first_statement['startDateTime'], str)
        if 'endDateTime' in first_statement:
            assert isinstance(first_statement['endDateTime'], str)
    else:
        pytest.skip("get_statements returned no statements")

def test_date_parameter_formats():
    # Test with datetime object
    date = datetime(2023, 11, 29)
    statements = get_statements(10, 1, date).json()
    assert isinstance(statements, dict)

    # Test with string date
    statements = get_statements(10, 1, "2023-11-29").json()
    assert isinstance(statements, dict)
