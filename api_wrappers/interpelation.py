import requests
import datetime
from Controller.MP import get_name  # Importing get_name from MP module

def get_interpelations(term, **params):
    """Returns a list of interpellations with optional filters."""
    return requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/interpellations', params=params)

def get_interpelation(term, num):
    """Returns details of a specific interpellation."""
    return requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/interpellations/{num}')

def get_interpelation_body(term, num):
    """Returns an interpellation body in HTML format."""
    return requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/interpellations/{num}/body').text

def get_reply_body(term, num, key):
    """Returns a reply body in HTML format."""
    return requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/interpellations/{num}/reply/{key}/body').text

def get_title(term, num, response=False):
    """Get the title of an interpellation."""
    if not response:
        response = get_interpelation(term, num)
    return response.json()['title']

def get_date(term, num, mode, response=False):
    """Get various dates related to an interpellation."""
    if not response:
        response = get_interpelation(term, num)
    data = response.json()
    
    match mode:
        case 'receipt_date' | 0 | 'data_otrzymania':
            return datetime.datetime.strptime(data['receiptDate'], '%Y-%m-%d').date()
        case 'sent_date' | 1 | 'data_wysłania':
            return datetime.datetime.strptime(data['sentDate'], '%Y-%m-%d').date()
        case 'last_modified' | 2 | 'czas_ostatniej_modyfikacji':
            return datetime.datetime.strptime(data['lastModified'], '%Y-%m-%dT%H:%M:%S').date()

def get_authors(term, num, response=False):
    """Get the authors of an interpellation."""
    if not response:
        response = get_interpelation(term, num)
    IDs = response.json()['from']
    return [get_name(term, id) for id in IDs]

def get_receipent(term, num, response=False):
    """Get the recipients of an interpellation."""
    if not response:
        response = get_interpelation(term, num)
    return response.json()['to']

def get_replies(term, num, response=False):
    """Get replies to an interpellation."""
    if not response:
        response = get_interpelation(term, num)
    
    file_urls = []
    htmls = []
    
    for reply in response.json()['replies']:
        # Handle attachments
        try:
            file_urls.extend([j['URL'] for j in reply.get('attachments', [])])
        except KeyError:
            file_urls.append(None)
        
        # Handle HTML body
        if not reply.get('onlyAttachment', False):
            html_response = requests.get(
                f"https://api.sejm.gov.pl/sejm/term{term}/interpellations/{num}/reply/{reply['key']}/body"
            )
            htmls.append(html_response.text)
    
    return (file_urls, htmls)

def get_repeated_interpellations(term, num, response=False):
    """Get repeated interpellations (follow-up questions)."""
    if not response:
        response = get_interpelation(term, num)
    return response.json().get('repeatedInterpellation', [])

# Additional utility functions
def is_repeated_interpellation(term, num, response=False):
    """Check if this is a repeated interpellation."""
    if not response:
        response = get_interpelation(term, num)
    return len(response.json().get('repeatedInterpellation', [])) > 0

if __name__ == "__main__":
    # Example usage demonstrating various methods
    term = 10
    num = "3999"  # Example interpellation number
    
    print("Interpellation Details:")
    print(f"Title: {get_title(term, num)}")
    print(f"Receipt Date: {get_date(term, num, 'receipt_date')}")
    print(f"Sent Date: {get_date(term, num, 'sent_date')}")
    print(f"Authors: {get_authors(term, num)}")
    print(f"Recipients: {get_receipent(term, num)}")
    
    file_urls, htmls = get_replies(term, num)
    print(f"Reply File URLs: {file_urls}")
    print(f"Number of HTML Replies: {len(htmls)}")
