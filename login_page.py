from flask import Flask, request, render_template_string, render_template, redirect, url_for # type: ignore
import sqlite3
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import datetime




def init_db():
    conn = sqlite3.connect('credentials.db')
    c = conn.cursor()
    # Create users table - if not exists, with an added email column and verified column
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT, password TEXT, email TEXT UNIQUE, verified INTEGER DEFAULT 0, otc TEXT)''')
    # Create OTC table for storing one-time codes
    c.execute('''CREATE TABLE IF NOT EXISTS otc_codes
                 (email TEXT, code TEXT, expiry TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

def generate_and_send_otc(email):
    # Generate a random 6-digit code
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    expiry = datetime.datetime.now() + datetime.timedelta(minutes=10)  # 10 minutes from now

    # Store the code in the database
    conn = sqlite3.connect('credentials.db')
    c = conn.cursor()
    c.execute("INSERT INTO otc_codes (email, code, expiry) VALUES (?, ?, ?)", (email, code, expiry))
    conn.commit()
    conn.close()

    # Send the code via email
    sender_email = "noreply.codesend@gmail.com" # Your Sender email
    receiver_email = email
    password = "**************"  # Your Sender email password, It will be 16 digit app password
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your One-Time Code"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"Hi,\nYour one-time code is: {code}"
    part = MIMEText(text, "plain")
    message.attach(part)

    # Send email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


app = Flask(__name__, 
            static_folder='../qna-frontend/static', 
            template_folder='../qna-frontend/templates')

# Route for displaying the registration form
# @app.route("/register", methods=["GET"])
# def register_form():
#     return REGISTER_FORM

# Simple regex for basic email validation
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

# Route for handling the registration logic
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
        
        try:
            conn = sqlite3.connect('credentials.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, email, password, verified) VALUES (?, ?, ?, 0)", (username, email, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Email already registered."
        finally:
            conn.close()

        # Generate and send OTC
        generate_and_send_otc(email)

        return redirect(url_for('verify', email=email))

    return render_template('register.html')



# @app.route("/verify", methods=["GET"])
# def verify_form():
#     return VERIFY_FORM

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
    
    conn = sqlite3.connect('credentials.db')
    c = conn.cursor()
    c.execute("SELECT code, expiry FROM otc_codes WHERE email = ? ORDER BY expiry DESC LIMIT 1", (email,))
    result = c.fetchone()
    
    if result:
        stored_code, expiry = result
        expiry = datetime.datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S.%f")
        if stored_code == otc and datetime.datetime.now() < expiry:
            c.execute("UPDATE users SET verified = 1 WHERE email = ?", (email,))
            conn.commit()
            message = "Your email has been verified successfully."
        else:
            message = "Invalid or expired one-time code."
    else:
        message = "No code found for this email."
    
    conn.close()
    return message



# Route for handling the login logic
@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('credentials.db')
        c = conn.cursor()
        c.execute("SELECT password, verified FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        
        conn.close()
        
        if user:
            stored_password, verified = user
            if verified and stored_password == password:
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
    app.run(debug=True, port=8000)
