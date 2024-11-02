import requests


def groupMpsByClub(term):
    response = requests.get(f"https://api.sejm.gov.pl/sejm/term{term}/MP")
    MpsList = response.json()
    MpIdByClub = {}
    MpNamesByClub = {}
    for Mp in MpsList:
        if Mp["club"] in MpIdByClub:
            MpIdByClub[Mp["club"]].append(Mp["id"])
            MpNamesByClub[Mp["lastFirstName"]].append(Mp["id"])
        else:
            MpIdByClub[Mp["club"]] = [Mp["id"]]
            MpNamesByClub[Mp["lastFirstName"]] = [Mp["id"]]
    # print(MpIdByClub)
    return MpIdByClub, MpsList, MpNamesByClub
