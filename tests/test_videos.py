import pytest
from api_wrappers.videos import get_videos, get_today_videos, get_date_videos, get_video
from datetime import datetime

def test_get_videos():
    videos = get_videos(10).json()
    assert isinstance(videos, list)
    if videos:
        first_video = videos[0]
        assert isinstance(first_video['title'], str)
        assert isinstance(first_video['type'], str)
        if 'startDateTime' in first_video:
            assert isinstance(first_video['startDateTime'], str)

def test_get_today_videos():
    videos = get_today_videos(10).json()
    assert isinstance(videos, list)
    if videos:
        first_video = videos[0]
        assert isinstance(first_video['title'], str)
        assert isinstance(first_video['type'], str)

def test_get_date_videos():
    # Test with a specific date
    date = "2023-12-13"  # Example date
    videos = get_date_videos(10, date).json()
    assert isinstance(videos, list)
    if videos:
        first_video = videos[0]
        assert isinstance(first_video['title'], str)
        assert isinstance(first_video['type'], str)

def test_get_video():
    # Using a specific video ID as example
    # Note: You'll need to replace with a valid video ID
    unid = "2A8A86E819C2C270C1258ACB0047A157"
    video = get_video(10, unid).json()
    assert isinstance(video, dict)
    assert isinstance(video['title'], str)
    assert isinstance(video['type'], str)

def test_invalid_video():
    response = get_video(10, "INVALID_VIDEO_ID")
    assert response.status_code == 404

def test_video_response_fields():
    videos = get_videos(10).json()
    if videos:
        first_video = videos[0]
        assert 'title' in first_video
        assert 'type' in first_video
        assert 'unid' in first_video
        if 'startDateTime' in first_video:
            assert isinstance(first_video['startDateTime'], str)
        if 'endDateTime' in first_video:
            assert isinstance(first_video['endDateTime'], str)
    else:
        pytest.skip("get_videos returned an empty list")

def test_date_parameter_formats():
    # Test with datetime object
    date = datetime(2023, 12, 13)
    videos = get_date_videos(10, str(date.date())).json()
    assert isinstance(videos, list)

    # Test with string date
    videos = get_date_videos(10, "2023-12-13").json()
    assert isinstance(videos, list)
