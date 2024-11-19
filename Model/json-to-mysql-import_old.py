import json
import mysql.connector
from mysql.connector import Error
from tqdm import tqdm

def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host='mysql.mikr.us',
            database='db_c179',
            user='c179',
            password='CE43_815986'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    return None

def insertClub(connection, club_data):
    try:
        cursor = connection.cursor()
        query = """INSERT INTO club (id, name, email, fax, phone, membersCount) 
                   VALUES (%s, %s, %s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE
                   name = VALUES(name), 
                   email = VALUES(email), 
                   fax = VALUES(fax), 
                   phone = VALUES(phone), 
                   membersCount = VALUES(membersCount)"""
        
        values = (
            club_data['id'],
            club_data['name'],
            club_data['email'],
            club_data['fax'],
            club_data['phone'],
            club_data['membersCount']
        )
        
        cursor.execute(query, values)
        connection.commit()
        print(f"Club data inserted/updated successfully: {club_data['name']}")
    except Error as e:
        print(f"Error while inserting club data: {e}")

def insertMP(connection, mp_data):
    try:
        cursor = connection.cursor()
        query = """INSERT INTO mp (id, accusativeName, active, birthDate, birthLocation, 
                   club, districtName, districtNum, firstLastName, firstName, genitiveName, 
                   term, lastFirstName, lastName, numberOfVotes, profession, secondName, 
                   voivodeship, email, educationLevel) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        values = (
            mp_data['id'], 
            mp_data['accusativeName'], 
            mp_data['active'], 
            mp_data['birthDate'],
            mp_data['birthLocation'], 
            mp_data['club'],  # Now using the club ID directly
            mp_data['districtName'], 
            mp_data['districtNum'],
            mp_data['firstLastName'], 
            mp_data['firstName'], 
            mp_data['genitiveName'],
            mp_data.get('term'),
            mp_data['lastFirstName'], 
            mp_data['lastName'], 
            mp_data['numberOfVotes'],
            mp_data.get('profession', 'Unknown'),  # Default to 'Unknown' if missing
            mp_data.get('secondName'), 
            mp_data['voivodeship'],
            mp_data['email'], 
            mp_data['educationLevel']
        )
        
        cursor.execute(query, values)
        connection.commit()
        print(f"MP data inserted successfully: {mp_data['firstLastName']}")
    except Error as e:
        print(f"Error while inserting MP data for {mp_data['firstLastName']}: {e}")

def insertInterpelation(connection, interpelation_data):
    try:
        cursor = connection.cursor()
        query = """INSERT INTO interpellation (id, term, num, title, receiptDate, lastModified, `from`, `to`, sentDate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        from_json = json.dumps(interpelation_data['from']) if isinstance(interpelation_data['from'], list) else interpelation_data['from']
        to_json = json.dumps(interpelation_data['to']) if isinstance(interpelation_data['to'], list) else interpelation_data['to']

        values = (
            interpelation_data['num'], # In JSON there's only "num", because their indexes are automatic which we could do also in database but that would create even more problems than it solves
            interpelation_data['term'],
            interpelation_data['num'],
            interpelation_data['title'],
            interpelation_data['receiptDate'],
            interpelation_data['lastModified'],
            from_json, # Hocus Pocus ponieważ to mogła być lista pythonowa
            to_json, # Hocus Pocus ponieważ to mogła być lista pythonowa
            interpelation_data['sentDate']
        )

        cursor.execute(query, values)
        connection.commit()
        print(f"Interpelation data inserted successfully: {interpelation_data['title']}")
    except Error as e:
        print (f"Error {e} while inserting interpelation data for : {interpelation_data['title']} ")

def updateClub():
    pass

# The mp table has a foreign key constraint that requires the club value to exist in the club table. 
def updateMP():
    connection = connect_to_mysql()
    if connection is None:
        return

    try:
        # Aktualnie na sztywno bo czemu nie, w przyszłości wrzucić do updateClub
        club_data = json.loads('''[{"email":"kp-ko@kluby.sejm.pl, prasowka@mail.platforma.org","fax":"(22) 694-26-36","id":"KO","membersCount":156,"name":"Klub Parlamentarny Koalicja Obywatelska - Platforma Obywatelska, Nowoczesna, Inicjatywa Polska, Zieloni","phone":""},{"email":"","fax":"(22) 694-29-31","id":"Konfederacja","membersCount":18,"name":"Klub Poselski Konfederacja","phone":""},{"email":"kp-lewica@kluby.sejm.pl","fax":"(22) 694-28-16","id":"Lewica","membersCount":26,"name":"Koalicyjny Klub Parlamentarny Lewicy (Nowa Lewica, PPS, Razem, Unia Pracy)","phone":""},{"email":"","fax":"(22) 694-15-34","id":"niez.","membersCount":1,"name":"Posłowie niezrzeszeni","phone":""},{"email":"kp-pis@kluby.sejm.pl","fax":"(22) 694-26-11","id":"PiS","membersCount":190,"name":"Klub Parlamentarny Prawo i Sprawiedliwość","phone":""},{"email":"kp-polska2050@kluby.sejm.pl","fax":"(22) 694-29-12","id":"Polska2050-TD","membersCount":32,"name":"Klub Parlamentarny Polska 2050 - Trzecia Droga","phone":""},{"email":"kp-psl@kluby.sejm.pl","fax":"(22) 694 23 21 ","id":"PSL-TD","membersCount":32,"name":"Klub Parlamentarny Polskie Stronnictwo Ludowe - Trzecia Droga","phone":""},{"email":"","fax":"","id":"Republikanie","membersCount":4,"name":"Koło Poselskie Wolni Republikanie","phone":""}]''')
        
        for club in club_data:
            insertClub(connection, club)

        # Then, insert MP data
        with open('MP.json', 'r', encoding='utf-8') as file:
            mp_list = json.load(file)
        
        for mp_data in tqdm(mp_list):
            insertMP(connection, mp_data)

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

def updateInterpelation():
    connection = connect_to_mysql()
    if connection is None:
        return

    try:
        with open('Model/interpellations.json', 'r', encoding='utf-8') as file:
            interpelation_list = json.load(file)

        for interpelation_data in interpelation_list:
            insertInterpelation(connection, interpelation_data)
            break
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
            
def main():
    # Invoke only those I'm working on
    updateInterpelation()

if __name__ == "__main__":
    main()