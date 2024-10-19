#import streamlit as st
#from Controller.vote import get_vote
#from Controller.MP import 
import json
import mysql.connector
from mysql.connector import Error

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

def execute_select_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error executing query: {e}")
        return None

def main():
    connection = connect_to_mysql()
    if connection is None:
        return

    try:
        query = """
        SELECT firstLastName
        FROM mp
        WHERE active = true
        ORDER BY firstLastName;
        """
        
        results = execute_select_query(connection, query)
        
        if results:
            print("Active MPs:")
            for row in results:
                print(row[0])
        else:
            print("No results found or an error occurred.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    main()

