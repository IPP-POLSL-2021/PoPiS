from api_wrappers.committees import get_committees

import csv
import os
from datetime import datetime
from api_wrappers.terms import get_terms
from api_wrappers.MP import get_MPs

def check_data_existence(term,fieldnames):
    print(term)
    results = {'code':'', 'name': ' ', 'nameGenitive': ' ', 'type': ' ', 'phone': ' ', 'appointmentDate': '', 'compositionDate': '', 'scope': '', 'members': ''}
    erw = {'code':0, 'name': 0, 'nameGenitive': 0, 'type': 0, 'phone': 0, 'appointmentDate': 0, 'compositionDate': 0, 'scope': 0, 'members': 0}
    committee_data = get_committees(term)
    for committee in committee_data:
        for fieldname in fieldnames:
            if fieldname not in committee:
                results[fieldname] += str(committee['code'])
                results[fieldname] += ', '
                erw[fieldname] += 1
    max = len(committee_data)
    for i in results:
        if erw[i] >= max:
            results[i] = 'Wszystkie'            
    return results

def generate_data_existence_report():
    """
    Generate a CSV report of data existence across terms.
    """
    terms = [3,4,5,6,7,8,9,10]
    # Prepare output directory
    output_dir = 'reports'
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f'Committees_fields_existence_report_{timestamp}.csv')
    # Write report
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['code', 'name', 'nameGenitive', 'type', 'phone', 'appointmentDate', 'compositionDate', 'scope','members']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for term in terms:
            result = check_data_existence(term, fieldnames)
            writer.writerow(result)

    print(f"Data existence report generated: {filename}")

if __name__ == "__main__":
    generate_data_existence_report()