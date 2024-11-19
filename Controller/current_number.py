import requests


def get_term_number():
    """
    Retrieve the latest term number for the Polish Sejm.

    Returns:
        int: The current term number.
    """
    for i in requests.get(f'https://api.sejm.gov.pl/sejm/term').json():
       if i['current']:
           return i['num']
    # term = current_term_number
    # while True:
    #     try:
    #         response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}', timeout=5)
    #         if response.status_code != 200:
    #             return term - 1
    #         term += 1
    #     except requests.RequestException:
    #         return term - 1


def get_sitting_number(term=0):
    """
    Retrieve the latest sitting number for a given term.
    
    Args:
        term (int, optional): Term number to check. Defaults to 0 which triggers get_term_number().
    Returns:
        int: The latest sitting number of the term.
    """
    current_sitting_number = 1
    if term==0:
        term = get_term_number()
    for i in requests.get(f"https://api.sejm.gov.pl/sejm/term{term}/proceedings/").json():
        if i['number']>current_sitting_number:
            current_sitting_number = i['number']
    return current_sitting_number

    # sitting = current_sitting_number
    # while True:
    #     response = requests.get(
    #         f'https://api.sejm.gov.pl/sejm/term{term}/proceedings/{sitting}')
    #     if response.status_code != 200:
    #         return sitting - 1
    #     sitting += 1


def get_voting_number(term=0, sitting=0):
    """
    Retrieve the latest voting number for a given term and sitting.
    
    Args:
        term (int, optional): Term number to check. Defaults to 0 which triggers get_term_number().
        sitting (int, optional): Sitting number to check. Defaults to 0 which triggers get_sitting_number(term).
    Returns:
        int: The latest voting number of given term and sitting.
    """
    if term==0:
        term = get_term_number()
    if sitting==0:
        sitting = get_sitting_number(term)
    return len(requests.get(f"https://api.sejm.gov.pl/sejm/term{term}/votings/{sitting}").json())
    #voting = current_voting_number
    #while True:
    #    response = requests.get(
    #        f"https://api.sejm.gov.pl/sejm/term{term}/votings/{sitting}/{voting}")
    #    if response.status_code != 200:
    #        voting = voting - 1
    #        return voting
    #    voting += 1
if __name__ == "__main__":
    term_number = get_term_number()
    sitting_number = get_sitting_number(term_number)
    voting_number = get_voting_number(term_number, sitting_number)
    if voting_number == 0:
        sitting_number = sitting_number-1
        voting_number = get_voting_number(term_number,sitting_number)
    print(
        f"Voting No. {voting_number} during the {sitting_number} session of the {term_number}th term of the Sejm"
    )
