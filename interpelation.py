# Maybe some more showing in if name == main or professional pytest testing
# Or type hints for functions, or comments directly next to function name so vscode nicely displays
import requests
import datetime
from MP import get_name
from functools import wraps

def get_interpelation(term, num): # Przyjmuje numer kadencji i interpelacji a zwraca odpowiedź w formie json
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/interpellations/{num}')         
    return response

# Enable supplying just response or full parameters
def handle_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = kwargs.get('response')

        # If response is not provided, try extracting term, sitting, and id from args or kwargs
        if not response:
            if len(args) >= 2:
                term, num = args[:2]  # Positional arguments
            else:
                term = kwargs.get('term')
                num = kwargs.get('num')
            
            # Ensure term, num are provided
            if term is None or num is None:
                raise ValueError("Provide term and num when response is not given")
            
            # Fetch the response
            response = get_interpelation(term,num)
            kwargs['response'] = response

        # Call the wrapped function with response
        return func(*args, **kwargs)
    
    return wrapper

@handle_response
def get_title(term=None, num=None, response=False):
    return response.json()['title']

#receipt_date str --> datetime.date: A date when the case was received Example: 2020-11-16.
#sent_date str --> datetime.date: A date when the interpellation was sent to recipients Example: 2021-01-20.
#last_modified str --> datetime.datetime: A date of last modification of a document Example: 2022-09-07 15:01:42.
@handle_response
def get_date(term=None, num=None, mode=None, response=False):
    match mode:
        case 'receipt_date' | 0 | 'data_otrzymania':
            return datetime.datetime.strptime(response.json()['receiptDate'], '%Y-%m-%d').date()
        case 'sent_date' | 1 | 'data_wysłania':
            return datetime.datetime.strptime(response.json()['sentDate'], '%Y-%m-%d').date()
        case 'last_modified' | 2 | 'czas_ostatniej_modyfikacji':
            return datetime.datetime.strptime(response.json()['lastModified'], '%Y-%m-%d %H:%M:%S')

def get_authors(term=None, num=None, response=False):
    if not response:
        response = get_interpelation(term, num)
    IDs = response.json()['from']
    authors = list()
    for i in IDs:
        authors.append(get_name(10,i))
    return authors

def get_receipent(term=None, num=None, response=False):
    if not response:
        response = get_interpelation(term,num)
    return response.json()['to']

def get_replies(term=None, num=None, response=False): # Przyjmuje odpowiedź jsonową z get_interpelation i zwraca listę linków do pobrania odpowiedzi w formie pdf
    if not response:
        response = get_interpelation(term, num)
    file_urls = list()
    htmls = list()
    ## 3 opcje
    ## onlyAttachment = True & attachments istnieje
    ## onlyAttachment = False & attachments istnieje
    ## attachments nie istnieje (onlyAttachment chyba zawsze wtedy false, alternatywa nie miałaby sensu) 
    for i in response.json()['replies']:
        try:
            for j in i['attachments']:
                file_urls.append(j['URL'])
        except KeyError:
            # Nie ma attachmentów do pobrania 
            file_urls.append(None)
        if not i['onlyAttachment']:
            # TODO Musimy renderować html TODO
            htmls.append(requests.get(f"https://api.sejm.gov.pl/sejm/term{term}/interpellations/{num}/reply/{i['key']}/body").text)
    return (file_urls, htmls)

