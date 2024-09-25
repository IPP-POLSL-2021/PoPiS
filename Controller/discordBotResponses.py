from Commitees import CommiteesList, CommiteeFutureSetting
import requests


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


# def create_event(id, text):
#     print(id)
#     commitees = CommiteesList(10)
#     commiteesList = ""
#     for commitee in commitees:

#         commiteesList += f":{commitee['code']} "
#     if text in commiteesList:
#         response = requests.get(
#             f'https://discord.com/api/v10/guilds/{id}/scheduled-events')
#         print(response)
#     print(response)
