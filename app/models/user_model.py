from app import mysql
from .base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):
    table = "users"

    @classmethod
    def find_by_email(cls, email):
        cur = cls.get_cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        return cur.fetchone()

    @classmethod
    def create(cls, name, email, password, role='user'):
        cur = cls.get_cursor()
        hashed = generate_password_hash(password)
        cur.execute("""
            INSERT INTO users (name, email, password, role, status, created_at, updated_at)
            VALUES (%s, %s, %s, %s, 1, NOW(), NOW())
        """, (name, email, hashed, role))
        mysql.connection.commit()
        return cur.lastrowid 
    
    @staticmethod
    def verify_password(stored_hash, plain_password):
        return check_password_hash(stored_hash, plain_password)
