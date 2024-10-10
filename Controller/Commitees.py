import requests

from datetime import datetime, timedelta


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
    return clubs, peoples


def CommitteeAge(committee):
    for patry in committee:
        for MP in patry:
            print(MP)
