import pymysql as mysql
import datetime


class DBError(Exception):
    # Raised when there's a fatal database error
    pass


class DBTypeError(TypeError):
    # Raised when there's a database type error ('str', 'float', 'int', 'None', 'bool' and datetime.datetime)
    pass


class Database:
    db_host = None
    db_user = None
    db_password = None
    db_name = None
    db_port = None
    db = None
    dbc = None
    auto_commit = True
    auto_reconnect = True

    def __init__(self, db_host, db_user, db_password, db_name, db_port=3306, auto_commit=True, auto_reconnect=True):
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.db_port = db_port
        self.auto_commit = auto_commit
        self.auto_reconnect = auto_reconnect
        self.validate_configurations()
        try:
            self.db = mysql.connect(host=self.db_user, user=db_user,
                                    password=db_password, database=db_name, port=db_port)
            self.dbc = self.db.cursor()
            self.db.ping(reconnect=self.auto_reconnect)
        except Exception as e:
            raise DBError(f"Exception while trying to connect to the database: {e}")

    def validate_configurations(self):
        if not isinstance(self.db_host, str):
            raise DBTypeError("Host for database must be of type 'str'.")
        if not isinstance(self.db_user, str):
            raise DBTypeError("User for database must be of type 'str'.")
        if not isinstance(self.db_password, str):
            raise DBTypeError("Password for database must be of type 'str'.")
        if not isinstance(self.db_name, str):
            raise DBTypeError("Name for database must be of type 'str'.")
        if not isinstance(self.db_port, int) or self.db_port < 0 or self.db_port > 65535:
            raise DBTypeError("Port for database must be of type string and set as (0<= int <= 65535).")
        if not isinstance(self.auto_commit, bool):
            raise DBTypeError("Auto commit param must be of type 'bool'.")
        if not isinstance(self.auto_reconnect, bool):
            raise DBTypeError("Auto reconnect param must be of type 'bool'.")

    def close(self):
        if self.db is not None:
            self.db.close()

    def insert(self, table, fields):
        length = len(fields)
        table = self.db.escape(table)
        query = f"INSERT INTO {table} ("
        i = 0
        query_keys = ''
        query_values = ''
        for key in fields:
            i += 1
            key = self.db.escape(key)
            if isinstance(fields[key], str):
                fields[key] = self.db.escape(fields[key])
                query_keys += f"{key}"
                query_values += f"'{fields[key]}'"
            elif isinstance(fields[key], int) or isinstance(fields[key], float) or isinstance(fields[key], bool):
                query_keys += f"{key}"
                query_values += f"{fields[key]}"
            elif fields[key] is None:
                query_keys += f"{key}"
                query_values += f"NULL"
            elif isinstance(fields[key], datetime.datetime):
                query_keys += f"{key}"
                query_values += f"'{fields[key].strftime('%Y%m%d%H%M%S')}'"
            else:
                raise DBTypeError(
                    "Fields value must be of type 'int', 'float', 'bool', 'str', 'datetime.datetime' or 'None'.")
            if i != length:
                query_keys += ","
                query_values += ","
        try:
            query += query_keys + ") VALUES (" + query_values + ")"
            self.dbc.execute(query)
            return True
        except Exception as e:
            print(e)
            return False

    def update(self, table, table_key, table_key_value, fields):
        length = len(fields)
        table = self.db.escape(table)
        query = f"UPDATE {table} SET "
        i = 0
        for key in fields:
            i += 1
            key = self.db.escape(key)
            if isinstance(fields[key], str):
                fields[key] = self.db.escape(fields[key])
                query += f"{key} = '{fields[key]}'"
            elif isinstance(fields[key], int) or isinstance(fields[key], float) or isinstance(fields[key], bool):
                query += f"{key} = {fields[key]}"
            elif isinstance(fields[key], datetime.datetime):
                query += f"{fields[key].strftime('%Y%m%d%H%M%S')}"
            elif fields[key] is None:
                query += f"{key} = NULL"
            else:
                raise DBTypeError(
                    "Fields value must be of type 'int', 'float', 'bool', 'str',"
                    "'datetime.datetime' or 'None'.")
            if i != length:
                query += ","
        query += f" WHERE {table_key} = {table_key_value}"
        try:
            self.dbc.execute(query)
            if self.auto_commit:
                self.db.commit()
            return self.dbc.rowcount
        except Exception:
            return -1

    def delete(self, table, table_key, table_key_value):
        table = self.db.escape(table)
        table_key = self.db.escape(table_key)
        query = f"DELETE FROM {table} WHERE {table_key} = {table_key_value}"
        try:
            self.dbc.execute(query)
            if self.auto_commit:
                self.db.commit()
            return self.dbc.rowcount
        except Exception:
            return -1

    def get_one(self, table, table_key, table_key_value):
        table = self.db.escape(table)
        table_key = self.db.escape(table_key)
        query = f"SELECT * FROM {table} WHERE {table_key} = {table_key_value}"
        try:
            self.dbc.execute(query)
            if self.auto_commit:
                self.db.commit()
            record = self.dbc.fetchone()
            return list(record)
        except Exception:
            return None
