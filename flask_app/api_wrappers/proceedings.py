import requests

def get_proceedings(term):
    """Returns a list of proceedings."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/proceedings')
    return response

def get_proceeding(term, id):
    """Returns information about a proceeding."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/proceedings/{id}')
    return response

if __name__ == "__main__":
    # Example usage
    proceedings = get_proceedings(10).json()
    if proceedings:
        print(f"First proceeding title: {proceedings[0]['title']}")
        if 'dates' in proceedings[0]:
            print(f"Dates: {', '.join(proceedings[0]['dates'])}")
