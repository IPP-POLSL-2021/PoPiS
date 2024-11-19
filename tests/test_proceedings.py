import pytest
from api_wrappers.proceedings import get_proceedings, get_proceeding

def test_get_proceedings():
    proceedings = get_proceedings(10).json()
    assert isinstance(proceedings, list)
    if proceedings:
        first_proceeding = proceedings[0]
        assert isinstance(first_proceeding['title'], str)
        assert isinstance(first_proceeding['number'], int)
        if 'dates' in first_proceeding:
            assert isinstance(first_proceeding['dates'], list)

def test_get_proceeding():
    # Using proceeding number 1 as example
    proceeding = get_proceeding(10, 1).json()
    assert isinstance(proceeding, dict)
    assert isinstance(proceeding['title'], str)
    assert isinstance(proceeding['number'], int)

def test_proceeding_response_fields():
    proceedings = get_proceedings(10).json()
    if proceedings:
        proceeding = proceedings[0]
        assert 'title' in proceeding
        assert 'number' in proceeding
        assert 'dates' in proceeding
        if proceeding['dates']:
            assert isinstance(proceeding['dates'][0], str)
    else:
        pytest.skip("get_proceedings returned no proceedings")

def test_proceeding_details():
    proceeding = get_proceeding(10, 1).json()
    assert 'title' in proceeding
    assert 'number' in proceeding
    assert 'dates' in proceeding
    if proceeding['dates']:
        # Verify date format
        date = proceeding['dates'][0]
        assert len(date) == 10  # YYYY-MM-DD format
        assert date[4] == '-' and date[7] == '-'
