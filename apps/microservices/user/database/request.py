import mariadb
from .database_error import DatabaseConnectionError, DatabaseQueryError

class Request:

    def __init__(self):
        # user .env
        self.config = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "mysql",
        "password": "velyb",
        "database": "velyb"
        }
        self.insert = self.manage_data
        self.update = self.manage_data
        self.delete = self.manage_data

    def start(self) :
        try :
            self.connect = mariadb.connect(**self.config)
            self.cursor = self.connect.cursor()
        except DatabaseConnectionError as e:
            print(f"Connection to database failed : {e}")

    def close(self) :
        self.cursor.close()
        self.connect.close()

    def exec(self, request, params):
        try :
            if not params is None and not isinstance(params, tuple):
                params = (params,)
            self.cursor.execute(request, params)
        except DatabaseQueryError as e:
            print(f"Database query failed : {e}")

    # Data read
    def select(self, request, params=None):
        self.start()
        self.exec(request, params)

        description = self.cursor.description
        results = self.cursor.fetchall()

        self.close()

        headers = list(map(lambda h: h[0], description))
        return list(map(lambda l: dict(zip(headers, l)), results))

    # Data manipulation (Create, Update, Delete)
    def manage_data(self, request, params=None):
        self.start()
        self.exec()
        self.connect.commit()
        self.close()