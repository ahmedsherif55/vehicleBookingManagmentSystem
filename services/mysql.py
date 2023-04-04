import pymysql as mysql
import pymysql.cursors as mysql_cursors
import datetime


class DBError(Exception):
    # Raised when there's a fatal database error
    pass


class DBTypeError(TypeError):
    # Raised when there's a database type error ('str', 'float', 'int', 'None', 'bool' and datetime.datetime)
    pass


class Database:
    _db_host = None
    _db_user = None
    _db_password = None
    _db_name = None
    _db_port = None
    _db = None
    _dbc = None
    _auto_commit = True
    _auto_reconnect = True

    def __init__(self, db_host, db_user, db_password, db_name, db_port=3306, auto_commit=True, auto_reconnect=True):
        self._db_host = db_host
        self._db_user = db_user
        self._db_password = db_password
        self._db_name = db_name
        self._db_port = db_port
        self._auto_commit = auto_commit
        self._auto_reconnect = auto_reconnect
        self._validate_configurations()
        try:
            self._db = mysql.connect(host=self._db_host, user=self._db_user, password=self._db_password,
                                     database=self._db_name, port=self._db_port)
            self._dbc = self._db.cursor(cursor=mysql_cursors.DictCursor)
            self._db.ping(reconnect=self._auto_reconnect)
        except Exception as e:
            raise DBError(f"Exception while trying to connect to the database: {e}")

    def _validate_configurations(self):
        if not isinstance(self._db_host, str):
            raise DBTypeError("Host for database must be of type 'str'.")
        if not isinstance(self._db_user, str):
            raise DBTypeError("User for database must be of type 'str'.")
        if not isinstance(self._db_password, str):
            raise DBTypeError("Password for database must be of type 'str'.")
        if not isinstance(self._db_name, str):
            raise DBTypeError("Name for database must be of type 'str'.")
        if not isinstance(self._db_port, int) or self._db_port < 0 or self._db_port > 65535:
            raise DBTypeError("Port for database must be of type string and set as (0<= int <= 65535).")
        if not isinstance(self._auto_commit, bool):
            raise DBTypeError("Auto commit param must be of type 'bool'.")
        if not isinstance(self._auto_reconnect, bool):
            raise DBTypeError("Auto reconnect param must be of type 'bool'.")

    def close(self):
        if self._db is not None:
            self._db.close()

    def insert(self, table, fields):
        length = len(fields)
        query = f"INSERT INTO {table} ("
        i = 0
        query_keys = ''
        query_values = ''
        for key in fields:
            i += 1
            key = self._db.escape(key)
            if isinstance(fields[key], str):
                fields[key] = self._db.escape(fields[key])
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
            self._dbc.execute(query)
            return True
        except Exception as e:
            print(e)
            return False

    def update(self, table, table_key, table_key_value, fields):
        length = len(fields)
        table_key_value = self._db.escape(table_key_value)
        query = f"UPDATE {table} SET "
        i = 0
        for key in fields:
            i += 1
            key = self._db.escape(key)
            if isinstance(fields[key], str):
                fields[key] = self._db.escape(fields[key])
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
            self._dbc.execute(query)
            if self._auto_commit:
                self._db.commit()
            return self._dbc.rowcount
        except Exception:
            return -1

    def delete(self, table, table_key, table_key_value):
        table_key_value = self._db.escape(table_key_value)
        query = f"DELETE FROM {table} WHERE {table_key} = {table_key_value}"
        try:
            self._dbc.execute(query)
            if self._auto_commit:
                self._db.commit()
            return self._dbc.rowcount
        except Exception:
            return -1

    def get_one(self, table, table_key, table_key_value):
        table_key_value = self._db.escape(table_key_value)
        query = f"SELECT * FROM {table} WHERE {table_key} = {table_key_value}"
        try:
            self._dbc.execute(query)
            if self._auto_commit:
                self._db.commit()
            record = self._dbc.fetchone()
            return record
        except Exception:
            return None