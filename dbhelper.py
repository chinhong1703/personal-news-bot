import os
import psycopg2


class DBHelper:
    def __init__(self):
        self.dbname = os.environ['DATABASE_URL']
        self.conn = psycopg2.connect(self.dbname, sslmode='require')
        self.cursor = self.conn.cursor()

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
        itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)"
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        self.cursor.execute(tblstmt)
        self.cursor.execute(itemidx)
        self.cursor.execute(ownidx)
        self.conn.commit()

    def add_item(self, item_text, owner):
        stmt = "INSERT INTO items (description, owner) VALUES (%s, %s)"
        args = (item_text, owner)
        self.cursor.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text, owner):
        stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
        args = (item_text, owner)
        self.cursor.execute(stmt, args)
        self.conn.commit()

    def get_items(self, owner):
        stmt = "SELECT description FROM items WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.cursor.execute(stmt, args)]
