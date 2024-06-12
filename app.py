from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_login import LoginManager, login_required, logout_user
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)
app.secret_key="super secret key"

# MySQL Configuration

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dev123'
app.config['MYSQL_DB'] = 'users'
app.config['SESSION_TYPE']='filesystem'

# Initialize MySQL
mysql = MySQL(app)
#Welcome
@app.route("/")
def welcome():
    return render_template("Welcome.html")
#userloginsession
@app.route('/Userlogin', methods =['GET', 'POST'])
def Userslogin():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM userstable WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['name'] = user['name']
            session['email'] = user['email']
            return redirect(url_for('home'))
        else:
            flash('Please enter correct email / password !')
            return redirect(url_for('Userslogin'))
    return render_template('User login.html', message = message)

#Adminloginsession
@app.route('/Alogin', methods=['GET', 'POST'])
def Adminslogin():
    m = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email, password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admintable WHERE email = %s AND password = %s', (email, password))
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
    session.pop('email', None)
    return redirect(url_for('login_options'))

@app.route("/Alogout")
def Adminlogout():
    session.pop('loggedin', None)
    session.pop('email', None)
    return redirect(url_for('login_options'))

#Loginoptions
@app.route("/Loginoptions")
def login_options():
    return render_template("Login options.html")
#Register
@app.route("/Register", methods=['GET','POST'])
def signup():
    if request.method=='POST':
        userdetails=request.form
        name =request.form['name']
        email = request.form['email']
        gender = request.form['gender']
        phone = userdetails['phone']
        username =userdetails['username']
        pwd = userdetails['password']
        pwd1 = userdetails['confirmpassword']
        role = userdetails['role']
        print(name,email,phone)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM userstable WHERE email=%s", (email,))
        existing_user=cur.fetchone()
        cur.close()
        if existing_user:
            error = 'User with this email already exists!'
            return render_template('Sign-up.html', error=error)
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO userstable (name, email, gender, phone, username, password, confirmpassword, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                           (name, email, gender, phone, username, pwd, pwd1, role))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for("login_options"))
    else:
        return render_template("Sign-up.html")
    
#Userprofiledisplay
@app.route('/Myprofile/<email>')
def profile(email):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM userstable WHERE email = %s', (email,))
    userstable = cursor.fetchone()
    cursor.close()
    return render_template('Myprofile.html', userstable = userstable)
#Adminloginpage
@app.route("/Adminlogin")
def admin_login():
    return render_template("Admin login.html")
#Userlogin

@app.route("/Userlogin")
def user_login():
    return render_template("User login.html")
#about

@app.route("/About")
def about():
    return render_template("About us.html")
#contactus

@app.route("/Contactus")
def contact_us():
    return render_template("Contact_us.html")
#Adminhomepage

@app.route("/Admindashboard")
def admindashboard():
    if 'loggedin' in session:
        return render_template("Admin_homepage.html")
    return redirect(url_for('Adminslogin'))
#Userhomepage

@app.route("/Userhomepage")
def home():
    if 'loggedin' in session:
        return render_template("User_homepage.html")
    return redirect(url_for('user_login'))
#User_instructions

@app.route("/User_instructions")
def user_instructions():
    return render_template("User_instructionpage.html")
#Feedback

@app.route("/Feedback")
def Feedback():
    return render_template("Feedback.html")
#Disclaimer

@app.route("/Disclaimer")
def Disclaimer():
    return render_template("Disclaimer.html")
#Rulesandacts

@app.route("/Rulesandacts")
def Rulesandacts():
    return render_template("Rules_and_acts.html")
@app.route("/CMA_1952")
def cma_1952():
    return render_template("cma_1952.html")
@app.route("/IEA_1884")
def iea_1884():
    return render_template("Indian_explosive_act_1884.html")
@app.route("/CCO_2000")
def cco_2000():
    return render_template("Colliery_control_order_2000.html")
@app.route("/CCO_2004")
def cco_2004():
    return render_template("Colliery_control_order_2004.html")
@app.route("/CMR_2017")
def cmr_2017():
    return render_template("Coal_mines_regulations_2017.html")
@app.route("/Paymentofwages")
def Payment_of_wages():
    return render_template("Payment_of_wages_1956.html")
@app.route("/CBA_1957")
def cba_1957():
    return render_template("CBA_1957.html")
@app.route("/Land_acquisition_act")
def LAA_1894():
    return render_template("Land_acquisition_act_1894.html")
@app.route("/R&Ract")
def RandR():
    return render_template("R&R act.html")
@app.route("/Glossary")
def Glossary():
    return render_template("Glossary.html")

@app.route("/Editprofile")
def edit_profile():
    return render_template("Editprofile.html")

@app.route("/Add_file")
def add_file():
    return render_template("add_files.html")

@app.route("/Upload_doc")
def upload_document():
    return render_template("Upload_document.html")

@app.route("/Upload_video")
def upload_video():
    return render_template("Upload_video.html")

@app.route("/Upload_desc")
def upload_desc():
    return render_template("Upload_description.html")
@app.route("/Add_internship")
def add_intern():
    return render_template("Add_internship.html")
if __name__ == "__main__":
    app.run(debug=True)
