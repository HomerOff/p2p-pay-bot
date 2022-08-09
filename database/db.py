import sqlite3
import time


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def set_status(self, user_id, status):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `status` = ? WHERE `user_id` = ?", (status, user_id,))

    def get_status(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `status` FROM `users` WHERE `user_id` = ?",
                                         (user_id,)).fetchall()
            for row in result:
                status = row[0]
            return status

    def get_users(self):
        with self.connection:
            result = self.cursor.execute("SELECT user_id FROM users").fetchall()
            return result

    def get_count_users(self):
        with self.connection:
            result = self.cursor.execute("SELECT COUNT(*) from 'users'").fetchall()
            return result[0][0]

    def get_user_comment(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `user_comment` FROM `users` WHERE `user_id` = ?",
                                         (user_id,)).fetchone()
            return bool(result[0])

    def get_user_rating(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `user_rating` FROM `users` WHERE `user_id` = ?",
                                         (user_id,)).fetchone()
            return bool(result[0])

    def set_user_comment(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `user_comment` = ? WHERE `user_id` = ?", (True, user_id,))

    def set_user_rating(self, user_id, user_rating):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `user_rating` = ? WHERE `user_id` = ?",
                                       (user_rating, user_id,))

    def get_managers_id(self):
        with self.connection:
            result = self.cursor.execute("SELECT `manager_id` FROM `managers` WHERE `manager_at_work` = 1")
            managers = []

            for row in result.fetchall():
                managers.append(row[0])
            return managers

    def get_manager_name(self, manager_id):
        with self.connection:
            result = self.cursor.execute("SELECT `manager_name` FROM `managers` WHERE `manager_id` = ?",
                                         (manager_id,)).fetchone()
            return result[0]