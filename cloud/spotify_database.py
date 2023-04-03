import pymysql
import logging

class Database:
    def __init__(self, hostname, username, password):
        self.connect_to_database(hostname, username, password)

    def connect_to_database(self, hostname, username, password):
        try: 
            connection = pymysql.connect(host=hostname, user=username, password=password)
            self.connection = connection
            self.cursor = connection.cursor()
            logging.info("Created and established database connection")
        except pymysql.Error as db_error:
            logging.error(db_error)

    def get_connection(self):
        return self.connection
    
    def get_cursor(self):
        return self.cursor

    def use_database(self, db_name):
        self.cursor.execute(f"USE {db_name}")

    def create_database(self, db_name: str):
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            logging.info(f"Created database: {db_name}")
        except pymysql.Error as db_error:
            logging.error(db_error)

    # tables_description -> list of tuples e.g. [("<table value>", "VARCHAR(255)")]
    def create_tables(self, db_name: str, table_name: str, tables_description: list, primary_key: str):
        try:
            self.use_database(db_name)
        except pymysql.ProgrammingError as db_error:
            logging.error(f"{db_name} does not exist.")
        try:
            logging.info("Crafting CREATE TABLES query")
            query = f"CREATE TABLE {table_name}("
            for description in tables_description:
                query += description[0] + " " + description[1] + " NOT NULL, "
            query += f"PRIMARY KEY ({primary_key}))"
            logging.info(f"Creating table: {table_name}")
            self.cursor.execute(query)
        except pymysql.ProgrammingError as db_error:
            logging.error(db_error)
    
    # "values -> {\'uri\': 'spotify:track:<id>'}"
    def add_to_table(self, db_name: str, table_name: str, values: dict):
        try:
            self.use_database(db_name)
        except pymysql.Error as db_error:
            logging.error(f"{db_name} does not exist.")
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
        except pymysql.IntegrityError as db_error:
            logging.error(db_error)
    
    def get_number_of_rows_in_table(self, db_name, table_name):
        try:
            self.use_database(db_name)
        except pymysql.Error as db_error:
            logging.error(f"{db_name} does not exist.")
        try:
            query = f"SELECT * FROM {table_name}"
            number_of_rows = self.cursor.execute(query)
            return number_of_rows
        except pymysql.IntegrityError as db_error:
            logging.error(db_error)

    def get_item_from_table(self, db_name, table_name):
        try:
            self.use_database(db_name)
        except pymysql.Error as db_error:
            logging.error(f"{db_name} does not exist.")
        try:
            query = f"SELECT * FROM {table_name}"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except pymysql.IntegrityError as db_error:
            logging.error(db_error)

    def delete_tables(self, table_name: str) -> None:
        try:
            query = f"DROP TABLES IF EXISTS {table_name}"
            self.cursor.execute(query)
        except pymysql.Error as db_error:
            logging.error(db_error)

    def delete_item_from_table(self, db_name, table_name, key, values) -> None:
        try:
            self.use_database(db_name)
        except pymysql.Error as db_error:
            logging.error(f"{db_name} does not exist.")
        try: 
            query = f"DELETE FROM {table_name} WHERE {key}=%s"
            # executemany works best when given a list of tuples
            values_tuple = [(n,) for n in values]
            self.cursor.executemany(query, values_tuple)
            self.connection.commit()
        except pymysql.Error as db_error:
            logging.error(db_error)

    def close_database_connection(self):
        try:
            self.connection.close()
        except pymysql.Error as db_error:
            logging.error(db_error)
