from sqlalchemy import create_engine
import requests
from Controller.Commitees import CommiteesList, CommiteeFutureSetting
from sqlalchemy.orm import sessionmaker
from Model.DatabaseContext import DatabaseContext
from Model.RemindersModel import Reminders
import sys

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
    db_context = DatabaseContext()

    session = db_context.get_session()
    commitees = CommiteesList(10)
    commiteesList = ""
    for commitee in commitees:

        commiteesList += f":{commitee['code']} "
    if text in commiteesList:
        date = CommiteeFutureSetting(10, text)
        new_reminder = Reminders(
            chanelId=id, committeeSitting=date, platform=platfom)
        session.add(new_reminder)
        session.commit()
        db_context.close_session(session)
        return date
        # print(response)
    # print(response)
    db_context.close_session(session)
    return "brak"
