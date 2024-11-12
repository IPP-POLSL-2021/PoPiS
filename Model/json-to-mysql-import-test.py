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

def updateInterpelation():
    connection = connect_to_mysql()
    if connection is None:
        return

    try:
        with open('Data/interpellations.json', 'r', encoding='utf-8') as file:
            interpelation_list = json.load(file)

        interpelation_values = []
        for interpelation_data in tqdm(interpelation_list):
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
            interpelation_values.append(values)

        # Batch insert/update using executemany
        query = """INSERT INTO interpellation (id, term, num, title, receiptDate, lastModified, `from`, `to`, sentDate) 
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   ON DUPLICATE KEY UPDATE
                   term = VALUES(term), 
                   title = VALUES(title), 
                   receiptDate = VALUES(receiptDate), 
                   lastModified = VALUES(lastModified),
                   `from` = VALUES(`from`), 
                   `to` = VALUES(`to`), 
                   sentDate = VALUES(sentDate)"""

        cursor = connection.cursor()
        cursor.executemany(query, interpelation_values)
        connection.commit()
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
    updateInterpelation()
    pass

if __name__ == "__main__":
    main()