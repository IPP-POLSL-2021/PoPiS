from api_wrappers.committees import get_committees, get_sittings

import csv
import os
from datetime import datetime
from api_wrappers.terms import get_terms
from api_wrappers.MP import get_MPs

def check_data_existence(term, codes):
    print(term)
    # Create a dictionary with codes as keys and the number of sittings as values
    return {code: len(get_sittings(term, code)) for code in codes}

def generate_data_existence_report():
    """
    Generate a CSV report of data existence across terms.
    """
    terms = [3,4,5,6,7,8,9,10]
    # Get all the codes
    codes = set()
    print("start")
    for term in terms:
        committees = get_committees(term)
        for committee in committees:
            codes.add(committee['code'])
    print(codes)
    # Prepare output directory
    output_dir = 'reports'
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f'Committees_sittings_report_{timestamp}.csv')

    # Write report
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=codes)    
        writer.writeheader()
        for term in terms:
            result = check_data_existence(term, codes)
            print(result)
            writer.writerow(result)

    print(f"Data existence report generated: {filename}")

if __name__ == "__main__":
    generate_data_existence_report()