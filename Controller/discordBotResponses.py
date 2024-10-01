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


def create_event(id, text, platfom):
    # print(id)
    remindersList = pd.read_csv("./Data/powiadomienia.csv")

    commitees = CommiteesList(10)
    commiteesList = ""
    for commitee in commitees:

        commiteesList += f":{commitee['code']} "
    if text in commiteesList:
        date = CommiteeFutureSetting(10, text)
        new_reminder = {
            'chanelId': id, 'committeeSitting': date, 'platform': platfom}
        if date is None:
            return "brak posiedzeń"
        if remindersList.loc[id, date, platfom] is None:
            df = pd.DataFrame(new_reminder)
            df.to_csv(remindersList, index=False, mode='a', header=False)
        return date
        # print(response)
    # print(response)

    return "brak"
