import requests

def get_prints(term):
    """Returns a list of prints for a given term."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/prints')
    return response

def get_print(term, num):
    """Returns information about a specific print."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/prints/{num}')
    return response

def get_print_attachment(term, num, attach_name):
    """Returns a print attachment."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/prints/{num}/{attach_name}')
    return response.content

if __name__ == "__main__":
    # Example usage
    prints = get_prints(10).json()
    if prints:
        print(f"First print title: {prints[0]['title']}")
