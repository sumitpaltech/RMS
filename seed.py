import os
import MySQLdb
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def seed_database():
    try:
        # Connect using .env credentials
        db = MySQLdb.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USERNAME'),
            passwd=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_DATABASE')
        )
        
        cursor = db.cursor()      
     
        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error while seeding: {e}")
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    seed_database()