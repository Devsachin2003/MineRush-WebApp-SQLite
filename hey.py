from flask import Flask, redirect, url_for, render_template, request, session, flash
import sqlite3
import re

app = Flask(__name__)
app.secret_key = "super secret key"

DATABASE = 'myapp.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Welcome
@app.route("/")
def welcome():
    return render_template("Welcome.html")

# User login session
@app.route('/Userlogin', methods=['GET', 'POST'])
def Userslogin():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM userstable WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['name'] = user['name']
            session['email'] = user['email']
            return redirect(url_for('home'))
        else:
            flash('Please enter correct email / password !')
            return redirect(url_for('Userslogin'))
    return render_template('User login.html', message=message)

# Admin login session
@app.route('/Alogin', methods=['GET', 'POST'])
def Adminslogin():
    m = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email, password)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admintable WHERE email = ? AND password = ?', (email, password))
        record = cursor.fetchone()

        if record:
            session['loggedin'] = True
            session['email'] = record['email']
            return redirect(url_for('admindashboard'))
        else:
            flash('Invalid email or password!')
    return render_template('Admin login.html', m=m)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('name', None)
    session.pop('email', None)
    return redirect(url_for('login_options'))

# Login options
@app.route("/Loginoptions")
def login_options():
    return render_template("Login options.html")

# Register
@app.route("/Register", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userdetails = request.form
        name = request.form['name']
        email = request.form['email']
        gender = request.form['gender']
        phone = userdetails['phone']
        username = userdetails['username']
        pwd = userdetails['password']
        pwd1 = userdetails['confirmpassword']
        role = userdetails['role']
        print(name, email, phone)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM userstable WHERE email=?", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            error = 'User with this email already exists!'
            return render_template('Sign-up.html', error=error)
        else:
            cursor.execute("INSERT INTO userstable (name, email, gender, phone, username, password, confirmpassword, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                           (name, email, gender, phone, username, pwd, pwd1, role))
            conn.commit()
            cursor.close()
            return redirect(url_for("login_options"))
    else:
        return render_template("Sign-up.html")

# Admin login page
@app.route("/Adminlogin")
def admin_login():
    return render_template("Admin login.html")

# User login
@app.route("/Userlogin")
def user_login():
    return render_template("User login.html")

# About
@app.route("/About")
def about():
    return render_template("About us.html")

# Contact us
@app.route("/Contactus")
def contact_us():
    return render_template("Contact_us.html")

# Admin homepage
@app.route("/Admindashboard")
def admindashboard():
    return render_template("Admin_homepage.html")

# User homepage
@app.route("/Userhomepage")
def home():
    return render_template("User_homepage.html")

# User instructions
@app.route("/User_instructions")
def user_instructions():
    return render_template("User_instructionpage.html")

# Feedback
@app.route("/Feedback")
def Feedback():
    return render_template("Feedback.html")

# Disclaimer
@app.route("/Disclaimer")
def Disclaimer():
    return render_template("Disclaimer.html")

# Rules and acts
@app.route("/Rulesandacts")
def Rulesandacts():
    return render_template("Rules_and_acts.html")

if __name__ == "__main__":
    app.run(debug=True)
