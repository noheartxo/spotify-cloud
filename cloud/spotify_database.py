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
        try:
            self.cursor.execute("USE {}".format(db_name))
        except pymysql.Error as db_error:
            self.connection.rollback()
            logging.error(db_error)

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
    
    # values -> "['spotify:track:<id>']"
    def add_to_table(self, db_name: str, table_name: str, table_keys: list, values: list):
        try:
            self.use_database(db_name)
        except pymysql.Error as db_error:
            logging.error(f"{db_name} does not exist.")
        try:
            query = f"INSERT INTO {table_name} (" + ", ".join(table_keys) + ")" + " VALUES ("
            for idx in range(0, len(table_keys)-1):
                if idx != len(table_keys)-1:
                    query += f"%s, "
                else: 
                    query += f"%s) "
            values_tuple = [(n,) for n in values]
            logging.info("Inserting into table")
            self.cursor.executemany(query, values_tuple)
            # needed so it goes to the actual database or else it's just local essentially
            self.connection.commit()
        except pymysql.IntegrityError as db_error:
            self.connection.rollback()
            logging.error(db_error)
    
    def get_number_of_rows_in_table(self, db_name: str, table_name: str) -> int:
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

    def get_item_from_table(self, db_name: str, table_name: str) -> list:
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

    def delete_item_from_table(self, db_name: str, table_name: str, key: str, values: list) -> None:
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
