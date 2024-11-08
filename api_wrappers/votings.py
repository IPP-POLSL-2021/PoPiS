import requests

def get_votings(term):
    """Returns number of votings for each day."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/votings')
    return response

def search_votings(term, **params):
    """Search for votings with various filters."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/votings/search', params=params)
    return response

def get_proceeding_votings(term, proceeding):
    """Returns a list of votings for a given proceeding."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/votings/{proceeding}')
    return response

def get_voting_details(term, proceeding, num):
    """Returns details about a specific voting, including results."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/votings/{proceeding}/{num}')
    return response

if __name__ == "__main__":
    # Example usage with search parameters
    votings = search_votings(10, 
        dateFrom='2023-01-01',  # Start date
        dateTo='2023-12-31',    # End date
        limit=5,                # Limit results
        offset=0,               # Starting point
        proceeding=1,           # Specific proceeding
        title='energii'         # Title filter
    ).json()
    
    print("Votings:")
    for voting in votings:
        print(f"Title: {voting.get('title', 'N/A')}")
        print(f"Date: {voting.get('date', 'N/A')}")
        print("---")
