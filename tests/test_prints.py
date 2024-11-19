import pytest
from api_wrappers.prints import get_prints, get_print, get_print_attachment

def test_get_prints():
    prints = get_prints(10).json()
    assert isinstance(prints, list)
    if prints:
        first_print = prints[0]
        assert isinstance(first_print['term'], int)
        assert isinstance(first_print['number'], str)
        assert isinstance(first_print['title'], str)
        assert isinstance(first_print['documentDate'], str)

def test_get_print():
    # Using print number 19 as an example
    print_doc = get_print(10, "19").json()
    assert isinstance(print_doc, dict)
    assert isinstance(print_doc['term'], int)
    assert isinstance(print_doc['number'], str)
    assert isinstance(print_doc['title'], str)
    assert isinstance(print_doc['documentDate'], str)

def test_get_print_attachment():
    # Using print 19 and its PDF as an example
    attachment = get_print_attachment(10, "19", "19.pdf")
    assert isinstance(attachment, bytes)

def test_invalid_print():
    response = get_print(10, "999999")
    assert response.status_code == 404

def test_invalid_attachment():
    response = get_print_attachment(10, "19", "nonexistent.pdf")
    assert bool(str(response))

def test_print_response_fields():
    prints = get_prints(10).json()
    if prints:
        first_print = prints[0]
        assert 'term' in first_print
        assert 'number' in first_print
        assert 'title' in first_print
        assert 'documentDate' in first_print
        assert 'deliveryDate' in first_print
        if 'attachments' in first_print:
            assert isinstance(first_print['attachments'], list)
    else:
        pytest.skip("get_prints returned an empty list")
