from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import errorcode

"""
classes:
1. Database
    a. create_database
    b. add_to_database
    c. connect_to_database
"""

class Database:
    def __init__(self, hostname):
        self.hostname = hostname

    def connect_to_database(self):
        load_dotenv()
        MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
        MYSQL_USER = os.getenv('MYSQL_USER')
        try: 
            print("Connecting to database")
            connection = mysql.connector.connect(host=self.hostname, user=MYSQL_USER, password=MYSQL_PASSWORD)
            self.connection = connection
            self.cursor = connection.cursor()
        except mysql.connector.Error as db_error:
            if db_error.errno == errorcode.CR_ALREADY_CONNECTED:
                pass
            elif db_error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error with username or password")

    def get_connection(self):
        return self.connection
    
    def get_cursor(self):
        return self.cursor

    def create_database(self, db_name):
        try:
            print(f"Creating database {db_name}")
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        except mysql.connector.DatabaseError as db_error:
            if db_error.errno == errorcode.ER_DB_CREATE_EXISTS:
                print(db_error)
            else: 
                print(db_error)

    def create_tables(self, db_name, table_name, tables_description, primary_key):
        try:
            self.cursor.execute("USE {}".format(db_name))
        except mysql.connector.ProgrammingError as db_error:
            print(f"{db_name} does not exist.")
            if db_error.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(db_name)
                print(f"Database {db_name} created.")
            else: 
                print(db_error)
        try:
            print("Crafting CREATE TABLES query")
            query = f"CREATE TABLE {table_name}("
            for description in tables_description:
                query += description[0] + " " + description[1] + " NOT NULL, "
            query += f"PRIMARY KEY ({primary_key}))"
            print(f"Creating table: {table_name}")
            self.cursor.execute(query)
        except mysql.connector.ProgrammingError as db_error:
            if db_error.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print(f"{table_name} already exists.")
            else: 
                print(db_error)
    
    def add_to_table(self, table_name, values):
        try:
            self.cursor.execute(f"USE {table_name}")
        except mysql.connector.ProgrammingError as db_error:
            print(f"{table_name} does not exist.")
            if db_error.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(table_name)
                print(f"Database test created.")
            else: 
                print(db_error)
        try:
            table_keys = list(values.keys())
            query = "INSERT INTO test(" + ", ".join(table_keys) + ")" + " VALUES ("
            for idx, value in enumerate(table_keys):
                if idx != len(table_keys) - 1:
                    query += f"%({value})s, "
                else: 
                    query += f"%({value})s) "
            print("Inserting into table")
            self.cursor.execute(query, values)
            # needed so it goes to the actual database or else it's just local essentially
            self.connection.commit()
        except mysql.connector.IntegrityError as db_error:
            print(db_error)
          
    def close_database_connection(self):
        self.connection.close()

