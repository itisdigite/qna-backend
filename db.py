import mysql.connector
from mysql.connector import errorcode

def init_db():
    conn = None
    c = None
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host="localhost",
            user="qnauser",
            password="Pass@000"  # Replace with the actual password
        )
        c = conn.cursor()

        # Create the database if it doesn't exist
        c.execute(f"CREATE DATABASE IF NOT EXISTS qna")
        c.execute(f"USE qna")

        # Create users table - if not exists, with an added email column and verified column
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (username VARCHAR(255), password VARCHAR(255), email VARCHAR(255) UNIQUE, verified TINYINT DEFAULT 0, otc VARCHAR(6))''')
        
        # Create OTC table for storing one-time codes
        c.execute('''CREATE TABLE IF NOT EXISTS otc_codes
                     (email VARCHAR(255), code VARCHAR(6), expiry TIMESTAMP)''')
        
        conn.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        # Ensure c and conn are closed if they were initialized
        if c:
            c.close()
        if conn:
            conn.close()

init_db()
