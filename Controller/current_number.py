import requests


def get_term_number(current_term_number=10):
    """
    Retrieve the latest term number for the Polish Sejm.
    
    Args:
        current_term_number (int, optional): Starting term number to check. Defaults to 10.
    
    Returns:
        int: The latest term number found.
    """
    term = current_term_number
    while True:
        try:
            response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}', timeout=5)
            if response.status_code != 200:
                return term - 1
            term += 1
        except requests.RequestException:
            return term - 1


def get_sitting_number(term=None, current_sitting_number=16):
    """
    Retrieve the latest sitting number for a given term.
    
    Args:
        term (int, optional): Term number to check. Defaults to the latest term.
        current_sitting_number (int, optional): Starting sitting number to check. Defaults to 16.
    
    Returns:
        int: The latest sitting number found.
    """
    if term is None:
        term = get_term_number()
    
    sitting = current_sitting_number
    while True:
        try:
            response = requests.get(
                f'https://api.sejm.gov.pl/sejm/term{term}/proceedings/{sitting}', 
                timeout=5
            )
            if response.status_code != 200:
                return sitting - 1
            sitting += 1
        except requests.RequestException:
            return sitting - 1


def get_voting_number(term=None, sitting=None, current_voting_number=1):
    """
    Retrieve the latest voting number for a given term and sitting.
    
    Args:
        term (int, optional): Term number to check. Defaults to the latest term.
        sitting (int, optional): Sitting number to check. Defaults to the latest sitting.
        current_voting_number (int, optional): Starting voting number to check. Defaults to 85.
    
    Returns:
        int: The latest voting number found.
    """
    if term is None:
        term = get_term_number()
    if sitting is None:
        sitting = get_sitting_number(term)
    
    voting = current_voting_number
    while True:
        try:
            response = requests.get(
                f"https://api.sejm.gov.pl/sejm/term{term}/votings/{sitting}/{voting}", 
                timeout=5
            )
            if response.status_code != 200:
                return voting - 1
            voting += 1
        except requests.RequestException:
            return voting - 1


if __name__ == "__main__":
    term_number = get_term_number()
    sitting_number = get_sitting_number(term_number)
    voting_number = get_voting_number(term_number, sitting_number)
    print(
        f"Voting No. {voting_number} during the {sitting_number} session of the {term_number}th term of the Sejm"
    )
