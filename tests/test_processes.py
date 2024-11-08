import pytest
from Controller.processes import get_processes, get_process

def test_get_processes():
    processes = get_processes(10).json()
    assert isinstance(processes, list)
    if processes:
        first_process = processes[0]
        assert isinstance(first_process['term'], int)
        assert isinstance(first_process['title'], str)
        if 'description' in first_process:
            assert isinstance(first_process['description'], str)

def test_get_process():
    # Using a known print number as example
    process = get_process(10, "1").json()
    assert isinstance(process, dict)
    assert isinstance(process['term'], int)
    assert isinstance(process['title'], str)

def test_process_response_fields():
    processes = get_processes(10).json()
    if processes:
        process = processes[0]
        assert 'term' in process
        assert 'number' in process
        assert 'title' in process
        assert 'documentDate' in process
        if 'stages' in process:
            assert isinstance(process['stages'], list)
    else:
        pytest.skip("get_processes returned no processes")

def test_process_details():
    process = get_process(10, "1").json()
    assert 'term' in process
    assert 'number' in process
    assert 'title' in process
    if 'stages' in process:
        assert isinstance(process['stages'], list)
        if process['stages']:
            stage = process['stages'][0]
            assert 'stageName' in stage
            assert 'date' in stage
