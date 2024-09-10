import mysql.connector
from mysql.connector import errorcode

def init_db():
    conn = None
    c = None
    try:
        # Connect to MySQL server running inside the Docker container
        conn = mysql.connector.connect(
            host="localhost",                  # 'db' is the service name in docker-compose.yml
            user="qnauser",
            password="Pass@000",         # Replace with the actual password
            database="qna"               # Name of the database
        )
        c = conn.cursor()

        # Create users table
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
        if c:
            c.close()
        if conn:
            conn.close()

init_db()
