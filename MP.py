import requests
import datetime

def get_MP(term, id):
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/MP/{id}')
    return response
    
def get_name(term, id, response=False):
    if not response:
        response = get_MP(term,id)
    return response.json()['firstLastName']

# Active - Bool
def get_status(term, id, response=False):
    if not response:
        response = get_MP(term,id)
    return response.json()['active']

def get_reason(term, id, response=False):
    if not response:
        response = get_MP(term,id)
    if response.json()['active']:
        return "None - MP is currently active"
    return response.json()['inactiveCause'] + " z powodu " + response.json()['waiverDesc']

#district_num :  A district id where MP was elected Example: 29.
#district_name : A district name where MP was elected Example: Katowice.
#voivodeship :   A voivodeship where MP was elected Example: śląskie.
def get_district(term, id, mode, response=False):
    if not response:
        response = get_MP(term,id)
    match mode:
        case "district_num" | 0 | "numer":
            return response.json()['districtNum']
        case "district_name" | 1 | "nazwa":
            return response.json()['districtName']
        case "voivodeship" | 2 | "województwo":
            return response.json()['voivodeship']
        case _:
            return response.json()['districtNum'] + " - " + response.json()['districtName'] + " - " + response.json()['voivodeship']

def get_club(term, id, response=False):
    if not response:
        response = get_MP(term,id)
    return response.json()['club']
#birth_date (str --> datetime.date): a date of birth Example: 1985-04-14.
#birth_location (str): a place of birth Example: Gliwice.
#profession (str): a profession Example: przedsiębiorca prywatny.
#education_level (str): an education level Example: wyższe.
#number_of_votes (int): a number of votes Example: 19430.
def get_other(term, id, mode, response=False):
    if not response:
        response = get_MP(term, id)
    match mode:
        case 'birth_date' | 0 | 'data_urodzenia':
            return datetime.datetime.strptime(response.json()['birthDate'], '%Y-%m-%d').date()
        case 'birth_location' | 1 | 'miejsce_urodzenia':
            return response.json()['birthLocation']
        case 'profession' | 2 | 'zawód':
            return response.json()['profession']
        case 'education_level' | 3 | 'wykształcenie':
            return response.json()['educationLevel']
        case 'number_of_votes' | 4 | 'liczba_głosów':
            return response.json()['numberOfVotes']
        case _:
            raise Exception("Mode must be specified")
if __name__ == "__main__" :
    # Zwykły - Zrzeczenie - Zgon 
    IDs = ['241','8','244']
    #print(get_MP(10,241).json())
    for i in IDs:
        response = get_MP(10,i)
        print(get_name(10,i, response), get_status(10,i, response), get_reason(10,i, response), get_district(10,i,'district_num', response), get_district(10,i, 1, response), get_district(10,i, 'województwo', response), get_club(10,i, response))
    
    print("========= INNE ========")

    for i in IDs:
        response = get_MP(10,i)
        print(response.json()['id'])
        for j in range(1,5):
            data = get_other(10,i, j, response)
            print(data, end=" ")
        print("")