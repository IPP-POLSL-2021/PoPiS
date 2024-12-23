import requests
from typing import Dict, List, Optional, Union
import datetime
from functools import wraps


def get_votings(term: int) -> Dict:
    """
    Returns number of votings for each day in a given term.

    Args:
        term (int): The Sejm term number

    Returns:
        Dict: A dictionary of voting information for each day
    """
    return requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/votings')


def get_vote(term: int, sitting: int, id: int) -> requests.Response:
    """
    Retrieve details of a specific voting.

    Args:
        term (int): The Sejm term number
        sitting (int): The sitting number
        id (int): The voting ID

    Returns:
        requests.Response: Response containing voting details
    """
    response = requests.get(
        f'https://api.sejm.gov.pl/sejm/term{term}/votings/{sitting}/{id}')
    return response


def handle_response(func):
    """
    Decorator to handle response retrieval and error checking for voting-related functions.

    Args:
        func (callable): The function to be wrapped

    Returns:
        callable: Wrapped function with response handling
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = kwargs.get('response')

        # If response is not provided, try extracting term, sitting, and id from args or kwargs
        if not response:
            if len(args) >= 3:
                term, sitting, id = args[:3]  # Positional arguments
            else:
                term = kwargs.get('term')
                sitting = kwargs.get('sitting')
                id = kwargs.get('id')

            # Ensure term, sitting, and id are provided
            if term is None or sitting is None or id is None:
                raise ValueError(
                    "Provide term, sitting, and id when response is not given")

            # Fetch the response
            response = get_vote(term, sitting, id)
            kwargs['response'] = response

        # Call the wrapped function with response
        return func(*args, **kwargs)

    return wrapper


def search_votings(term: int, **params) -> List[Dict]:
    """
    Search for votings with various filters.

    Args:
        term (int): The Sejm term number
        **params: Optional search parameters like:
            - dateFrom: start date
            - dateTo: end date
            - limit: max results
            - offset: starting point
            - proceeding: specific proceeding number
            - title: search by title

    Returns:
        List[Dict]: A list of votings matching the search criteria
    """
    return requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/votings/search', params=params)


def get_proceeding_votings(term: int, proceeding: int) -> List[Dict]:
    """
    Returns a list of votings for a given proceeding.

    Args:
        term (int): The Sejm term number
        proceeding (int): The proceeding number

    Returns:
        List[Dict]: A list of votings for the specified proceeding
    """
    return requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/votings/{proceeding}')


def get_voting_details(term: int, proceeding: int, num: int) -> Dict:
    """
    Returns comprehensive details about a specific voting.

    Args:
        term (int): The Sejm term number
        proceeding (int): The proceeding number
        num (int): The voting number

    Returns:
        Dict: Detailed information about the voting
    """
    response = requests.get(
        f'https://api.sejm.gov.pl/sejm/term{term}/votings/{proceeding}/{num}')
    return response


def get_mp_voting_details(term: int, mp_id: int, sitting: int, date: str) -> List[Dict]:
    """
    Returns voting details for a specific MP on a given date.

    Args:
        term (int): The Sejm term number
        mp_id (int): The MP's ID
        sitting (int): The sitting number
        date (str): The date of voting (YYYY-MM-DD format)

    Returns:
        List[Dict]: Voting details for the specified MP
    """
    response = requests.get(
        f'https://api.sejm.gov.pl/sejm/term{term}/MP/{mp_id}/votings/{sitting}/{date}')
    return response


@handle_response
def get_date(term: Optional[int] = None, sitting: Optional[int] = None,
             id: Optional[int] = None, response: Optional[requests.Response] = None) -> datetime.datetime:
    """
    Extract the date of a specific voting.

    Args:
        term (int, optional): The Sejm term number
        sitting (int, optional): The sitting number
        id (int, optional): The voting ID
        response (requests.Response, optional): Pre-fetched response

    Returns:
        datetime.datetime: Date of the voting
    """
    return datetime.datetime.strptime(response.json()['date'], '%Y-%m-%dT%H:%M:%S')


@handle_response
def get_votes_with_mode(term: Optional[int] = None, sitting: Optional[int] = None,
                        id: Optional[int] = None, mode: Optional[Union[str, int]] = None,
                        response: Optional[requests.Response] = None) -> Union[int, str]:
    """
    Retrieve voting results based on a specified mode.

    Args:
        term (int, optional): The Sejm term number
        sitting (int, optional): The sitting number
        id (int, optional): The voting ID
        mode (str or int, optional): Mode of vote retrieval
        response (requests.Response, optional): Pre-fetched response

    Returns:
        int or str: Voting results based on the specified mode
    """
    vote_data = response.json()

    vote_modes = {
        "yes": ["yes", 0, "za"],
        "no": ["no", 1, "przeciw"],
        "abstain": ["abstain", 2, "wstrzymał"],
        "notParticipating": ["notParticipating", 3, "nieobecni"],
        "totalVoted": ["totalVoted", 4, "suma"]
    }

    # Normalize mode to a standard key
    normalized_mode = next(
        (key for key, values in vote_modes.items() if mode in values), mode)

    if normalized_mode in vote_modes or normalized_mode is None:
        if normalized_mode is None:
            return f"{vote_data['yes']} - {vote_data['no']} - {vote_data['abstain']} - {vote_data['notParticipating']}"
        return vote_data[normalized_mode]

    raise ValueError(f"Invalid mode: {mode}")


@handle_response
def get_info(term: Optional[int] = None, sitting: Optional[int] = None,
             id: Optional[int] = None, mode: Optional[Union[str, int]] = None,
             response: Optional[requests.Response] = None) -> str:
    """
    Retrieve specific information about a voting.

    Args:
        term (int, optional): The Sejm term number
        sitting (int, optional): The sitting number
        id (int, optional): The voting ID
        mode (str or int, optional): Type of information to retrieve
        response (requests.Response, optional): Pre-fetched response

    Returns:
        str: Requested voting information
    """
    info_modes = {
        "votingNumber": ["votingNumber", 0, "nr_głosowania"],
        "sitting": ["sitting", 1, "nr_posiedzenia"],
        "title": ["title", 2, "punkt_obrad"],
        "topic": ["topic", 3, "przedmiot"],
        "kind": ["kind", 4, "typ"]
    }

    # Normalize mode to a standard key
    normalized_mode = next(
        (key for key, values in info_modes.items() if mode in values), mode)

    if normalized_mode in info_modes:
        return response.json()[normalized_mode]

    raise ValueError(f"Invalid mode: {mode}")


def analyze_voting_results(voting_details: Dict) -> Dict:
    """
    Provides an analysis of voting results.

    Args:
        voting_details (Dict): Voting details from get_voting_details()

    Returns:
        Dict: Comprehensive voting analysis
    """
    total_votes = voting_details.get('totalVoted', 0)
    yes_votes = voting_details.get('yes', 0)
    no_votes = voting_details.get('no', 0)
    abstain_votes = voting_details.get('abstain', 0)
    not_participating = voting_details.get('notParticipating', 0)

    return {
        'total_votes': total_votes,
        'yes_percentage': round(yes_votes / total_votes * 100, 2) if total_votes > 0 else 0,
        'no_percentage': round(no_votes / total_votes * 100, 2) if total_votes > 0 else 0,
        'abstain_percentage': round(abstain_votes / total_votes * 100, 2) if total_votes > 0 else 0,
        'not_participating_percentage': round(not_participating / total_votes * 100, 2) if total_votes > 0 else 0,
        'voting_kind': voting_details.get('kind', 'Unknown'),
        'voting_title': voting_details.get('title', 'No title'),
        'voting_topic': voting_details.get('topic', 'No topic')
    }


def group_votes_by_club(voting_details: Dict) -> Dict[str, Dict]:
    """
    Groups voting results by parliamentary club.

    Args:
        voting_details (Dict): Voting details from get_voting_details()

    Returns:
        Dict[str, Dict]: Voting breakdown by parliamentary club
    """
    club_votes = {}

    # Normalize vote types to match test expectations
    vote_type_map = {
        'za': 'yes',
        'przeciw': 'no',
        'wstrzymał się': 'abstain',
        'nieobecny': 'not_voting'
    }

    # Handle case where voting_details might be a response object
    if hasattr(voting_details, 'json'):
        voting_details = voting_details.json()

    # Use .get() with a default empty list to prevent KeyError
    for vote in voting_details.get('votes', voting_details.get('vote', [])):
        # Use .get() with defaults to handle missing keys
        club = vote.get('club', 'Unknown')
        raw_vote_type = vote.get('vote', 'Unknown').lower()

        # Normalize vote type
        vote_type = vote_type_map.get(raw_vote_type, raw_vote_type)

        # Initialize club entry if not exists
        if club not in club_votes:
            club_votes[club] = {
                'yes': 0, 'no': 0, 'abstain': 0, 'not_voting': 0
            }

        # Increment vote count, defaulting to 'not_voting' if unknown
        club_votes[club][vote_type] = club_votes[club].get(vote_type, 0) + 1

    return club_votes


if __name__ == "__main__":
    # Example usage
    term = 10
    proceeding = 1
    voting_num = 3

    # Get voting details
    voting_details = get_voting_details(term, proceeding, voting_num).json()

    # Analyze voting results
    voting_analysis = analyze_voting_results(voting_details)
    print("Voting Analysis:")
    for key, value in voting_analysis.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

    # Group votes by club
    club_votes = group_votes_by_club(voting_details)
    print("\nVoting Breakdown by Club:")
    for club, votes in club_votes.items():
        print(f"{club}:")
        for vote_type, count in votes.items():
            if count > 0:
                print(f"  {vote_type.title()}: {count}")


def clubs_votes(term: int, proceedingNum: int, voteNum: int, MPslist: dict):
    votesLists = requests.get(
        f"https://api.sejm.gov.pl/sejm/term{term}/votings/{proceedingNum}/{voteNum}").json()
    clubVoteDict = {}
    for element in MPslist:
        if element["club"] not in clubVoteDict:
            clubVoteDict["club"] = {}

    return
