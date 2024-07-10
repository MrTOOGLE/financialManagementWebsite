import sqlite3


def closeDB(cursor, db):
    cursor.close()
    db.close()


def getUser(mail):
    try:
        db = sqlite3.connect('users.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM passwords WHERE mail = '{mail}';")
        result = cursor.fetchone()
        closeDB(cursor, db)
        if not result:
            return False
        return result
    except Exception as e:
        pass
    return False
