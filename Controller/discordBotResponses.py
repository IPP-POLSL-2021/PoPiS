from sqlalchemy import create_engine
import requests
from Controller.Commitees import CommiteesList, CommiteeFutureSetting
from datetime import datetime, timedelta
import sys

import pandas as pd
#####

lastCheckDate = ""


async def check_24_hours(file):
    # Odczytaj datę z pliku
    last_check_str = readDate(file)

    # Sprawdź, czy plik był kiedykolwiek zapisany
    if last_check_str:
        last_check = datetime.strptime(last_check_str, '%Y-%m-%d %H:%M:%S')
    else:
        last_check = None

    # Oblicz różnicę czasu
    current_time = datetime.now()

    if last_check is None or (current_time - last_check) >= timedelta(hours=24):
        remindersList = pd.read_csv("./Data/powiadomienia.csv")
        write(file, current_time)
        for reminder in remindersList:
            create_event(reminder['chanelId'],
                         reminder['platform'], reminder['committee'], False)

        return True
    else:
        return False


def write(file, lastCheckDate):

    with open(file, mode="w") as writingFile:
        writingFile.write(lastCheckDate)


def readDate(file):
    with open(file, mode="r") as readingFile:
        lastCheckDate = readingFile.read()
        # isRead = True
        return lastCheckDate


def get_respone(User_Input):
    lowered = User_Input.lower()
    if lowered == '':
        return ""
    elif lowered == "komisje":
        commitees = CommiteesList(10)
        commiteesList = ""
        for commitee in commitees:

            commiteesList += f"{commitee['name']} o kodzie: {commitee['code']}\n"

        # print(commiteesList)
        return f"oto lista komisji\n{commiteesList}"
    else:
        return ""


def create_event(id, text, platfom, userEvent=True):
    # print(id)
    remindersList = pd.read_csv("./Data/powiadomienia.csv")
    last = ""
    commitees = CommiteesList(10)
    commiteesList = ""
    for commitee in commitees:

        commiteesList += f":{commitee['code']} "
    if text in commiteesList:
        date = CommiteeFutureSetting(10, text)
        new_reminder = {
            'chanelId': id, 'platform': platfom, 'committee': text}
        if date is None:
            if not ((new_reminder['chanelId'] in remindersList['chanelId'].values) and (new_reminder['platform'] in remindersList['platform'].values) and (new_reminder['committee'] in remindersList['committee'].values)):
                df = pd.DataFrame([new_reminder])
                df.to_csv("./Data/powiadomienia.csv",
                          mode='a', index=False, header=False)
            return "brak nowych posiedzeń"
        elif userEvent is False:
            return f"w ciągu ostanich trzech dni komijsa o kodzei {text} miała ostanie spotkanie {date}"
        # print(remindersList['platform'])

        if not ((new_reminder['chanelId'] in remindersList['chanelId'].values) and (new_reminder['platform'] in remindersList['platform'].values) and (new_reminder['committee'] in remindersList['committee'].values)):

            df = pd.DataFrame([new_reminder])
            df.to_csv("./Data/powiadomienia.csv",
                      mode='a', index=False, header=False)
            if date is not None:
                last = f"ostanie o kodzie {text} spotkanie miało mijesce {date}"
        return f"dodano do obserwoanych {last}"
        # print(response)
    # print(response)
    else:
        return "brak"
