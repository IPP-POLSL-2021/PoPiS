import requests

from datetime import datetime, timedelta
from Controller import MP
import pandas as pd


def CommiteesList(term):
    response_API = requests.get(
        f'https://api.sejm.gov.pl/sejm/term{term}/committees')
    # print(response_API.status_code)
    # print(f'https://api.sejm.gov.pl/sejm/term{term}/committees')
    commitees = response_API.json()
    # print(commitees)
    return commitees


def CommiteeFutureSetting(term, code):

    response_API = requests.get(
        f'https://api.sejm.gov.pl/sejm/term{term}/committees/{code}/sittings')
    # print(f'https://api.sejm.gov.pl/sejm/term{term}/committees/{code}')
    if response_API.status_code != 200:
        date = " wystąpił bład"
        return date
    committee = response_API.json()
    for setting in committee:
        # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        # print(setting)

        # print(setting['date'])
        date = datetime.strptime(setting['date'], '%Y-%m-%d').date()
        print(date)
        today = datetime.today().date()-timedelta(4)
        if date >= today:
            return date


def LastNCommitteeSettingDates(committeeCode, numebrOfSitting, term):
    response_API = requests.get(
        f'https://api.sejm.gov.pl/sejm/term{term}/committees/{committeeCode}/sittings')
    if response_API.status_code != 200:
        return "coś poszło nie tak"
    committee = response_API.json()
    settingsCounter = 0
    datesList = []
    for setting in reversed(committee):
        datesList.append(setting['date'])
        settingsCounter += 1
        if settingsCounter >= numebrOfSitting:
            return datesList
    return datesList


def ComitteStats(term, code=None):
    if code == None or code == "łącznie":
        API = f'https://api.sejm.gov.pl/sejm/term{term}/committees'
    else:
        API = f'https://api.sejm.gov.pl/sejm/term{term}/committees/{code}'
    response = requests.get(API)
    API_data = response.json()
    clubs = {}
    peoples = {}
    if code is None or code == "łącznie":
        for obj in API_data:
            for member in obj['members']:
                if member['lastFirstName'] in peoples:
                    peoples[member['lastFirstName']] += 1
                else:
                    peoples[member['lastFirstName']] = 1
                    if member['club'] in clubs:
                        clubs[member['club']].append(member['lastFirstName'])
                    else:
                        clubs[member['club']] = [member['lastFirstName']]
    else:
        for member in API_data['members']:
            if member['lastFirstName'] in peoples:
                peoples[member['lastFirstName']] += 1
            else:
                peoples[member['lastFirstName']] = 1
                if member['club'] in clubs:
                    clubs[member['club']].append(member['lastFirstName'])
                else:
                    clubs[member['club']] = [member['lastFirstName']]
    ClubsDataframe = pd.DataFrame.from_dict(clubs, orient='index')
    MPsDataframe = pd.DataFrame.from_dict(peoples, orient='index')
    return ClubsDataframe, MPsDataframe


def CommitteeAge(committee, term=10):
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/MP')
    MPs = response.json()
    current_time = datetime.now().replace(microsecond=0, second=0, minute=0, hour=0)
    MPsAge = {}
    for patry in committee:
        # print(patry)
        ages = []
        for person in committee[patry]:
            # print(person)
            filtered_MPs = [
                mp for mp in MPs if mp['lastFirstName'] == person]
            # dateOfBirth = [mp['birthDate'] for mp in filtered_MPs]
            dateOfBirth = [datetime.strptime(
                mp['birthDate'], '%Y-%m-%d').date() for mp in filtered_MPs]
            ageOfMP = current_time.date()-dateOfBirth.date()
            ages.append(ageOfMP)

        MPsAge[patry] = ages
        # MPsAge.append()
        #
    agesDataFrame = pd.DataFrame(MPsAge)

    return agesDataFrame
    # do zrobienia uzyskać pełną liczbe posło to w zmiennej a następnie poporstu szukać konkretnych
    # print(MP.get_MP_ID(10, person))
    # for MP in patry:
