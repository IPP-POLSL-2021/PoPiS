import requests

from datetime import datetime, timedelta
# Nie korzystasz z tego i tak
#from Controller import MP
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
    ClubsNonDataframe = clubs
    return ClubsDataframe, MPsDataframe, ClubsNonDataframe


def ComitteEducation(commitee, term=10, searchedInfo='edukacja'):
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/MP')
    MPs = response.json()
    MPsEducation = {}

    for party in commitee:
        educations = {}
        for person in commitee[party]:

            filtered_MPs = [
                mp for mp in MPs if mp['lastFirstName'] == person]
            # dateOfBirth = [mp['birthDate'] for mp in filtered_MPs]
            if filtered_MPs:
                # print(filtered_MPs)
                educationOfMP = ""
                match searchedInfo:
                    case 'edukacja':
                        educationOfMP = str([
                            mp['educationLevel'] for mp in filtered_MPs])
                    case 'okrąg':
                        educationOfMP = str([
                            mp['districtName'] for mp in filtered_MPs])
                    case 'profesja':

                        educationOfMP = str(
                            [mp['profession'] for mp in filtered_MPs if 'profession' in mp])
                    # case 'województwo':
                    #     educationOfMP = str([
                    #         mp['voivodeship'] for mp in filtered_MPs])
                educationOfMP = educationOfMP.strip("[]'")

                if educationOfMP in educations:
                    educations[educationOfMP] += 1
                else:
                    educations[educationOfMP] = 1
        MPsEducation[party] = educations
    return MPsEducation


def CommitteeAge(committee, term=10, searchedInfo='birthDate'):
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/MP')
    MPs = response.json()
    current_time = datetime.now().replace(microsecond=0, second=0, minute=0, hour=0)
    if term != 10:
        termResponse = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}')
        termInfo = termResponse.json()
        endOfTerm = termInfo['to']
        current_time = datetime.strptime(endOfTerm, "%Y-%m-%d")
    # print(current_time)
    MPsAge = {}
    # print(committee)
    # print(committee.to_dict)
    # committee = committee.to_dict(orient="list")
    # print(committee)
    searchedData = f'{searchedInfo}'
    for patry in committee:
        # print(committee[patry])
        ages = []

        # print(patry)
        for person in committee[patry]:
            # print(person)
            filtered_MPs = [
                mp for mp in MPs if mp['lastFirstName'] == person]
            dateOfBirth = str([
                mp[searchedData] for mp in filtered_MPs])
            # print(datetime.strptime(str(dateOfBirth[0]), '%Y-%m-%d').date())
            dateOfBirth = dateOfBirth.strip("[]'")
            # print(dateOfBirth)
            # print("=================")

            ageOfMP = current_time.date() - \
                datetime.strptime(dateOfBirth, "%Y-%m-%d").date()

            ageOfMP = ageOfMP.days/365
            # if ageOfMP > maxMPsAge:
            #     maxMPsAge = ageOfMP
            # MaxMinMP[0]=
            ages.append(round(ageOfMP))

        MPsAge[patry] = ages
        # MPsAge.append()
        # print(MPsAge)
    agesDataFrame = pd.DataFrame.from_dict(MPsAge, orient='index')

    # agesDataFrame = pd.DataFrame(MPsAge)
    # print(agesDataFrame)
    return agesDataFrame, MPsAge
    # do zrobienia uzyskać pełną liczbe posło to w zmiennej a następnie poporstu szukać konkretnych
    # print(MP.get_MP_ID(10, person))
    # for MP in patry:
