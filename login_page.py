from flask import Flask, request, render_template, redirect, url_for # type: ignore
import mysql.connector
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import datetime
import bcrypt
from db import init_db  # Import the init_db function

# Initialize the database before starting the app
init_db()

app = Flask(__name__, 
            static_folder='../qna-frontend/static', 
            template_folder='../qna-frontend/templates')

def get_db_connection():
    return mysql.connector.connect(
        user='qnauser',
        password='your_qnauser_password',  # Replace with your actual password
        host='db',  # Use the service name 'db'
        database='qna'
    )


def generate_and_send_otc(email):
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    expiry = datetime.datetime.now() + datetime.timedelta(minutes=10)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO otc_codes (email, code, expiry) VALUES (%s, %s, %s)", (email, code, expiry))
    conn.commit()
    conn.close()

    sender_email = "noreply.codesend@gmail.com" # Your Sender email
    receiver_email = email
    password = "kemg ypms ajpu hloc"  # Your Sender email password
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your One-Time Code"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"Hi,\nYour one-time code is: {code}"
    part = MIMEText(text, "plain")
    message.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
        except KeyError:
            return "Missing form data", 400
        
        if not is_valid_email(email):
            return "Invalid email format", 400
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password, verified) VALUES (%s, %s, %s, 0)", (username, email, hashed_password))
            conn.commit()
        except mysql.connector.IntegrityError:
            return "Email already registered."
        finally:
            conn.close()

        generate_and_send_otc(email)

        return redirect(url_for('verify', email=email))

    return render_template('register.html')

@app.route("/verify", methods=['GET'])
def verify():
    email = request.args.get('email')
    return render_template('verification.html', email=email)

@app.route("/verify_code", methods=['POST'])
def verify_code():
    email = request.form.get('email')
    otc = request.form.get('otc')
    
    if not email or not otc:
        return "Email and one-time code are required."
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT code, expiry FROM otc_codes WHERE email = %s ORDER BY expiry DESC LIMIT 1", (email,))
    result = cursor.fetchone()
    
    if result:
        stored_code, expiry = result
        if stored_code == otc and datetime.datetime.now() < expiry:
            cursor.execute("UPDATE users SET verified = 1 WHERE email = %s", (email,))
            conn.commit()
            message = "Your email has been verified successfully."
        else:
            message = "Invalid or expired one-time code."
    else:
        message = "No code found for this email."
    
    conn.close()
    return message

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password, verified FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        conn.close()
        
        if user:
            stored_password, verified = user
            stored_password = stored_password.encode('utf-8')  # Convert the stored password to bytes
            
            if verified and bcrypt.checkpw(password.encode('utf-8'), stored_password):
                return "Login successful!"
            elif not verified:
                return "Email not verified."
            else:
                return "Invalid email or password."
        else:
            message = 'Please enter correct email / password!'
        return render_template('login.html', message=message)
    else:
        return render_template('login.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
