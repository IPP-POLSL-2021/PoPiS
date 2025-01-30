import requests

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
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/videos/{date}')
    return response

def get_video(term, unid):
    """Returns a video transmission details."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/videos/{unid}')
    return response

if __name__ == "__main__":
    # Example usage with various parameters
    videos = get_videos(10, 
        comm='SUE',  # Committee filter
        limit=5,     # Limit results
        offset=0,    # Starting point
        since='2023-01-01',  # Start date
        till='2023-12-31',   # End date
        title='kodeksu',     # Title filter
        type='komisja'       # Type filter
    ).json()
    
    print("Videos:")
    for video in videos:
        print(f"Title: {video.get('title', 'N/A')}")
        print(f"Start Time: {video.get('startDateTime', 'N/A')}")
        print("---")
