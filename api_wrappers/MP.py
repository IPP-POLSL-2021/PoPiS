# Maybe some more showing in if name == main or professional pytest testing
# Or type hints for functions, or comments directly next to function name so vscode nicely displays
# Or work on displaying photos of MP (simple as st.image(f"https://api.sejm.gov.pl/sejm/term{term}/MP/{id}/photo"))
import requests
import datetime
from functools import wraps

def get_MPs(term):
    """
    Fetches a list of Members of Parliament (MPs) for a given term.

    Parameters:
    term (int): The term number of the parliament.

    Returns:
    Response: The HTTP response object containing the MPs' data.
    """
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/MP')
    return response


def get_MP(term, id):
    """
    Fetches information about a Member of Parliament (MP) for a given term and ID.

    Parameters:
    term (int): The term number of the parliament.
    id (str): The unique identifier of the MP.

    Returns:
    Response: The HTTP response object containing the MP's data.
    """
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/MP/{id}')
    return response

# Enable supplying just response or full parameters
def handle_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = kwargs.get('response')

        # If response is not provided, try extracting term, sitting, and id from args or kwargs
        if not response:
            if len(args) >= 2:
                term, id = args[:2]  # Positional arguments
            else:
                term = kwargs.get('term')
                id = kwargs.get('id')
            
            # Ensure term, sitting, and id are provided
            if term is None or id is None:
                raise ValueError("Provide term and id when response is not given")
            
            # Fetch the response
            response = get_MP(term,id)
            kwargs['response'] = response

        # Call the wrapped function with response
        return func(*args, **kwargs)
    
    return wrapper

@handle_response    
def get_name(term=None, id=None, response=False):
    return response.json()['firstLastName']

# Returns a boolean value
@handle_response
def get_status(term=None, id=None, response=False):
    if not response:
        response = get_MP(term,id)
    return response.json()['active']

@handle_response
def get_reason(term=None, id=None, response=False):
    if response.json()['active']:
        return "None - MP is currently active"
    return response.json()['inactiveCause'] + " z powodu " + response.json()['waiverDesc']

@handle_response
def get_club(term=None, id=None, response=False):
    return response.json()['club']

#district_num :  A district id where MP was elected Example: 29.
#district_name : A district name where MP was elected Example: Katowice.
#voivodeship :   A voivodeship where MP was elected Example: śląskie.
@handle_response
def get_district(term=None, id=None, mode=None, response=False):
    match mode:
        case "district_num" | 0 | "numer":
            return response.json()['districtNum']
        case "district_name" | 1 | "nazwa":
            return response.json()['districtName']
        case "voivodeship" | 2 | "województwo":
            return response.json()['voivodeship']
        case _:
            raise Exception("Mode must be specified")
            #return response.json()['districtNum'] + " - " + response.json()['districtName'] + " - " + response.json()['voivodeship']

@handle_response
def get_photo(term, id, response=False):
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/MP/{id}/photo')

#birth_date (str --> datetime.date): a date of birth Example: 1985-04-14.
#birth_location (str): a place of birth Example: Gliwice.
#profession (str): a profession Example: przedsiębiorca prywatny.
#education_level (str): an education level Example: wyższe.
#number_of_votes (int): a number of votes Example: 19430.
@handle_response
def get_other(term=None, id=None, mode=None, response=False):
    match mode:
        case 'birth_date' | 0 | 'data_urodzenia':
            return datetime.datetime.strptime(response.json()['birthDate'], '%Y-%m-%d').date()
        case 'birth_location' | 1 | 'miejsce_urodzenia':
            return response.json()['birthLocation']
        case 'profession' | 2 | 'zawód':
            return response.json()['profession']
        case 'education_level' | 3 | 'wykształcenie':
            return response.json()['educationLevel']
        case 'number_of_votes' | 4 | 'liczba_głosów':
            return response.json()['numberOfVotes']
        case _:
            raise Exception("Mode must be specified")

# New function to get MP votings
def get_mp_votings(term, id, sitting, date):
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/MP/{id}/votings/{sitting}/{date}')
    return response.json()

# New functions to get MP photos
def get_mp_photo(term, id):
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/MP/{id}/photo')
    return response.content

def get_mp_photo_mini(term, id):
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/MP/{id}/photo-mini')
    return response.content


if __name__ == "__main__":
    # Zwykły - Zrzeczenie - Zgon
    IDs = ['241', '8', '244']
    # print(get_MP(10,241).json())
    for i in IDs:
        response = get_MP(10,i)
        print(get_name(response=response), get_status(response=response), get_reason(response=response), get_district(mode='district_num', response=response), get_district(mode=1, response=response), get_district(mode='województwo', response=response), get_club(response=response))
    
    print("========= INNE ========")
    for i in IDs:
        response = get_MP(10,i)
        print(response.json()['id'])
        for j in range(1,5):
            data = get_other(mode=j, response=response)
            print(data, end=" ")
        print("")

# TODO
# Part of result from term10/MP/1/votings/18/2024-09-25
# All of votings of given MP (in this case 1) on 18 sitting and 2024-09-2025
example = {
    "date": "2024-09-25T10:12:53",
    "kind": "ELECTRONIC",
    "title": "18. posiedzenie Sejmu Rzeczypospolitej Polskiej w dniach 25, 26 i 27 września oraz 1 października 2024 r.",
    "topic": "wniosek o skrócenie terminu, o którym mowa w art. 37 ust. 4 regulaminu Sejmu",
    "vote": "YES",
    "votingNumber": 1
  },
{
    "date": "2024-09-25T10:14:01",
    "kind": "ELECTRONIC",
    "title": "18. posiedzenie Sejmu Rzeczypospolitej Polskiej w dniach 25, 26 i 27 września oraz 1 października 2024 r.",
    "topic": "wniosek o skrócenie terminu, o którym mowa w art. 37 ust. 4 regulaminu Sejmu",
    "vote": "YES",
    "votingNumber": 2
  },