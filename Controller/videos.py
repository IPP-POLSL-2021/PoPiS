import requests
from datetime import datetime

def get_videos(term, **params):
    """Returns a list of video transmissions with optional filters."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/videos', params=params)
    return response

def get_today_videos(term):
    """Returns a list of video transmissions for today."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/videos/today')
    return response

def get_date_videos(term, date):
    """Returns a list of video transmissions for a specified date."""
    if isinstance(date, datetime):
        date = date.strftime('%Y-%m-%d')
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/videos/{date}')
    return response

def get_video(term, unid):
    """Returns a video transmission details."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/videos/{unid}')
    return response

if __name__ == "__main__":
    # Example usage
    today_videos = get_today_videos(10).json()
    if today_videos:
        print("Today's transmissions:")
        for video in today_videos:
            print(f"Title: {video['title']}")
            if 'startDateTime' in video:
                print(f"Start time: {video['startDateTime']}")
