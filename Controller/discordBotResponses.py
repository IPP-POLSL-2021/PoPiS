from sqlalchemy import create_engine
import requests
from api_wrappers.committees import get_committees, get_committee_future_sitting
from datetime import datetime, timedelta
import sys
# from Controller.telegrambot import create_reminders

import pandas as pd
#####

lastCheckDate = ""


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
        committees = get_committees(10)
        committeesList = ""
        for committee in committees:
            committeesList += f"{committee['name']} o kodzie: {committee['code']}\n"

        # print(commiteesList)
        return f"oto lista komisji\n{committeesList}"
    else:
        return ""


def create_event(id, text, platform, userEvent=True):
    # print(id)
    remindersList = pd.read_csv("./Data/powiadomienia.csv")
    last = ""
    committees = get_committees(10)
    committeesList = ""
    for committee in committees:
        committeesList += f":{committee['code']} "

    if text in committeesList:
        date = get_committee_future_sitting(10, text, 3)
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

        elif userEvent is False:
            Auto_date = f"w ciągu ostatnich trzech dni komisja o kodzie {text} miała ostatnie spotkanie {date}"
            if platform == "discord":
                # id.send(
                #     f"w ciągu ostatnich trzech dni komisja o kodzie {text} miała ostanie spotkanie {date}"
                # )
                print("narazie pusto")
            # else:
                # create_reminders("", True, id, Auto_date)
        # print(remindersList['platform'])
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
