import requests
from datetime import datetime

def get_statements(term, proceeding_id, date):
    """Returns a list of statements."""
    if isinstance(date, datetime):
        date = date.strftime('%Y-%m-%d')
    response = requests.get(
        f'https://api.sejm.gov.pl/sejm/term{term}/proceedings/{proceeding_id}/{date}/transcripts')
    return response

def get_pdf_transcript(term, proceeding_id, date):
    """Returns a transcript of a day of a proceeding in PDF format."""
    if isinstance(date, datetime):
        date = date.strftime('%Y-%m-%d')
    response = requests.get(
        f'https://api.sejm.gov.pl/sejm/term{term}/proceedings/{proceeding_id}/{date}/transcripts/pdf')
    return response.content

def get_statement(term, proceeding_id, date, statement_num):
    """Returns a statement body in HTML format."""
    if isinstance(date, datetime):
        date = date.strftime('%Y-%m-%d')
    response = requests.get(
        f'https://api.sejm.gov.pl/sejm/term{term}/proceedings/{proceeding_id}/{date}/transcripts/{statement_num}')
    return response.text

if __name__ == "__main__":
    # Example usage
    statements = get_statements(10, 1, '2023-11-29')
    if statements and 'statements' in statements:
        print("Statements from proceeding:")
        for statement in statements['statements']:
            if 'name' in statement and 'function' in statement:
                print(f"{statement['name']} ({statement['function']})")
