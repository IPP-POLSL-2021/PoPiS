import pytest
from api_wrappers.committees import (
    get_committees, 
    get_committee, 
    get_committee_sittings, 
    get_committee_sitting, 
    get_committee_sitting_html, 
    get_committee_sitting_pdf,
    find_next_committee_sitting,
    get_committee_stats
)
from datetime import datetime, date

def test_get_committees():
    response = get_committees(10)
    assert response.status_code == 200
    committees = response.json()
    assert isinstance(committees, list)
    if committees:
        first_committee = committees[0]
        assert 'code' in first_committee
        assert 'name' in first_committee

def test_get_committee():
    # Using a known committee code
    committees = get_committees(10).json()
    if not committees:
        pytest.skip("No committees found")
    
    # Use the first committee's code
    code = committees[0]['code']
    response = get_committee(10, code)
    assert response.status_code == 200
    committee = response.json()
    assert isinstance(committee, dict)
    assert 'code' in committee
    assert 'name' in committee

def test_get_committee_sittings():
    # Using a known committee code
    committees = get_committees(10).json()
    if not committees:
        pytest.skip("No committees found")
    
    # Use the first committee's code
    code = committees[0]['code']
    response = get_committee_sittings(10, code)
    assert response.status_code == 200
    sittings = response.json()
    assert isinstance(sittings, list)

def test_get_committee_sitting():
    # Using a known committee code
    committees = get_committees(10).json()
    if not committees:
        pytest.skip("No committees found")
    
    # Use the first committee's code
    code = committees[0]['code']
    
    # Get sittings for this committee
    sittings = get_committee_sittings(10, code).json()
    if not sittings:
        pytest.skip("No sittings found for this committee")
    
    # Use the first sitting number
    sitting_num = sittings[0]['num']
    response = get_committee_sitting(10, code, sitting_num)
    assert response.status_code == 200
    sitting = response.json()
    assert isinstance(sitting, dict)
    assert 'date' in sitting
    assert 'num' in sitting

def test_get_committee_sitting_html():
    # Using a known committee code
    committees = get_committees(10).json()
    if not committees:
        pytest.skip("No committees found")
    
    # Use the first committee's code
    code = committees[0]['code']
    
    # Get sittings for this committee
    sittings = get_committee_sittings(10, code).json()
    if not sittings:
        pytest.skip("No sittings found for this committee")
    
    # Use the first sitting number
    sitting_num = sittings[0]['num']
    html = get_committee_sitting_html(10, code, sitting_num)
    assert isinstance(html, str)
    assert len(html) > 0

def test_get_committee_sitting_pdf():
    # Using a known committee code
    committees = get_committees(10).json()
    if not committees:
        pytest.skip("No committees found")
    
    # Use the first committee's code
    code = committees[0]['code']
    
    # Get sittings for this committee
    sittings = get_committee_sittings(10, code).json()
    if not sittings:
        pytest.skip("No sittings found for this committee")
    
    # Use the first sitting number
    sitting_num = sittings[0]['num']
    pdf = get_committee_sitting_pdf(10, code, sitting_num)
    assert isinstance(pdf, bytes)
    assert len(pdf) > 0

def test_find_next_committee_sitting():
    # Using a known committee code
    committees = get_committees(10).json()
    if not committees:
        pytest.skip("No committees found")
    
    # Use the first committee's code
    code = committees[0]['code']
    
    next_sitting = find_next_committee_sitting(10, code)
    # Allow for None, date, or error string
    assert next_sitting is None or \
           isinstance(next_sitting, (datetime, date)) or \
           isinstance(next_sitting, str), \
           f"Unexpected type: {type(next_sitting)}"

def test_get_committee_stats():
    # Test with a specific committee
    committees = get_committees(10).json()
    if not committees:
        pytest.skip("No committees found")
    
    # Use the first committee's code
    code = committees[0]['code']
    
    clubs, peoples = get_committee_stats(10, code)
    
    # Validate clubs dictionary
    assert isinstance(clubs, dict)
    
    # Validate peoples dictionary
    assert isinstance(peoples, dict)

def test_get_committee_stats_all():
    # Test getting stats for all committees
    clubs, peoples = get_committee_stats(10)
    
    # Validate clubs dictionary
    assert isinstance(clubs, dict)
    
    # Validate peoples dictionary
    assert isinstance(peoples, dict)
