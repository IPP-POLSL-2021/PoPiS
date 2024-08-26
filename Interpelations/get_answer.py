import requests
def get_interpelation(term_number, interpelation_number): # Przyjmuje numer kadencji i interpelacji a zwraca odpowiedź w formie json
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term_number}/interpellations/{interpelation_number}')         
    return response.json()

def get_replies(response): # Przyjmuje odpowiedź jsonową z get_interpelation i zwraca listę linków do pobrania odpowiedzi w formie pdf
    urls = list()
    for i in response['replies']:
        for j in i['attachments']:
            # Sprawdź flagę czy jest tylko załącznik czy trzeba renderować html'a
            if i['onlyAttachment']:
                urls.append(j['URL'])
            else:
                # Tymczasowo zamiast działać poprawnie zwróć numer interpelacji gdzie onlyAttachment jest false a więc trzeba dorobić logikę
                return response['num']
    return urls

if __name__ == "__main__" :
    response_single = get_interpelation(10,3999)
    response_multiple = get_interpelation(10,296)
    response_noanswer = get_interpelation(10,1481)
    print(get_replies(response_single))
    print(get_replies(response_multiple))
    print(get_replies(response_noanswer))

    # Expected Output
    #['https://orka2.sejm.gov.pl/INT10.nsf/klucz/ATTD8AJ46/$FILE/i03999-o1.pdf']
    #['https://orka2.sejm.gov.pl/INT10.nsf/klucz/ATTCZRK2H/$FILE/i00296-o1.pdf', 'https://orka2.sejm.gov.pl/INT10.nsf/klucz/ATTD29JSZ/$FILE/i00296-o2.pdf', 'https://orka2.sejm.gov.pl/INT10.nsf/klucz/ATTD34L8A/$FILE/i00296-o3.pdf']
    #[]