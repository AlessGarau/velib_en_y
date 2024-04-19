import mariadb
from .database_error import DatabaseConnectionError, DatabaseQueryError, DatabaseEmptyResultError

class Request:

    def __init__(self):
        # user .env
        self.config = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "",
        "database": "velyb"
        }
        self.insert = self.manage_data
        self.update = self.manage_data
        self.delete = self.manage_data

    def start(self) :
        try :
            self.connect = mariadb.connect(**self.config)
            self.cursor = self.connect.cursor()
        except mariadb.OperationalError as e:
            print(f"Connection to database failed : {e}")
            raise DatabaseConnectionError(f"Connection to database failed : {e}") from e

    def close(self) :
        self.cursor.close()
        self.connect.close()

    def exec(self, request, params):
        try :
            if not params is None and not isinstance(params, tuple):
                params = (params,)
            self.cursor.execute(request, params)
        except BaseException as e:
            print(f"Database query failed : {e}")
            raise DatabaseQueryError(f"Database query failed : {e}") from e

    # Data read
    def select(self, request, params=None):
        self.start()
        self.exec(request, params)

        description = self.cursor.description
        results = self.cursor.fetchall()

        self.close()

        headers = list(map(lambda h: h[0], description))
        response = list(map(lambda l: dict(zip(headers, l)), results))
        if len(response) > 0:
            return response
        else:
            raise DatabaseEmptyResultError("Empty result")

    # Data manipulation (Create, Update, Delete)
    def manage_data(self, request, params=None):
        self.start()
        self.exec(request, params)
        if (self.cursor.rowcount > 0):
            self.connect.commit() 
            self.close()
        else:
            raise DatabaseQueryError("No data was affected")