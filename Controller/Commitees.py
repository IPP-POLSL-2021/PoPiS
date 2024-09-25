import requests

from datetime import datetime


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
    print(f'https://api.sejm.gov.pl/sejm/term{term}/committees/{code}')
    if response_API.status_code != 200:
        date = " wystąpił bład"
        return date
    committee = response_API.json()
    for setting in committee:
        # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(setting)

        print(setting['date'])
        date = datetime.strptime(setting['date'], '%Y-%m-%d').date()
        today = datetime.today().date()
        if date >= today:
            return date


def ComitteStats(term, code=None):
    if code == None:
        API = f'https://api.sejm.gov.pl/sejm/term{term}/committees'
    else:
        API = f'https://api.sejm.gov.pl/sejm/term{term}/committees/{code}'
    response = requests.get(API)
    API_data = response.json()
    clubs = {}
    peoples = {}
    if code is None:
        for obj in API_data:
            for member in obj['members']:
                if member['lastFirstName'] in peoples:
                    peoples[member['lastFirstName']] += 1
                else:
                    peoples[member['lastFirstName']] = 1
                    if member['club'] in clubs:
                        clubs[member['club']].append(member['lastFirstName'])
                    else:
                        clubs[member['club']] = member['lastFirstName']
    else:
        for member in API_data['members']:
            for member in obj['members']:
                if member['lastFirstName'] in peoples:
                    peoples[member['lastFirstName']] += 1
                else:
                    peoples[member['lastFirstName']] = 1
                    if member['club'] in clubs:
                        clubs[member['club']].append(member['lastFirstName'])
                    else:
                        clubs[member['club']] = member['lastFirstName']
    return clubs, peoples
