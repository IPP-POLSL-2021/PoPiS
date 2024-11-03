import requests
from datetime import datetime, timedelta
import pandas as pd


def groupMpsByClub(term):
    response = requests.get(f"https://api.sejm.gov.pl/sejm/term{term}/MP")
    MpsList = response.json()
    MpIdByClub = {}
    MpNamesByClub = {}
    for Mp in MpsList:
        if Mp["club"] in MpIdByClub:
            MpIdByClub[Mp["club"]].append(Mp["id"])
            MpNamesByClub[Mp["club"]].append(Mp["lastFirstName"])
        else:
            MpIdByClub[Mp["club"]] = [Mp["id"]]
            MpNamesByClub[Mp["club"]] = [Mp["lastFirstName"]]
    # print(MpIdByClub)
    return MpIdByClub, MpsList, MpNamesByClub


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
            ages.append(round(ageOfMP))

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
                            mp['educationLevel'] for mp in filtered_MPs])
                    case 'okrąg':
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
