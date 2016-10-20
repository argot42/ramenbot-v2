import sqlite3

class DBM:
    """ Interface to interact with the database """

    def __init__(self, database, schema):
        with open(schema, 'r') as fp:
            self.connection = sqlite3.connect(database)

            try:
                self.connection.executescript(fp.read())
            except sqlite3.OperationalError:
                pass


    def query(self, query):
        return (self.connection.execute(query)).fetchall()


    def query_iter(self, query):
        cursor = self.connection.execute(query)

        while True:
            response = cursor.fetchone()
            if not response: break
            yield response

