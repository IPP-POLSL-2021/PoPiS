from sqlalchemy import create_engine
import requests
from Controller.Commitees import CommiteesList, CommiteeFutureSetting

import sys

import pandas as pd
#####


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
            return "brak nowych posiedzeń"
        elif userEvent is False:
            return f"w ciągu ostanich trzech dni komijsa o kodzei {text} miała ostanie spotkanie {date}"
        # print(remindersList['platform'])

        if not ((new_reminder['chanelId'] in remindersList['chanelId'].values) and (new_reminder['platform'] in remindersList['platform'].values) and (new_reminder['committee'] in remindersList['committee'].values)):

            df = pd.DataFrame([new_reminder])
            df.to_csv("./Data/powiadomienia.csv",
                      mode='a', index=False, header=False)
            if date is not None:
                last = f"ostanie spotkanie miało mijesce {date}"
        return f"dodano do obserwoanych {last}"
        # print(response)
    # print(response)

    return "brak"
