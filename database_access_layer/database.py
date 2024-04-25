import os
import mysql.connector
from mysql.connector import Error


def connect_to_database():
    """
    Establishes a connection to the MySQL database.
    """

    try:
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        database = os.getenv('DB_DATABASE')

        if not all((host, user, password, database)):
            print("Connection failed, set env variables: DB_HOST, DB_USER, DB_PASSWORD, and DB_DATABASE.")
            return None

        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print("Connection successfull")
        return connection
    except Error as e:
        print(f"Connection failed: {e}")
        return None


def close_connection(connection):
    """
    Closes the connection to the database.
    """
    if connection:
        connection.close()
        print("Connection to the database closed.")
