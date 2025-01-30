import requests

def get_terms():
    """Returns a list of terms."""
    response = requests.get('https://api.sejm.gov.pl/sejm/term')
    return response

def get_term(term):
    """Returns information about a specific term."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}')
    return response

if __name__ == "__main__":
    # Example usage
    terms = get_terms().json()
    if terms:
        current_term = next((term for term in terms if term.get('current')), None)
        if current_term:
            print(f"Current term: {current_term['num']}")
            print(f"Started: {current_term['from']}")
