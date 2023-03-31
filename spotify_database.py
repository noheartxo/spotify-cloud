import os
import mysql.connector
import logging
from dotenv import load_dotenv
from mysql.connector import errorcode

logging = logging.getLogger().setLevel(logging.INFO)

class Database:
    def __init__(self, hostname):
        self.hostname = hostname
        self.connect_to_database()

    def connect_to_database(self):
        load_dotenv()
        MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
        MYSQL_USER = os.getenv('MYSQL_USER')
        try: 
            connection = mysql.connector.connect(host=self.hostname, user=MYSQL_USER, password=MYSQL_PASSWORD)
            self.connection = connection
            self.cursor = connection.cursor()
            logging.info("Created and established database connection")
        except mysql.connector.Error as db_error:
            if db_error.errno == errorcode.CR_ALREADY_CONNECTED:
                pass
            elif db_error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.error("Error with username or password")

    def get_connection(self):
        return self.connection
    
    def get_cursor(self):
        return self.cursor

    def create_database(self, db_name: str):
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            logging.info(f"Created database: {db_name}")
        except mysql.connector.DatabaseError as db_error:
            if db_error.errno == errorcode.ER_DB_CREATE_EXISTS:
                logging.error(db_error)
            else: 
                logging.error(db_error)

    # tables_description -> list of tuples e.g. [("<table value>", "VARCHAR(255)")]
    def create_tables(self, db_name: str, table_name: str, tables_description: list, primary_key: str):
        try:
            self.cursor.execute("USE {}".format(db_name))
        except mysql.connector.ProgrammingError as db_error:
            logging.error(f"{db_name} does not exist.")
            if db_error.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(db_name)
                logging.info(f"Database {db_name} created.")
            else: 
                logging.error(db_error)
        try:
            logging.info("Crafting CREATE TABLES query")
            query = f"CREATE TABLE {table_name}("
            for description in tables_description:
                query += description[0] + " " + description[1] + " NOT NULL, "
            query += f"PRIMARY KEY ({primary_key}))"
            logging.info(f"Creating table: {table_name}")
            self.cursor.execute(query)
        except mysql.connector.ProgrammingError as db_error:
            if db_error.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                logging.error(f"{table_name} already exists.")
            else: 
                logging.error(db_error)
    
    # "values -> {\'uri\': 'spotify:track:<id>'}"
    def add_to_table(self, db_name: str, table_name: str, values: dict):
        try:
            self.cursor.execute(f"USE {db_name}")
        except mysql.connector.ProgrammingError as db_error:
            logging.error(f"{table_name} does not exist.")
            if db_error.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(table_name)
                logging.info(f"Database {table_name} created.")
            else: 
                logging.error(db_error)
        try:
            table_keys = list(values.keys())
            query = f"INSERT INTO {table_name}(" + ", ".join(table_keys) + ")" + " VALUES ("
            for idx, value in enumerate(table_keys):
                if idx != len(table_keys) - 1:
                    query += f"%({value})s, "
                else: 
                    query += f"%({value})s) "
            logging.info("Inserting into table")
            self.cursor.execute(query, values)
            # needed so it goes to the actual database or else it's just local essentially
            self.connection.commit()
        except mysql.connector.IntegrityError as db_error:
            logging.error(db_error)
    
    def delete_tables(self, table_name: str):
        try:
            query = f"DROP TABLES IF EXISTS {table_name}"
            self.cursor.execute(query)
        except mysql.connector.Error as db_error:
            logging.error(db_error)

    def delete_item_from_table(self):
        pass

    def close_database_connection(self):
        self.connection.close()

