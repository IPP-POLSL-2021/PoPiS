
import requests
from api_wrappers.committees import get_committees, get_committee_future_sitting
from datetime import datetime, timedelta
import sys
# from Controller.telegrambot import create_reminders
import requests
import pandas as pd
#####

lastCheckDate = ""


def delete(commite_code, id):
    remindersList = pd.read_csv("./Data/powiadomienia.csv")
    if ((id in remindersList['channelId'].values) and
            (commite_code in remindersList['committee'].values)):
        foundCommittee = remindersList.loc[~((remindersList['channelId'] ==
                                              id) & (remindersList['committee'] == commite_code))]
        foundCommittee.to_csv("./Data/powiadomienia.csv", index=False)


def check_24_hours(file, platform=""):
    # Odczytaj datę z pliku
    last_check_str = readDate(file)

    # Sprawdź, czy plik był kiedykolwiek zapisany
    if last_check_str:
        last_check = datetime.strptime(last_check_str, '%Y-%m-%d %H:%M:%S')
    else:
        last_check = None

    # Oblicz różnicę czasu
    current_time = datetime.now().replace(microsecond=0)

    if last_check is None or (current_time - last_check) >= timedelta(hours=24):
        remindersList = pd.read_csv("./Data/powiadomienia.csv")
        write(file, current_time)
        newList = ""
        filtered_reminders = remindersList[remindersList['platform'] == platform]
        print(filtered_reminders)

        return filtered_reminders
    else:
        return False


def write(file, lastCheckDate):
    with open(file, mode="w") as writingFile:
        writingFile.write(str(lastCheckDate))


def readDate(file):
    with open(file, mode="r") as readingFile:
        lastCheckDate = readingFile.read()
        # isRead = True
        return lastCheckDate


def get_response(User_Input):
    lowered = User_Input.lower()
    if lowered == '':
        return ""
    elif lowered == "komisje":
        term = 10
        committees = get_committees(term)
        committeesList = ""
        for committee in committees:
            committeesList += f"{committee['name']} o kodzie: {committee['code']}\n"

        # print(commiteesList)
        return f"oto lista komisji\n{committeesList}"
    else:
        return ""


def create_event(id, text, platform):

    remindersList = pd.read_csv("./Data/powiadomienia.csv")
    last = ""
    response = requests.get(f"https://api.sejm.gov.pl/sejm/term")
    termList = response.json()
    for TERM in termList:
        if TERM["current"] == True:
            term = TERM["num"]
    committees = get_committees(term)
    committeesList = ""
    for committee in committees:
        committeesList += f":{committee['code']} "

    if text in committeesList:
        date = get_committee_future_sitting(term, text, 3)
        new_reminder = {
            'channelId': id, 'platform': platform, 'committee': text}

        if date is None:
            if not ((new_reminder['channelId'] in remindersList['channelId'].values) and
                    (new_reminder['platform'] in remindersList['platform'].values) and
                    (new_reminder['committee'] in remindersList['committee'].values)):
                df = pd.DataFrame([new_reminder])
                df.to_csv("./Data/powiadomienia.csv",
                          mode='a', index=False, header=False)
            return "brak nowych posiedzeń"
        request = requests.get(
            f"https://api.sejm.gov.pl/sejm/term10/committees/{text}")
        response = request.json()
        if not ((new_reminder['channelId'] in remindersList['channelId'].values) and
                (new_reminder['platform'] in remindersList['platform'].values) and
                (new_reminder['committee'] in remindersList['committee'].values)):
            df = pd.DataFrame([new_reminder])
            df.to_csv("./Data/powiadomienia.csv",
                      mode='a', index=False, header=False)

        if date is not None:
            last = f" %ostatnie spotkanie  {response['name']}  miało miejsce {date}"
        return f"dodano do obserwowanych {last}"
    else:
        return "brak"
