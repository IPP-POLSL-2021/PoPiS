import requests

def get_groups(term):
    """Returns a list of bilateral groups."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/bilateralGroups')
    return response

def get_group(term, id):
    """Returns a group's details."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/bilateralGroups/{id}')
    return response

if __name__ == "__main__":
    # Example usage
    groups = get_groups(10).json()
    if groups:
        print(f"First group name: {groups[0]['name']}")
        if 'engName' in groups[0]:
            print(f"English name: {groups[0]['engName']}")
