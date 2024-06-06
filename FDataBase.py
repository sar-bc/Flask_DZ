import time
import sqlite3
import math
import re
from flask import url_for, flash, session


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        sql = "SELECT * FROM mainmenu"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except IOError:
            print("Ошибка чтения из БД")
        return []

    def add_curs(self, title, url, body, price):
        try:
            self.__cur.execute("SELECT COUNT() as `count` FROM cursy WHERE url LIKE ?", (url,))
            res = self.__cur.fetchone()
            if res['count'] > 0:
                flash("Статья с таким url уже существует", category="error")
                # print("Статья с таким url уже существует")
                return False

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO cursy VALUES (NULL, ?, ?, ?, ?, ?)", (title, url, body, price, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False
        return True

    def get_curses(self):
        try:
            self.__cur.execute("SELECT id, title, url, price, body FROM cursy ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статей из БД " + str(e))

        return []

    def get_curs(self, slug):
        try:
            self.__cur.execute(f"SELECT title, price, body FROM cursy WHERE url='{slug}'")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи в БД " + str(e))

        return False, False
