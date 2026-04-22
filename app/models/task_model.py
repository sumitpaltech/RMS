from app import mysql
from .base_model import BaseModel

class Task(BaseModel):
    table = "task_tracker"

    @classmethod
    def all_with_user(cls):
        """Join task_tracker with users based on the 'assigned_to' column"""
        cur = cls.get_cursor()
        cur.execute("""
            SELECT task_tracker.*, users.name AS user_name
            FROM task_tracker
            LEFT JOIN users ON task_tracker.assigned_to = users.email
            ORDER BY task_tracker.created_at DESC
        """)
        return cur.fetchall()

    @classmethod
    def by_user(cls, user_email):
        """Finds tasks where 'assigned_to' matches the user's email"""
        cur = cls.get_cursor()
        cur.execute("""
            SELECT * FROM task_tracker 
            WHERE assigned_to = %s
        """, [user_email])
        
        tasks = cur.fetchall()
        return tasks

    @classmethod
    def create(cls, data):
        """
        Expects a dictionary matching your schema:
        title, description, category, assigned_to, priority, start_date, due_date, status, remarks
        """
        cur = cls.get_cursor()
        cur.execute("""
            INSERT INTO task_tracker (
                title, description, category, assigned_to, priority, 
                start_date, due_date, status, remarks, created_at, updated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """, (
            data['title'], data['description'], data['category'], 
            data['assigned_to'], data['priority'], data['start_date'], 
            data['due_date'], data['status'], data['remarks']
        ))
        mysql.connection.commit()
        return cur.lastrowid

    @classmethod
    def update_status(cls, task_id, new_status, completion_date=None):
        """Updates status and optionally sets completion_date"""
        cur = cls.get_cursor()
        cur.execute("""
            UPDATE task_tracker
            SET status=%s, completion_date=%s, updated_at=NOW()
            WHERE id=%s
        """, (new_status, completion_date, task_id))
        mysql.connection.commit()
        return cur.rowcount
    
    @classmethod
    def count_by_status(cls, assigned_to_value):
        """
        Counts tasks grouped by their status for a specific user.
        Uses 'assigned_to' to match your schema.
        """
        cur = cls.get_cursor()
        cur.execute("""
            SELECT status, COUNT(*) as total
            FROM task_tracker 
            WHERE assigned_to = %s
            GROUP BY status
        """, (assigned_to_value,))
        return cur.fetchall()
    @classmethod
    def find(cls, id):
        cur = cls.get_cursor()
        cur.execute("SELECT * FROM task_tracker WHERE id = %s", (id,))
        return cur.fetchone()
    