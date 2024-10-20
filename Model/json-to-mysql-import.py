import json
import mysql.connector
from mysql.connector import Error
from mysql.connector.errors import IntegrityError
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
        #print(f"Club data inserted/updated successfully: {club_data['name']}")
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
            mp_data['club'],
            mp_data['districtName'], 
            mp_data['districtNum'],
            mp_data['firstLastName'], 
            mp_data['firstName'], 
            mp_data['genitiveName'],
            mp_data.get('term'),
            mp_data['lastFirstName'], 
            mp_data['lastName'], 
            mp_data['numberOfVotes'],
            mp_data.get('profession', 'Unknown'),
            mp_data.get('secondName'), 
            mp_data['voivodeship'],
            mp_data['email'], 
            mp_data['educationLevel']
        )
        
        cursor.execute(query, values)
        connection.commit()
        #print(f"MP data inserted successfully: {mp_data['firstLastName']}")
    except Error as e:
        print(f"Error while inserting MP data for {mp_data['firstLastName']}: {e}")

def insertInterpelation(connection, interpelation_data):
    try:
        cursor = connection.cursor()
        query = """INSERT INTO interpellation (id, term, num, title, receiptDate, lastModified, `from`, `to`, sentDate) 
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        from_json = json.dumps(interpelation_data['from']) if isinstance(interpelation_data['from'], list) else interpelation_data['from']
        to_json = json.dumps(interpelation_data['to']) if isinstance(interpelation_data['to'], list) else interpelation_data['to']

        values = (
            interpelation_data['num'],
            interpelation_data['term'],
            interpelation_data['num'],
            interpelation_data['title'],
            interpelation_data['receiptDate'],
            interpelation_data['lastModified'],
            from_json,
            to_json,
            interpelation_data.get('sentDate', '2137-04-01')
        )

        cursor.execute(query, values)
        connection.commit()
        #print(f"Interpelation data inserted successfully: {interpelation_data['title']}")
    except IntegrityError:
        pass
    except Error as e:
        print(f"Error {e} while inserting interpelation data for: {interpelation_data['title']}")

def insertTerm(connection, term_data):
    try:
        cursor = connection.cursor()
        query = """INSERT INTO terms (num, from_date, to_date, current) 
                   VALUES (%s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE
                   from_date = VALUES(from_date), 
                   to_date = VALUES(to_date), 
                   current = VALUES(current)"""
        
        values = (
            term_data['num'],
            term_data['from'],
            term_data.get('to'),  # 'to' might be None for the current term
            term_data['current']
        )
        
        cursor.execute(query, values)
        connection.commit()
        #print(f"Term data inserted/updated successfully: Term {term_data['num']}")
    except Error as e:
        print(f"Error while inserting term data: {e}")

def updateClub():
    connection = connect_to_mysql()
    if connection is None:
        return

    try:
        with open("Data/clubs.json", 'r', encoding='utf-8') as file:
            clubs_list = json.load(file)
        for club in tqdm(clubs_list):
            insertClub(connection, club)
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
def updateMP():
    connection = connect_to_mysql()
    if connection is None:
        return

    try:
        with open('Data/MP.json', 'r', encoding='utf-8') as file:
            mp_list = json.load(file)
        
        for mp_data in mp_list:
            insertMP(connection, mp_data)
            break

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
        with open('Data/interpellations.json', 'r', encoding='utf-8') as file:
            interpelation_list = json.load(file)

        for interpelation_data in tqdm(interpelation_list):
            insertInterpelation(connection, interpelation_data)
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

def updateTerms():
    connection = connect_to_mysql()
    if connection is None:
        return

    try:
        with open('Data/terms.json', 'r', encoding='utf-8') as file:
            terms_data = json.load(file)
        #terms_data = json.loads('''[{"current":false,"from":"1993-10-14","num":2,"to":"1997-10-19"},{"current":false,"from":"1997-10-20","num":3,"to":"2001-10-18"},{"current":false,"from":"2001-10-19","num":4,"prints":{"count":0,"link":"/term4/prints"},"to":"2005-10-18"},{"current":false,"from":"2005-10-19","num":5,"prints":{"count":0,"link":"/term5/prints"},"to":"2007-11-04"},{"current":false,"from":"2007-11-05","num":6,"prints":{"count":0,"link":"/term6/prints"},"to":"2011-11-07"},{"current":false,"from":"2011-11-08","num":7,"prints":{"count":4356,"lastChanged":"2024-06-18T03:34:50","link":"/term7/prints"},"to":"2015-11-11"},{"current":false,"from":"2015-11-12","num":8,"prints":{"count":4362,"lastChanged":"2024-06-19T03:35:57","link":"/term8/prints"},"to":"2019-11-11"},{"current":false,"from":"2019-11-12","num":9,"prints":{"count":4142,"lastChanged":"2024-07-06T03:36:08","link":"/term9/prints"},"to":"2023-11-12"},{"current":true,"from":"2023-11-13","num":10,"prints":{"count":802,"lastChanged":"2024-10-18T15:28:51","link":"/term10/prints"}}]''')
        
        for term in tqdm(terms_data):
            insertTerm(connection, term)

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

def main():
    #updateTerms()
    #updateClub()
    #updateMP() # This does not handle updates yet Error while inserting MP data for Andrzej Adamczyk: 1062 (23000): Duplicate entry '1' for key 'PRIMARY'
    #updateInterpelation()
    pass

if __name__ == "__main__":
    main()