from Commitees import CommiteesList, CommiteeFutureSetting
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Model import DatabaseContext
from Model import RemindersModel


def get_respone(User_Input):
    lowered = User_Input.lower()
    if lowered == '':
        return ""
    elif lowered == "komisje":
        commitees = CommiteesList(10)
        commiteesList = ""
        for commitee in commitees:

            commiteesList += f"{commitee['name']} o kodzie: {commitee['code']}\n"

        print(commiteesList)
        return f"oto lista komisji\n{commiteesList}"
    else:
        return ""


def create_event(id, text):
    print(id)
    db_context = DatabaseContext.DatabaseContext()
    session = db_context.get_session()
    commitees = CommiteesList(10)
    commiteesList = ""
    for commitee in commitees:

        commiteesList += f":{commitee['code']} "
    if text in commiteesList:
        date = CommiteeFutureSetting(10, text)
        new_reminder = RemindersModel.Reminders(
            chanelId=id, committeeSitting=date, platform="discord")
        session.add(new_reminder)
        session.commit()
        # print(response)
    # print(response)
    db_context.close_session(session)
