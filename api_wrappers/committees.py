import requests
from datetime import datetime, timedelta

def get_committees(term):
    """Returns a list of committees."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/committees')
    return response

def get_committee(term, code):
    """Returns details about a specific committee."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/committees/{code}')
    return response

def get_committee_sittings(term, code):
    """Returns a list of committee sittings."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/committees/{code}/sittings')
    return response

def get_committee_sitting(term, code, num):
    """Returns details about a specific committee sitting."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/committees/{code}/sittings/{num}')
    return response

def get_committee_sitting_html(term, code, num):
    """Returns transcript of the meeting in HTML format."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/committees/{code}/sittings/{num}/html')
    return response.text

def get_committee_sitting_pdf(term, code, num):
    """Returns transcript of the meeting in PDF format."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/committees/{code}/sittings/{num}/pdf')
    return response.content

# Preserving some custom functionality from the original Commitees.py
def find_next_committee_sitting(term, code):
    """Find the next committee sitting date."""
    try:
        sittings = get_committee_sittings(term, code).json()
        today = datetime.today().date() - timedelta(4)
        
        for sitting in sittings:
            date = datetime.strptime(sitting['date'], '%Y-%m-%d').date()
            if date >= today:
                return date
        return None
    except Exception:
        return "Error occurred while finding next sitting"

def get_committee_stats(term, code=None):
    """Get statistics about committee members."""
    try:
        if code is None or code == "łącznie":
            api_url = f'https://api.sejm.gov.pl/sejm/term{term}/committees'
        else:
            api_url = f'https://api.sejm.gov.pl/sejm/term{term}/committees/{code}'
        
        response = requests.get(api_url)
        data = response.json()
        
        clubs = {}
        peoples = {}
        
        members = data['members'] if code is not None else [member for committee in data for member in committee['members']]
        
        for member in members:
            # Count members by club
            if member['club'] in clubs:
                clubs[member['club']].append(member['lastFirstName'])
            else:
                clubs[member['club']] = [member['lastFirstName']]
            
            # Count individual member occurrences
            if member['lastFirstName'] in peoples:
                peoples[member['lastFirstName']] += 1
            else:
                peoples[member['lastFirstName']] = 1
        
        return clubs, peoples
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Example usage
    committees = get_committees(10).json()
    print("Committees:")
    for committee in committees:
        print(f"Name: {committee['name']}, Code: {committee['code']}")
