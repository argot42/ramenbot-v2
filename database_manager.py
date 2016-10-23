import sqlite3

class DBM:
    """ Interface to interact with the database """

    def __init__(self, db, schema):
        with open(schema, 'r') as fp:
            self.database = db

            connection = sqlite3.connect(self.database)
            try:
                connection.executescript(fp.read())
            except sqlite3.OperationalError:
                pass

    def query(self, query, args=tuple()):
        connection = sqlite3.connect(self.database)

        try:
            response = (connection.execute(query, args)).fetchall()
        except:
            raise

        connection.commit()
        connection.close()
        return response



    def query_iter(self, query, args=tuple()):
        connection = sqlite3.connect(self.database)
        cursor = connection.execute(query, args)

        while True:
            response = cursor.fetchone()
            if not response: break
            yield response

        connection.close()

