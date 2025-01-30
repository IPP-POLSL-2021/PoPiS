import requests
import datetime
try:
    # Importing get_name from MP module
    from api_wrappers.MP import get_name, get_club, get_photo, get_other
except ModuleNotFoundError:
    from MP import get_name, get_club, get_photo, get_other
from functools import wraps


def get_interpelations(term, **params):
    """Returns a list of interpellations with optional filters."""
    return requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/interpellations', params=params)


def get_interpelation(term, num):
    """Returns details of a specific interpellation."""
    return requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/interpellations/{num}')


def get_interpelation_body(term, num):
    """Returns an interpellation body in HTML format."""
    return requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/interpellations/{num}/body').text


def get_reply_body(term, num, key):
    """Returns a reply body in HTML format."""
    return requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/interpellations/{num}/reply/{key}/body').text

# Enable supplying just response or full parameters


def handle_response(func):
    """
    Decorator to handle the response for interpellation-related functions.

    This decorator allows functions to either receive a pre-fetched response
    or fetch the response internally using provided term and num parameters.

    Parameters:
    func (function): The function to be wrapped by the decorator.

    Returns:
    function: The wrapped function that ensures a response is available for processing.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = kwargs.get('response')

        # If response is not provided, try extracting term, sitting, and id from args or kwargs
        if not response:
            if len(args) >= 2:
                term, num = args[:2]  # Positional arguments
            else:
                term = kwargs.get('term')
                num = kwargs.get('num')

            # Ensure term, num are provided
            if term is None or num is None:
                raise ValueError(
                    "Provide term and num when response is not given")

            # Fetch the response
            response = get_interpelation(term, num)
            kwargs['response'] = response

        # Call the wrapped function with response
        return func(*args, **kwargs)

    return wrapper


@handle_response
def get_title(term=None, num=None, response=False):
    """Get the title of an interpellation."""
    return response.json()['title']

# receipt_date str --> datetime.date: A date when the case was received by Marshall Example: 2020-11-16.
# sent_date str --> datetime.date: A date when the interpellation was sent from Marshall to recipients Example: 2021-01-20.
# last_modified str --> datetime.datetime: A date of last modification of a document Example: 2022-09-07 15:01:42.


@handle_response
def get_date(term=None, num=None, mode=None, response=False):
    """Get various dates related to an interpellation."""
    match mode:
        case 'receipt_date' | 0 | 'data_otrzymania':
            return datetime.datetime.strptime(response.json()['receiptDate'], '%Y-%m-%d').date()
        case 'sent_date' | 1 | 'data_wysłania':
            if 'sentDate' in response.json():
                return datetime.datetime.strptime(response.json()['sentDate'], '%Y-%m-%d').date()
            else:
                return " "
        case 'last_modified' | 2 | 'czas_ostatniej_modyfikacji':
            return datetime.datetime.strptime(response.json()['lastModified'], '%Y-%m-%dT%H:%M:%S').date()


@handle_response
def get_authors(term=None, num=None, response=False):
    """
    Get the authors of an interpellation.

    Parameters:
    term (int, optional): The term of the parliament. Defaults to None.
    num (str, optional): The number of the interpellation. Defaults to None.
    response (requests.Response, optional): The response object containing interpellation data. Defaults to False.

    Returns:
    list: A list of tuples, each containing the name, club, photo URL, and other details of an author.
    """
    IDs = response.json()['from']
    if term == None:
        term = response.json()['term']
    return [(get_name(term, id), get_club(term, id), get_photo(term, id), get_other(term, id, mode=2)) for id in IDs]


@handle_response
def get_receipent(term=None, num=None, response=False):
    """Get the recipients of an interpellation."""
    return response.json()['to']


@handle_response
def get_replies(term, num, response=False):
    """
    Retrieve replies to a specific interpellation.

    Parameters:
    term (int): The term of the parliament.
    num (str): The number of the interpellation.
    response (requests.Response, optional): The response object containing interpellation data. Defaults to False.

    Returns:
    tuple: A tuple containing two lists:
        - file_urls (list): A list of URLs for any attachments in the replies.
        - htmls (list): A list of HTML links for the replies.
    """
    file_urls = []
    htmls = []

    for reply in response.json()['replies']:
        # Handle attachments
        try:
            file_urls.extend([j['URL'] for j in reply.get('attachments', [])])
        except KeyError:
            file_urls.append(None)

        try:
            htmls.append(reply['links'][1]['href'])
        except KeyError:
            htmls.append(None)

    return (file_urls, htmls)


@handle_response
def get_repeated_interpellations(term, num, response=False):
    """Get repeated interpellations (follow-up questions)."""
    return response.json().get('repeatedInterpellation', [])

# Additional utility functions


@handle_response
def is_repeated_interpellation(term, num, response=False):
    """Check if this is a repeated interpellation."""
    return len(response.json().get('repeatedInterpellation', [])) > 0


if __name__ == "__main__":
    # Example usage demonstrating various methods
    term = 10
    num = "3999"  # Example interpellation number

    print("Interpellation Details:")
    print(f"Title: {get_title(term, num)}")
    print(f"Receipt Date: {get_date(term, num, 'receipt_date')}")
    print(f"Sent Date: {get_date(term, num, 'sent_date')}")
    print(f"Authors: {get_authors(term, num)}")
    print(f"Recipients: {get_receipent(term, num)}")

    file_urls, htmls = get_replies(term, num)
    print(f"Reply File URLs: {file_urls}")
    print(f"Number of HTML Replies: {len(htmls)}")
