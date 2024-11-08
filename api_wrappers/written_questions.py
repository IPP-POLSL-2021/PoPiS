import requests
import datetime
from api_wrappers.MP import get_name

def get_written_questions(term, **params):
    """Returns a list of written questions with optional filters."""
    return requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/writtenQuestions', params=params)

def get_written_question(term, num):
    """Returns details of a written question."""
    return requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/writtenQuestions/{num}')

def get_question_body(term, num):
    """Returns a written question body in HTML format."""
    return requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/writtenQuestions/{num}/body').text

def get_reply_body(term, num, key):
    """Returns a reply body in HTML format."""
    return requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/writtenQuestions/{num}/reply/{key}/body').text

def get_title(term, num, response=False):
    if not response:
        response = get_written_question(term, num)
    return response.json()['title']

def get_date(term, num, mode, response=False):
    if not response:
        response = get_written_question(term, num)
    match mode:
        case 'receipt_date' | 0 | 'data_otrzymania':
            return datetime.datetime.strptime(response.json()['receiptDate'], '%Y-%m-%d').date()
        case 'sent_date' | 1 | 'data_wysłania':
            return datetime.datetime.strptime(response.json()['sentDate'], '%Y-%m-%d').date()
        case 'last_modified' | 2 | 'czas_ostatniej_modyfikacji':
            return datetime.datetime.strptime(response.json()['lastModified'], '%Y-%m-%d %H:%M:%S').date()

def get_authors(term, num, response=False):
    if not response:
        response = get_written_question(term, num)
    IDs = response.json()['from']
    authors = list()
    for i in IDs:
        authors.append(get_name(10, i))
    return authors

def get_receipent(term, num, response=False):
    if not response:
        response = get_written_question(term, num)
    return response.json()['to']

def get_replies(term, num, response=False):
    if not response:
        response = get_written_question(term, num)
    file_urls = list()
    htmls = list()
    for i in response.json()['replies']:
        try:
            for j in i['attachments']:
                file_urls.append(j['URL'])
        except KeyError:
            file_urls.append(None)
        if not i['onlyAttachment']:
            htmls.append(requests.get(
                f"https://api.sejm.gov.pl/sejm/term{term}/writtenQuestions/{num}/reply/{i['key']}/body").text)
    return (file_urls, htmls)
