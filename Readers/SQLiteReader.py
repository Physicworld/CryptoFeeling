import sqlite3


class SQLiteReader:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, path_db):
        self.connection = sqlite3.connect(path_db)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def read(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()


