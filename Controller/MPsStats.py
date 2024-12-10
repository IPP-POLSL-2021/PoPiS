import requests
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from Model import MPModel


def groupMpsByClub(term):
    response = requests.get(f"https://api.sejm.gov.pl/sejm/term{term}/MP")
    MpsList = response.json()
    MpIdByClub = {}
    MpNamesByClub = {}
    for Mp in MpsList:
        if Mp.get("club", "brak informacji") in MpIdByClub:
            MpIdByClub[Mp.get("club", "brak informacji")].append(Mp["id"])
            MpNamesByClub[Mp.get("club", "brak informacji")
                          ].append(Mp["lastFirstName"])
        else:
            MpIdByClub[Mp.get("club", "brak informacji")] = [Mp["id"]]
            MpNamesByClub[Mp.get("club", "brak informacji")] = [
                Mp["lastFirstName"]]
    return MpIdByClub, MpsList, MpNamesByClub


def MPsData(term):
    response = requests.get(f"https://api.sejm.gov.pl/sejm/term{term}/MP")
    MpsList = response.json()
    MpData = {"Name": [], "Age": [], "Club": []}
    # current_time = datetime.now().replace(microsecond=0, second=0, minute=0, hour=0)
    termResponse = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}')
    termInfo = termResponse.json()
    endOfTerm = termInfo['from']
    endOfTerm_time = datetime.strptime(endOfTerm, "%Y-%m-%d")
    clubRespnse = requests.get(
        f'https://api.sejm.gov.pl/sejm/term{term}/clubs')
    clubsInfo = clubRespnse.json()
    clubList = []

    for club in clubsInfo:
        clubList.append(club['id'])

    for MP in MpsList:
        if "club" in MP:
            MpData["Name"].append(MP["lastFirstName"])

            MpData["Club"].append(MP["club"])
            dateOfBirth = str(MP["birthDate"]).strip("[]'")
            ageOfMP = endOfTerm_time.date() - \
                datetime.strptime(dateOfBirth, "%Y-%m-%d").date()
            ageOfMP = int(ageOfMP.days/365)

            MpData["Age"].append(ageOfMP)
    DataFRame = pd.DataFrame(MpData)
    return DataFRame, clubList


def ageStats(term, MpIdByClub, Mplist):
    # response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/MP')
    searchedData = 'birthDate'
    MPs = Mplist
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
    # searchedData = f'{searchedInfo}'
    for patry in MpIdByClub:
        # print(committee[patry])
        ages = []

        # print(patry)
        for personId in MpIdByClub[patry]:
            # print(person)
            dateOfBirth = [
                mp['birthDate'] for mp in MPs if mp['id'] == personId]
            # dateOfBirth = str(Mplist[])
            # print(datetime.strptime(str(dateOfBirth[0]), '%Y-%m-%d').date())
            dateOfBirth = str(dateOfBirth).strip("[]'")
            # print(dateOfBirth)
            # print("=================")

            ageOfMP = current_time.date() - \
                datetime.strptime(dateOfBirth, "%Y-%m-%d").date()

            ageOfMP = ageOfMP.days/365
            # if ageOfMP > maxMPsAge:
            #     maxMPsAge = ageOfMP
            # MaxMinMP[0]=
            ages.append(int(ageOfMP))

        MPsAge[patry] = ages
        # MPsAge.append()
        # print(MPsAge)
    agesDataFrame = pd.DataFrame.from_dict(MPsAge, orient='index')

    # agesDataFrame = pd.DataFrame(MPsAge)
    print(agesDataFrame)
    return agesDataFrame, MPsAge


def MoreMPsStats(MPSimpleList, MPIdlist, term=10, searchedInfo='edukacja'):

    MPs = MPSimpleList
    MPsEducation = {}

    for party in MPIdlist:
        educations = {}
        for person in MPIdlist[party]:

            filtered_MPs = [
                mp for mp in MPs if mp['id'] == person]
            # dateOfBirth = [mp['birthDate'] for mp in filtered_MPs]
            if filtered_MPs:
                # print(filtered_MPs)
                educationOfMP = ""
                match searchedInfo:
                    case 'edukacja':
                        educationOfMP = str([
                            mp.get('educationLevel', 'Brak') for mp in filtered_MPs])
                    case 'okręg':
                        educationOfMP = str([
                            mp['districtName'] for mp in filtered_MPs])
                    case 'profesja':

                        educationOfMP = str(
                            [mp['profession'] for mp in filtered_MPs if 'profession' in mp])
                    case 'województwo':
                        educationOfMP = str([
                            mp['voivodeship'] for mp in filtered_MPs])
                educationOfMP = educationOfMP.strip("[]'")

                if educationOfMP in educations:
                    educations[educationOfMP] += 1
                else:
                    educations[educationOfMP] = 1
        MPsEducation[party] = educations
        # print(MPsEducation)
    return MPsEducation


def HistoryOfMp(lastFirstName, currentMpsList, selectedTem):
    # print(lastFirstName)
    request = requests.get("https://api.sejm.gov.pl/sejm/term")
    response = request.json()
    termNum = 0
    for term in response:
        if term['current']:
            termNum = term['num']
            # print(term)
    curr = termNum
    termNum = selectedTem
    HistList = {}

    for termNum in range(termNum, 0, -1):
        if termNum == curr:
            Mp = [Mp for Mp in currentMpsList if Mp['lastFirstName'] == lastFirstName]
            # list[term] = [currentMpsList['club'], currentMpsList['districtName'],,currentMpsList['educationLevel'],currentMpsList['proffesion']]
            Mp = Mp[0]
            Mpstats = MPModel.Mp(Mp.get('club', None), Mp.get('districtName', None), Mp.get('educationLevel', None),
                                 Mp.get('numberOfVotes', None), Mp.get('profession', None), Mp.get('voivodeship', None))
            HistList[termNum] = Mpstats
        else:
            request = requests.get(
                f"https://api.sejm.gov.pl/sejm/term{termNum}/MP")
            response = request.json()

            # print(response, "ressssponse")
            Mp = [Mp for Mp in response if Mp['lastFirstName'] == lastFirstName]

            # print(f"{Mp} Mp zwykłe")
            # print(f"{Mp[0]} Mp nie zwykłe czytaj spierdolone")
            if len(Mp) > 0:
                Mp = Mp[0]
                Mpstats = MPModel.Mp(Mp.get('club', None), Mp.get('districtName', None), Mp.get('educationLevel', None),
                                     Mp.get('numberOfVotes', None), Mp.get('profession', None), Mp.get('voivodeship', None))
                HistList[termNum] = Mpstats
            # else:
        # print(Mpstats.club)
        # print(termNum)
    # print(HistList)
    return HistList
