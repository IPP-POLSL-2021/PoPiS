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
        date = datetime.strptime(setting['date'], '%Y-%m-%d')
        today = datetime.today()
        if date > today:
            return date
