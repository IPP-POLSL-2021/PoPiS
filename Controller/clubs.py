import requests

def get_clubs(term):
    """Returns a list of clubs for a given term."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/clubs')
    return response

def get_club(term, id):
    """Returns information about a specific club."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/clubs/{id}')
    return response

def get_club_logo(term, id):
    """Returns a club's logo image."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/clubs/{id}/logo')
    return response.content

if __name__ == "__main__":
    # Example usage
    clubs = get_clubs(10)
    print("List of clubs:")
    for club in clubs:
        print(f"Name: {club['name']}, Members: {club['membersCount']}")
