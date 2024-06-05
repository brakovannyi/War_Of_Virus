import sqlite3
class Database():
    def __init__(self):
        self.connect = None

    def connection(self):
        try:
            self.connect = sqlite3.connect('war_of_virus')
        except:
            return

    def create(self):
        cursor = self.connect.cursor()
        sql = ("CREATE TABLE IF NOT EXISTS users("
               "id INT AUTO_INCREMENT PRIMARY KEY,"
               "login TEXT, "
               "password TEXT)")
        cursor.execute(sql)
        self.connect.commit()

    def writes(self, login, password):
        cursor = self.connect.cursor()
        line = (login, password)
        sql = ("INSERT INTO users(login, password)"
               "VALUES (?, ?)")
        cursor.execute(sql, line)
        self.connect.commit()

    def check(self, login, password):
        cursor = self.connect.cursor()
        sql = (f"SELECT login, password FROM users WHERE login = '{login}'")
        cursor.execute(sql)
        try:
            login_, password_ = cursor.fetchone()
        except:
            login_, password_ = None, None
        print(login_, password_)
        if password_ == password:
            return True
        else:
            return False

    def check_new_acc(self, login, password):
        cursor = self.connect.cursor()
        sql = (f"SELECT login FROM users WHERE login = '{login}'")
        cursor.execute(sql)
        login_ = cursor.fetchone()
        print(login_, login)
        if login_ == None:
            return True
        if login_[0] == login:
            return False
        else:
            return True
