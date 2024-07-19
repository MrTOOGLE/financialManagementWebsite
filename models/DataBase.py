class DataBase:
    """Класс для работы с базой данных"""
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
        except Exception as e:
            print("(⊙x⊙;)" + str(e))
            return False

    def getUserByMail(self, mail):
        try:
            self.__cursor.execute(f"SELECT * FROM users WHERE mail = '{mail}'")
            result = self.__cursor.fetchone()
            if not result:
                return False
            return result
        except Exception as e:
            print("щ(゜ロ゜щ)" + str(e))
            return False

    def addUser(self, mail, password, name, balance):
        try:
            self.__cursor.execute(f"SELECT COUNT() as `count` FROM users WHERE mail LIKE '{mail}'")
            res = self.__cursor.fetchone()
            if res['count'] > 0:
                return False
            self.__cursor.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?)", (mail, password, name, balance))
            self.__db.commit()
            return True
        except Exception as e:
            print("╰（‵□′）╯" + str(e))
            return False

    def addOperations(self, id_user, category, type_operations, money, comment=""):
        try:
            self.__cursor.execute("""INSERT INTO financialOperations VALUES(?, ?, ?, ?, ?)""", (id_user, category, type_operations, money, comment))
            self.__db.commit()
            user = self.getUser(id_user)
            if type_operations == "expenses":
                money *= -1
            self.__cursor.execute(f"UPDATE users SET accountBalance = '{int(user[4]) + money}' WHERE mail = '{user[1]}'")
            self.__db.commit()
            return True
        except Exception as e:
            print("┗|｀O′|┛" + str(e))
            return False

    def getOperations(self, id_user):
        try:
            self.__cursor.execute(f"SELECT * FROM financialOperations WHERE id_user = '{id_user}'")
            result = self.__cursor.fetchall()
            return result
        except Exception as e:
            print("╚(•⌂•)╝" + str(e))
            return False
