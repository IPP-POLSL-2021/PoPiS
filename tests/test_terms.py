import pytest
from api_wrappers.terms import get_terms, get_term

def test_get_terms():
    terms = get_terms().json()
    assert isinstance(terms, list)
    if terms:
        first_term = terms[0]
        assert isinstance(first_term['num'], int)
        assert isinstance(first_term['from'], str)
        assert isinstance(first_term['to'], str)
        assert 'current' in first_term

def test_get_term():
    # Using term 10 as example
    term = get_term(10).json()
    assert isinstance(term, dict)
    assert isinstance(term['num'], int)
    assert isinstance(term['from'], str)
    try:
        assert isinstance(term['to'], str)
    except KeyError:
        assert term['current']==True
    assert 'current' in term

def test_current_term():
    terms = get_terms().json()
    current_terms = [term for term in terms if term['current']]
    assert len(current_terms) == 1, "There should be exactly one current term"
    current_term = current_terms[0]
    assert current_term['current'] is True

def test_term_response_fields():
    terms = get_terms().json()
    if terms:
        term = terms[0]
        assert 'num' in term
        assert 'from' in term
        assert 'to' in term
        assert 'current' in term
        if 'prints' in term:
            assert isinstance(term['prints'], dict)
    else:
        pytest.skip("get_terms returned no terms")

def test_term_date_formats():
    terms = get_terms().json()
    if terms:
        term = terms[0]
        # Check date formats (YYYY-MM-DD)
        assert len(term['from']) == 10
        assert len(term['to']) == 10
        assert term['from'][4] == '-' and term['from'][7] == '-'
        assert term['to'][4] == '-' and term['to'][7] == '-'
    else:
        pytest.skip("get_terms returned no terms")
