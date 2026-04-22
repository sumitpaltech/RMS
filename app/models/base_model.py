from app import mysql


class BaseModel:
    """
    Base model — all models extend this.
    Works like Laravel's DB facade / Eloquent base.
    """
    table = ""

    @staticmethod
    def get_cursor():
        return mysql.connection.cursor()

    @classmethod
    def all(cls):
        cur = cls.get_cursor()
        cur.execute(f"SELECT * FROM {cls.table}")
        return cur.fetchall()

    @classmethod
    def find(cls, id):
        cur = cls.get_cursor()
        cur.execute(f"SELECT * FROM {cls.table} WHERE id = %s", (id,))
        return cur.fetchone()

    @classmethod
    def delete(cls, id):
        cur = cls.get_cursor()
        cur.execute(f"DELETE FROM {cls.table} WHERE id = %s", (id,))
        mysql.connection.commit()
        return cur.rowcount
