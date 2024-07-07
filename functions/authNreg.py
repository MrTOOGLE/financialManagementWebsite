import sqlite3


def closeDB(cursor, db):
    cursor.close()
    db.close()
