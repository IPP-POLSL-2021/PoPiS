import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Union, Tuple, Optional


def get_committees(term: int) -> List[Dict]:
    """Retrieve the list of committees for a given term."""
    response = requests.get(
        f'https://api.sejm.gov.pl/sejm/term{term}/committees')
    return response.json()


def get_committee_future_sitting(term: int, code: str) -> Optional[datetime.date]:
    """Find the next future sitting date for a specific committee."""
    response = requests.get(
        f'https://api.sejm.gov.pl/sejm/term{term}/committees/{code}/sittings')

    if response.status_code != 200:
        return " wystąpił bład"

    committee = response.json()
    for setting in committee:
        date = datetime.strptime(setting['date'], '%Y-%m-%d').date()
        print(date)
        today = datetime.today().date() - timedelta(4)
        if date >= today:
            return date

    return None


def get_last_n_committee_sitting_dates(committeeCode: str, numberOfSitting: int, term: int) -> Union[List[str], str]:
    """Retrieve the last N sitting dates for a specific committee."""
    response = requests.get(
        f'https://api.sejm.gov.pl/sejm/term{term}/committees/{committeeCode}/sittings')

    if response.status_code != 200:
        return "coś poszło nie tak"

    committee = response.json()
    settingsCounter = 0
    datesList = []

    for setting in reversed(committee):
        datesList.append(setting['date'])
        settingsCounter += 1
        if settingsCounter >= numberOfSitting:
            return datesList

    return datesList


def get_committee_stats(term: int, code: Optional[str] = None) -> Dict[str, Union[Dict[str, List[str]], Dict[str, int]]]:
    """Retrieve statistics about committee members."""
    if code is None or code == "łącznie":
        API = f'https://api.sejm.gov.pl/sejm/term{term}/committees'
        response = requests.get(API)
        API_data = response.json()

        # Use sets to prevent duplicates in clubs
        unique_members = set()
        clubs: Dict[str, List[str]] = {}
        peoples: Dict[str, int] = {}

        # Aggregate unique members from all committees
        for committee in API_data:
            for member in committee['members']:
                # Add to clubs (prevent duplicates in club list)
                if member['club'] not in clubs:
                    clubs[member['club']] = []
                if member['lastFirstName'] not in clubs[member['club']]:
                    clubs[member['club']].append(member['lastFirstName'])

                # Count committees per MP (allow multiple counts)
                peoples[member['lastFirstName']] = peoples.get(
                    member['lastFirstName'], 0) + 1
    else:
        API = f'https://api.sejm.gov.pl/sejm/term{term}/committees/{code}'
        response = requests.get(API)
        API_data = response.json()

        clubs: Dict[str, List[str]] = {}
        peoples: Dict[str, int] = {}

        for member in API_data['members']:
            if member['club'] not in clubs:
                clubs[member['club']] = []
            clubs[member['club']].append(member['lastFirstName'])

            peoples[member['lastFirstName']] = peoples.get(
                member['lastFirstName'], 0) + 1

    return {
        'clubs': clubs,
        'members': peoples
    }


def get_committee_member_details(committee: Dict[str, List[str]], term: int = 10, searchedInfo: str = 'edukacja') -> Dict[str, Dict[str, int]]:
    """Retrieve detailed information about committee members."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/MP')
    MPs = response.json()
    MPsEducation: Dict[str, Dict[str, int]] = {}

    for party, members in committee.items():
        educations: Dict[str, int] = {}
        for person in members:
            filtered_MPs = [mp for mp in MPs if mp['lastFirstName'] == person]

            if filtered_MPs:
                educationOfMP = ""
                match searchedInfo:
                    case 'edukacja':
                        educationOfMP = str([mp['educationLevel']
                                            for mp in filtered_MPs])
                    case 'okrąg':
                        educationOfMP = str([mp['districtName']
                                            for mp in filtered_MPs])
                    case 'profesja':
                        educationOfMP = str(
                            [mp['profession'] for mp in filtered_MPs if 'profession' in mp])

                educationOfMP = educationOfMP.strip("[]'")
                educations[educationOfMP] = educations.get(
                    educationOfMP, 0) + 1

        MPsEducation[party] = educations

    return MPsEducation


def get_committee_member_ages(committee: Dict[str, List[str]], term: int = 10, searchedInfo: str = 'birthDate') -> Tuple[pd.DataFrame, Dict[str, List[float]]]:
    """Calculate ages of committee members."""
    # print(f"get_committee_member_ages from committees.py the term number is {term}")
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/MP')
    MPs = response.json()

    current_time = datetime.now().replace(microsecond=0, second=0, minute=0, hour=0)

    if term != 10:
        termResponse = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}')
        termInfo = termResponse.json()
        endOfTerm = termInfo['to']
        current_time = datetime.strptime(endOfTerm, "%Y-%m-%d")

    MPsAge: Dict[str, List[float]] = {}

    for party, members in committee.items():
        ages: List[float] = []
        for person in members:
            filtered_MPs = [mp for mp in MPs if mp['lastFirstName'] == person]

            if filtered_MPs:
                dateOfBirth = str([mp[searchedInfo]
                                  for mp in filtered_MPs]).strip("[]'")

                ageOfMP = current_time.date() - datetime.strptime(dateOfBirth, "%Y-%m-%d").date()
                ages.append(int(ageOfMP.days/365))

        MPsAge[party] = ages

    agesDataFrame = pd.DataFrame.from_dict(MPsAge, orient='index')

    return agesDataFrame, MPsAge
