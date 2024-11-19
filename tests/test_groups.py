import pytest
from api_wrappers.groups import get_groups, get_group

def test_get_groups():
    groups = get_groups(10).json()
    assert isinstance(groups, list)
    if groups:
        first_group = groups[0]
        assert isinstance(first_group['id'], int)
        assert isinstance(first_group['name'], str)
        if 'engName' in first_group:
            assert isinstance(first_group['engName'], str)

def test_get_group():
    # Using group ID 463 as example
    group = get_group(10, 463).json()
    assert isinstance(group, dict)
    assert isinstance(group['id'], int)
    assert isinstance(group['name'], str)
    if 'members' in group:
        assert isinstance(group['members'], list)

def test_group_response_fields():
    groups = get_groups(10).json()
    if groups:
        group = groups[0]
        assert 'id' in group
        assert 'name' in group
        assert 'appointmentDate' in group
    else:
        pytest.skip("get_groups returned no groups")

def test_group_details():
    group = get_group(10, 463).json()
    assert 'id' in group
    assert 'name' in group
    assert 'appointmentDate' in group
    if 'members' in group:
        member = group['members'][0]
        assert 'id' in member
        assert 'name' in member
        assert 'club' in member
