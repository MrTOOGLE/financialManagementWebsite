class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()

    def getUser(self, user_id):
        try:
            self.__cursor.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
            result = self.__cursor.fetchone()
            if not result:
                return False
            return result
        except sqlite3.Error as e:
            print(e)
        return False

    def getUserByMail(self, mail):
        try:
            self.__cursor.execute(f"SELECT * FROM users WHERE mail = '{mail}'")
            result = self.__cursor.fetchone()
            if not result:
                return False
            return result
        except sqlite3.Error as e:
            print(e)
        return False

    def addUser(self, mail, password, name, balance):
        try:
            self.__cursor.execute(f"SELECT COUNT() as `count` FROM users WHERE mail LIKE '{mail}'")
            res = self.__cursor.fetchone()
            if res['count'] > 0:
                return False
            self.__cursor.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?)", (mail, password, name, balance))
            self.__db.commit()
        except Exception as e:
            print("╰（‵□′）╯" + str(e))
            return False
        return True
