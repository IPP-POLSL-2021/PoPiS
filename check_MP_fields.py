import csv
import os
from datetime import datetime
from api_wrappers.terms import get_terms
from api_wrappers.MP import get_MPs

def check_data_existence(term,fieldnames):
    print(term)
    results = {'accusativeName': ' ', 'active': ' ', 'birthDate': ' ', 'birthLocation': ' ', 'club': ' ', 'districtName': ' ', 'districtNum': ' ', 'educationLevel': ' ', 'email': ' ', 'firstLastName': ' ', 'firstName': ' ', 'genitiveName': ' ', 'id': ' ', 'lastFirstName': ' ', 'lastName': ' ', 'numberOfVotes': ' ', 'profession': ' ', 'secondName': ' ', 'voivodeship': ' '}
    erw = {'accusativeName': 0, 'active': 0, 'birthDate': 0, 'birthLocation': 0, 'club': 0, 'districtName': 0, 'districtNum': 0, 'educationLevel': 0, 'email': 0, 'firstLastName': 0, 'firstName': 0, 'genitiveName': 0, 'id': 0, 'lastFirstName': 0, 'lastName': 0, 'numberOfVotes': 0, 'profession': 0, 'secondName': 0, 'voivodeship': 0}
    
    mp_data = get_MPs(term).json()
    for mp in mp_data:
        for fieldname in fieldnames:
            if fieldname not in mp:
                results[fieldname] += str(mp['id'])
                results[fieldname] += ', '
                erw[fieldname] += 1
        if mp['numberOfVotes'] == 0:
            results['numberOfVotes'] += str(mp['id'])
            results['numberOfVotes'] += ', '
            erw['numberOfVotes'] += 1
    max = len(mp_data)
    for i in results:
        if erw[i] >= max:
            results[i] = 'Wszystkie'            
    return results

def generate_data_existence_report():
    """
    Generate a CSV report of data existence across terms.
    """
    # Get available terms
    #terms_data = get_terms().json()
    #terms = sorted([term['num'] for term in terms_data])
    terms = [3,4,5,6,7,8,9,10]
    # Prepare output directory
    output_dir = 'reports'
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f'MP_fields_existence_report_{timestamp}.csv')
    #sampleMP = {"accusativeName":"Andrzeja Adamczyka","active":True,"birthDate":"1959-01-04","birthLocation":"Krzeszowice","club":"PiS","districtName":"Kraków","districtNum":13,"educationLevel":"wyższe","email":"Andrzej.Adamczyk@sejm.pl","firstLastName":"Andrzej Adamczyk","firstName":"Andrzej","genitiveName":"Andrzeja Adamczyka","id":1,"lastFirstName":"Adamczyk Andrzej","lastName":"Adamczyk","numberOfVotes":45171,"profession":"ekonomista","secondName":"Mieczysław","voivodeship":"małopolskie"}
    # Write report
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['accusativeName', 'active', 'birthDate', 'birthLocation', 'club', 'districtName', 'districtNum', 'educationLevel', 'email', 'firstLastName', 'firstName', 'genitiveName', 'id', 'lastFirstName', 'lastName', 'numberOfVotes', 'profession','secondName', 'voivodeship']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for term in terms:
            result = check_data_existence(term, fieldnames)
            writer.writerow(result)

    print(f"Data existence report generated: {filename}")

if __name__ == "__main__":
    generate_data_existence_report()