if __name__ == "__main__" :
    response = get_interpelation(10,3999)
    
    print(get_title(response=response))
    print(get_date(mode=1,response=response))
    print(get_authors(response=response))
    print(get_receipent(response=response))
    # Expected Output
    #Interpelacja w sprawie ministerialnej oceny skutków gospodarczych tzw. kredytu 0%
    #2024-07-25
    #['Sławomir Mentzen', 'Bartłomiej Pejo', 'Ryszard Wilk']
    #['minister rozwoju i technologii']

    print(get_replies(10,3999)[0])
    print(get_replies(10,12)[0])
    print(get_replies(10,3)[0])
    # Expected Output
    #['https://orka2.sejm.gov.pl/INT10.nsf/klucz/ATTD8AJ46/$FILE/i03999-o1.pdf']
    #[None]
    #['https://orka2.sejm.gov.pl/INT10.nsf/klucz/ATTCYYKKZ/$FILE/i00003-o1.pdf', 'https://orka2.sejm.gov.pl/INT10.nsf/klucz/ATTCZEK3B/$FILE/i00003-o2_1.pdf', 'https://orka2.sejm.gov.pl/INT10.nsf/klucz/ATTCZEK3B/$FILE/i00003-o2_2.pdf']
    
    print(get_replies(10,3999)[1], end="\n ============================ \n")
    print(get_replies(10,12)[1], end="\n ============================ \n")
    print(get_replies(10,3)[1])
    # Expected Output
    #[]
    # ============================ 
    #['<!DOCTYPE html>\n<html lang="pl">\n<head>\n<meta name="charset" content="utf-8">\n<title>Odpowiedź na interpelację w sprawie wydatków na\xa0świadczenie\xa0rodzicielskie\xa0("kosiniakowe"), wysokości tego świadczenia oraz\xa0liczby osób otrzymujących to świadczenie\xa0w\xa0latach 2016-2022</title>\n</head>\n<body>\n<h1>Odpowiedź na interpelację nr 12</h1>\r\n\t<p class="int-title">w sprawie wydatków na\xa0świadczenie\xa0rodzicielskie\xa0("kosiniakowe"), wysokości tego świadczenia oraz\xa0liczby osób otrzymujących to świadczenie\xa0w\xa0latach 2016-2022</p>\r\n\t<p class="intAuthor">Odpowiadający: minister rodziny, pracy i polityki społecznej Agnieszka Dziemianowicz-Bąk</p>\r\n\t<p class="intDate">Warszawa, 06-02-2024</p>\r\n\t<p>Szanowny Panie Marszałku,</p>\r\n<p>w związku z interpelacją nr 12 Pani Poseł Kariny Anny Bosak z dnia 7 grudnia 2023 r. w sprawie wydatków na świadczenie rodzicielskie („kosiniakowe“), wysokości tego świadczenia oraz liczby osób otrzymujących to świadczenie w latach 2016–2022, poniżej przekazuję odpowiednie informacje w tym zakresie.</p>\r\n<p>Pragnę zwrócić uwagę, że sprawozdania rzeczowo-finansowe z realizacji świadczeń rodzinnych zawierają dane zagregowane obejmujące liczbę wypłaconych świadczeń oraz wydatków na nie. Nie zawierają one wyodrębnionej kategorii świadczeń pobranych przez beneficjentów, wynikających z art. 17c ust. 1 i ust. 2 ustawy o świadczeniach rodzinnych.</p>\r\n<p>Ponadto informuję, iż wysokość wypłacanego świadczenia rodzicielskiego pozostaje niezmienna od chwili jego wprowadzenia. W związku z powyższym podczas weryfikacji w 2018 r. oraz 2021 r. Radzie Dialogu Społecznego nie została zaproponowana zmiana wysokości świadczenia. </p>\r\n<p>Informuję również, że kwoty, o których mowa w art. 5 ust. 1 i 2 oraz art. 15b ust. 2, zostaną poddane weryfikacji i odpowiedniej analizie w roku 2024 zgodnie z art. 18 ww. ustawy.</p>\r\n\r\n<p>Tabela 1 – Dane dotyczące wypłat świadczenia rodzicielskiego w latach 2016–2022</p>\r\n\r\n<table border="1" cellpadding="5">\r\n <tbody>\r\n  <tr>\r\n   <td>  </td>\r\n   <td> <p><strong>Wydatki w mln zł</strong></p> </td>\r\n   <td> <p><strong>Przeciętna liczba świadczeniobiorców w tys.</strong></p> </td>\r\n  </tr>\r\n  <tr>\r\n   <td> <p><strong>2016</strong></p> </td>\r\n   <td> <p>862,9</p> </td>\r\n   <td> <p>78</p> </td>\r\n  </tr>\r\n  <tr>\r\n   <td> <p><strong>2017</strong></p> </td>\r\n   <td> <p>1 044,6</p> </td>\r\n   <td> <p>94,5</p> </td>\r\n  </tr>\r\n  <tr>\r\n   <td> <p><strong>2018</strong></p> </td>\r\n   <td> <p>999,4</p> </td>\r\n   <td> <p>91,4</p> </td>\r\n  </tr>\r\n  <tr>\r\n   <td> <p><strong>2019</strong></p> </td>\r\n   <td> <p>920,2</p> </td>\r\n   <td> <p>84,3</p> </td>\r\n  </tr>\r\n  <tr>\r\n   <td> <p><strong>2020</strong></p> </td>\r\n   <td> <p>862,9</p> </td>\r\n   <td> <p>79,1</p> </td>\r\n  </tr>\r\n  <tr>\r\n   <td> <p><strong>2021</strong></p> </td>\r\n   <td> <p>784,6</p> </td>\r\n   <td> <p>72,6</p> </td>\r\n  </tr>\r\n  <tr>\r\n   <td> <p><strong>2022</strong></p> </td>\r\n   <td> <p>678,5</p> </td>\r\n   <td> <p>62,3</p> </td>\r\n  </tr>\r\n </tbody>\r\n</table>\r\n\r\n\r\n<p>Z wyrazami szacunku</p>\r\n<p>Agnieszka Dziemianowicz-Bąk<br>Minister Rodziny, Pracy i Polityki Społecznej</p>\r\n\r\n\r\n</body>\n</html>']
    # ============================ 
    #['<!DOCTYPE html>\n<html lang="pl">\n<head>\n<meta name="charset" content="utf-8">\n<title>Odpowiedź na interpelację w sprawie spisów wyborców udostępnionych Poczcie Polskiej SA przez gminy na wybory prezydenckie</title>\n</head>\n<body>\n<h1>Odpowiedź na interpelację nr 3</h1>\r\n\t<p class="int-title">w sprawie spisów wyborców udostępnionych Poczcie Polskiej SA przez gminy na wybory prezydenckie</p>\r\n\t<p class="intAuthor">Odpowiadający: minister aktywów państwowych Borys Budka</p>\r\n\t<p class="intDate">Warszawa, 10-01-2024</p>\r\n \t<p>Treść odpowiedzi znajduje się w załączniku.</p>\r\n\t<h2 class="attachments">Załączniki</h2><ol class="attachments-list"><li><a href="https://sejm.gov.pl/int10.nsf/klucz/ATTCZEK3B/$FILE/i00003-o2_1.pdf" target="_blank">MAP_K10INT3_uzupełnienie.pdf</a></li><li><a href="https://sejm.gov.pl/int10.nsf/klucz/ATTCZEK3B/$FILE/i00003-o2_2.pdf" target="_blank">Zał. Wykaz jednostek samorządowych, które przesłały Poczcie Polskiej S.A. dane ze spisów wyborczych na potrzeby wyborów korespondencyjnych.pdf</a></li></ol>\r\n</body>\n</html>']    #['https://orka2.sejm.gov.pl/INT10.nsf/klucz/ATTD8AJ46/$FILE/i03999-o1.pdf']