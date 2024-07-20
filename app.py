from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_login import LoginManager, login_required, logout_user
from werkzeug.utils import secure_filename
import os
import pymysql
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
import pymysql.cursors


app = Flask(__name__)
app.secret_key="super secret key"

# MySQL Configuration

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dev123'
app.config['MYSQL_DB'] = 'users'
app.config['SESSION_TYPE']='filesystem'
app.config['UPLOAD_FOLDER'] = 'F:\College\App module\MineRush Web app\bootstrap frontend\Webpages\static\Articles\rules and acts'
# Initialize MySQL
mysql = MySQL(app)

# File Upload Configuration

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = "static/Articles/rules and acts"
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'mp4'}

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    error = ''
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
            error='Please enter correct email / password !'
            
    return render_template('Admin login.html', error=error)

@app.route('/logout')
def logout(): 
    session.pop('loggedin', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route("/Alogout")
def Adminlogout():
    session.pop('loggedin', None)
    session.pop('email', None)
    return redirect(url_for('login'))

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
        organization = userdetails['organization']
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
            cur.execute("INSERT INTO userstable (name, email, gender, phone, username, password, confirmpassword, role, organization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                           (name, email, gender, phone, username, pwd, pwd1, role, organization))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for("login"))
    else:
        return render_template("Sign-up.html")
    
#Userprofiledisplay

@app.route('/Login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Check user table
        cursor.execute('SELECT * FROM userstable WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        
        if user:
            session['loggedin'] = True
            session['name'] = user['name']
            session['email'] = user['email']
            session['responsibility'] = 'user'
            return redirect(url_for('home'))
        
        # Check admin table
        cursor.execute('SELECT * FROM admintable WHERE email = %s AND password = %s', (email, password))
        admin = cursor.fetchone()
        
        if admin:
            session['loggedin'] = True
            session['email'] = admin['email']
            session['responsibility'] = 'admin'
            return redirect(url_for('admindashboard'))
        
        cursor.close()
        
    messages = 'Please enter correct email / password!'
        
    return render_template('Login.html', messages=messages)

@app.route('/Myprofile')
def profile():
    email = session.get('email')
    if not email:
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM userstable WHERE email = %s', (email,))
    user_details = cur.fetchone()
    cur.close()

    if not user_details:
        return "User not found", 404

    return render_template('My_profile.html', user=user_details)
        
        
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
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT name, email FROM userstable")
        users = cursor.fetchall()
        cursor.execute("SELECT name, email FROM internship_applications")
        applications = cursor.fetchall()
        cursor.close()
        return render_template("Admin_homepage.html",users=users,applications=applications)
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
    if 'loggedin' in session:
        return render_template("User_instructionpage.html")
    else:
        return redirect(url_for('user_login'))
@app.route("/Userhistory")
def userhistory():
    if 'loggedin' in session:
        return render_template("Userchathistory.html")
    else:
        return redirect(url_for('user_login'))
    
#Explore_internships

@app.route('/Explore_internships')
def explore_internships():
    if 'loggedin' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM internships")
        internships = cur.fetchall()
        print(internships)
        cur.close()
        return render_template('Explore_internships.html', internships=internships)
    else:
        return redirect(url_for('user_login'))

@app.route('/Internship_application_form')
def internship_application_form():
    if 'loggedin' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM internships")
        intern = cur.fetchall()
        cur.close()
        return render_template("Internship_application_form.html",intern=intern)
    else:
        return redirect(url_for('login'))

@app.route('/submit_application', methods=['GET', 'POST'])
def submit_application():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        gender = request.form['gender']
        dob = request.form['dob']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        degree_branch = request.form['degree_branch']
        year_of_study = request.form['year_of_study']
        company_name = request.form['company_name']
        skills = request.form['skills']
        internship_role=request.form['internship_role']
        
        # Handle file upload
        if 'resume' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        resume = request.files['resume']
        
        if resume.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        if resume and resume.filename.endswith('.pdf'):
            filename = secure_filename(resume.filename)
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume.save(resume_path)
            
            # Insert data into the database
            try:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query = """INSERT INTO internship_applications 
                           (name, gender, dob, phone, email, address, degree_branch, year_of_study, company_name, skills,internship_role, resume) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s)"""
                cursor.execute(query, (name, gender, dob, phone, email, address, degree_branch, year_of_study, company_name, skills,internship_role, resume))
                mysql.connection.commit()
                cursor.close()
                flash('Application submitted successfully!', 'success')
            except mysql.connection.Error as err:
                flash(f'Error: {err}', 'danger')
                return redirect(url_for('internship_application_form'))
            
            return redirect(url_for('internship_application_form'))
        else:
            flash('Only PDF files are allowed', 'danger')
            return redirect(request.url)
    
    return '''
    <form method="post" enctype="multipart/form-data">
        <input type="text" name="name" placeholder="Name">
        <input type="text" name="gender" placeholder="Gender">
        <input type="date" name="dob" placeholder="Date of Birth">
        <input type="text" name="phone" placeholder="Phone">
        <input type="email" name="email" placeholder="Email">
        <input type="text" name="address" placeholder="Address">
        <input type="text" name="degree_branch" placeholder="Degree Branch">
        <input type="text" name="year_of_study" placeholder="Year of Study">
        <input type="text" name="company_name" placeholder="Company Name">
        <input type="text" name="skills" placeholder="Skills">
        <input type="file" name="resume">
        <input type="submit" value="Submit">
    </form>
    '''

    
@app.route("/Disclaimer")
def Disclaimer():
    if 'loggedin' in session:
        return render_template("Disclaimer.html")
    else:
        return redirect(url_for('user_login'))
#Rulesandacts

@app.route("/Rulesandacts")
def Rulesandacts():
    if 'loggedin' in session:
        return render_template("Rules_and_acts.html")
    else:
        return redirect(url_for('user_login'))

@app.route("/Manage_users")
def manage():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM userstable")
        users = cursor.fetchall()
        cursor.close()
        return render_template('manage_users.html', users=users)
    else:
        return redirect(url_for("user_login"))

#delete user from userstable

@app.route('/delete_user/<email>', methods=['POST'])
def delete_user(email):
    try:
        # Create MySQL cursor
        cur = mysql.connection.cursor()

        # Execute query to delete user
        cur.execute("DELETE FROM users WHERE email = %s", (email,))

        # Commit changes to database
        mysql.connection.commit()

        # Close cursor
        cur.close()

        return redirect(url_for('manage'))  # Redirect to manage users page
    except Exception as e:
        return str(e)  # Handle exceptions as needed

@app.route("/Update_glossary")
def update_glossary():
    return render_template("/Update_glossary.html")
@app.route("/View_user_detailsD")
def view_user_detailsD():
    return render_template("/View_user_detailsD.html")
@app.route('/view_user_details')
def view_user_details():
    # Logic to handle user details view
    return render_template("/View_user_detailsD.html")
@app.route("/Add_faqs_admin")
def add_faqs_admin():
    return render_template("/Add_faqs_admin.html")

   
@app.route("/Glossary")
def Glossary():
    if 'loggedin' in session:
        return render_template("Glossary.html")
    else:
        return redirect(url_for('user_login'))
@app.route("/FAQs")
def openfaqs():
    if 'loggedin' in session:
        # Fetch FAQs from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT section, question, answer FROM faqs")
        faqs = cur.fetchall()
        cur.close()
        
        # Group FAQs by section
        faq_dict = {}
        for faq in faqs:
            section, question, answer = faq
            if section not in faq_dict:
                faq_dict[section] = []
            faq_dict[section].append({'question': question, 'answer': answer})
        
        return render_template("FAQs_user.html", faqs=faq_dict, enumerate=enumerate)
    else:
        return redirect(url_for('user_login'))
    
def update_user_details(email, name, username, role, gender, picture):
    try:
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
                UPDATE userstable
                SET name = %s, username = %s, role = %s, gender = %s, picture = %s
                WHERE email = %s
            """
        cursor.execute(sql, (name, username, role, gender, picture, email))
        mysql.connection.commit()
    finally:
        cursor.close()

def get_user_details(email):
    try:
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "SELECT * FROM userstable WHERE email = %s"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()
        return user
    finally:
        cursor.close()


@app.route("/Editprofile",methods=['GET','POST'])
def edit_user_profile():
    if 'loggedin' in session:
        if request.method == 'POST':
            # Handle form submission
            name = request.form['name']
            username = request.form['username']
            role = request.form['role']
            gender = request.form['gender']
            # Check if the post request has the file part
            picture_file = request.files.get('picture')
            if picture_file and allowed_file(picture_file.filename):
                picture_filename = secure_filename(picture_file.filename)
                picture_file.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_filename))
            else:
                picture_filename = None
            
            # Update user details in the database
            update_user_details(session['email'], name, username, role, gender, picture_filename )
            
            return redirect(url_for('profile'))
        
        # Get user details from the database
        user = get_user_details(session['email'])
        
        return render_template('Edituserprofile.html', user=user)
    else:
        return redirect(url_for("user_login"))

@app.route("/Upload_files",methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        rulename = request.form.get('rulename')
        description = request.form.get('description')
        video=request.form.get('video')
        

        # Handle document upload
        document_file = request.files.get('document')
        if document_file and allowed_file(document_file.filename):
            document_filename = secure_filename(document_file.filename)
            document_file.save(os.path.join(app.config['UPLOAD_FOLDER'], document_filename))
        else:
            document_filename = None

        # Insert file metadata into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO rulesandacts (rulename, video,description, document) VALUES (%s, %s, %s, %s)", (rulename, video,description, document_filename))
        mysql.connection.commit()
        cur.close()

        flash('Files uploaded successfully!', 'success')
        return redirect(url_for('upload_file'))

    return render_template('Upload_files.html')
    

       
        

        

@app.route("/Upload_doc")
def upload_document():
    return render_template("Upload_document.html")

@app.route("/Upload_video")
def upload_video():
    return render_template("Upload_video.html")

#display description
@app.route("/DisplayCMA1952")
def display_data1():
    if 'loggedin' in session:
        page = "Coal mines act, 1952"
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM rulesandacts WHERE rulename = %s", (page,))
        data = cur.fetchone()
        cur.close()

        if not data:
            return "Details not found", 404

        vid = data['video']
        desc = data['description']
        doc = data['document']  # Extracting description from the fetched data

        return render_template('cma_1952.html',vid=vid, desc=desc, doc=doc)
    else:
        return redirect(url_for('user_login'))

@app.route("/DisplayIEA1884")
def data():
    if 'loggedin' in session:
        page = "Indian explosives act, 1884"
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM rulesandacts WHERE rulename = %s", (page,))
        data = cur.fetchone()
        cur.close()

        if not data:
            return "Details not found", 404

        vid = data['video']
        desc = data['description']
        doc = data['document']  # Extracting description from the fetched data

        return render_template('Indian _explosives_act_1884.html', vid=vid, desc=desc, doc=doc)
    else:
        return redirect(url_for('user_login'))

@app.route("/DisplayCCO2000")
def display_data3():
    if 'loggedin' in session:
        page = "Colliery control act, 2000"
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM rulesandacts WHERE rulename = %s", (page,))
        data = cur.fetchone()
        cur.close()

        if not data:
            return "Details not found", 404

        vid = data['video']
        desc=data['description']
        doc=data['document'] # Extracting description from the fetched data

        return render_template('Colliery_control_order_2000.html', vid=vid, desc=desc, doc=doc)
    else:
        return redirect(url_for('user_login'))

@app.route("/DisplayCCO2004")
def display_data4():
    if 'loggedin' in session:
        page = "Colliery control act, 2004"
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM rulesandacts WHERE rulename = %s", (page,))
        data = cur.fetchone()
        cur.close()

        if not data:
           return "Details not found", 404

        vid = data['video']
        desc=data['description']
        doc=data['document'] # Extracting description from the fetched data

        return render_template('Colliery_control_order_2004.html',vid=vid, desc=desc, doc=doc )
    else:
        return redirect(url_for('user_login'))

@app.route("/DisplayCMR2017")
def display_data5():
    if 'loggedin' in session:
        page = "The coal mines regulations, 2017"
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM rulesandacts WHERE rulename = %s", (page,))
        data = cur.fetchone()
        cur.close()

        if not data:
            return "Details not found", 404

        vid = data['video']
        desc=data['description']
        doc=data['document'] # Extracting description from the fetched data

        return render_template('Coal_mines_regulations_2017.html',vid=vid, desc=desc, doc=doc  )
    else:
        return redirect(url_for('user_login'))

@app.route("/DisplayPaymentofwages1956")
def display_data6():
    if 'loggedin' in session:
        page = "Payment of wages(mines) rules, 1956"
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM rulesandacts WHERE rulename = %s", (page,))
        data = cur.fetchone()
        cur.close()

        if not data:
            return "Details not found", 404

        vid = data['video']
        desc=data['description']
        doc=data['document']# Extracting description from the fetched data

        return render_template('Payment_of_wages_1956.html', vid=vid, desc=desc, doc=doc)
    else:
        return redirect(url_for('user_login'))

@app.route("/DisplayCBAact1957")
def display_data7():
    if 'loggedin' in session:
        page = "CBA ACT, 1957"
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM rulesandacts WHERE rulename = %s", (page,))
        data = cur.fetchone()
        cur.close()

        if not data:
            return "Details not found", 404

        vid = data['video']
        desc=data['description']
        doc=data['document'] # Extracting description from the fetched data

        return render_template('CBA_1957.html',  vid=vid, desc=desc, doc=doc)
    else:
        return redirect(url_for('user_login'))
@app.route("/DisplayLandacquisition1894")
def display_data8():
    if 'loggedin' in session:
        page = "Land acquisition act, 1894"
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM rulesandacts WHERE rulename = %s", (page,))
        data = cur.fetchone()
        cur.close()

        if not data:
            return "Details not found", 404

        vid = data['video']
        desc=data['description']
        doc=data['document'] # Extracting  from the fetched data

        return render_template('Land_acquisition_act_1894.html',  vid=vid, desc=desc, doc=doc)
    else:
        return redirect(url_for('user_login'))

@app.route("/DisplayRandR")
def display_data9():
    if 'loggedin' in session:
        page = "R&R act, 2013"
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM rulesandacts WHERE rulename = %s", (page,))
        data = cur.fetchone()
        cur.close()

        if not data:
           return "Details not found", 404

        vid = data['video']
        desc=data['description']
        doc=data['document']# Extracting description from the fetched data

        return render_template('R&R act.html',vid=vid, desc=desc, doc=doc)
    else:
        return redirect(url_for('user_login'))


@app.route("/Adddescription",methods=['GET','POST'])
def adddescription():
    if 'loggedin' in session:
        if request.method == 'POST':
            page = request.form['page']
            description = request.form['description']
            cur=mysql.connection.cursor()
            
            # Insert into MySQL
            cur.execute("INSERT INTO description (page, description) VALUES (%s, %s)", (page, description))
            mysql.connection.commit()
            cur.close()
            flash('Description uploaded successfully!')
            return redirect(url_for("adddescription"))
        else:
            return render_template("Upload_description.html")
    else:
         return redirect(url_for('user_login'))

@app.route("/Add_Glossary",methods=['GET','POST'])
def add_glossary():
    if 'loggedin' in session:
        if request.method == 'POST':
            term = request.form['term']
            definition = request.form['definition']

            # Connect to MySQL database
            cur = mysql.connection.cursor()
            # Insert data into MySQL table
            insert_query = 'INSERT INTO glossary (term, definition) VALUES (%s, %s)'
            cur.execute(insert_query, (term, definition))
            mysql.connection.commit()
            cur.close()

            flash('Term added successfully!', 'success')
            return redirect(url_for('add_glossary'))

        return render_template("Update_glossary.html")
    else:
         return redirect(url_for('user_login'))

@app.route("/Displayglossary")
def display_glossary():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM glossary"
        cursor.execute(query)
        glossary_entries = cursor.fetchall()
        cursor.close()
    
        return render_template('Glossary.html', glossary_entries=glossary_entries)
    else:
        return redirect(url_for("user_login"))



@app.route("/Manage_internships")
def manage_internships():
    return render_template("Manage_internships.html")
@app.route("/Admin_internship_options")
def admin_internship_options():
    return render_template("/Admin_internship_options.html")
#adding an internship from admin side
@app.route("/Add_internship")
def add_intern():
    return render_template("Add_internship.html")
@app.route('/Add_intern_from_adminside', methods=['GET', 'POST'])
def Add_intern_from_adminside():
    if 'loggedin' in session:
        if request.method == 'POST':
            title = request.form['title']
            company = request.form['company']
            location = request.form['location']
            duration = request.form['duration']
            description = request.form['description']
            requirement = request.form['requirements']
            stipend = request.form['stipend']
            process = request.form['application_process']
            outcome = request.form['learning_outcomes']
            contact = request.form['contact_info']

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM internships WHERE title=%s", (title,))
            existing_internship = cur.fetchone()
            if existing_internship:
                flash('Internship title already exists!')
                return render_template('Add_internship.html')
            else:
                query = '''
                INSERT INTO internships (title, company, location, duration, description, requirements, stipend, application_process, learning_outcomes, contact_info)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                cur.execute(query, (title, company, location, duration, description, requirement, stipend, process, outcome, contact))
                mysql.connection.commit()
                cur.close()

                flash('Internship added successfully!')
                return redirect(url_for('Add_intern_from_adminside'))
        else:
            return render_template('Add_internship.html')
    else:
        return redirect(url_for("user_login"))
    
@app.route('/Add_faq', methods=['GET', 'POST'])
def Add_faq():
    if 'loggedin' in session:
        if request.method == 'POST':
            section = request.form['section']
            question = request.form['question']
            answer = request.form['answer']

            # Connect to MySQL database
            cur = mysql.connection.cursor()
            # Insert data into MySQL table
            insert_query = 'INSERT INTO faqs (section, question, answer) VALUES (%s, %s, %s)'
            cur.execute(insert_query, (section, question, answer))
            mysql.connection.commit()
            cur.close()

            flash('FAQ added successfully!', 'success')
            return redirect(url_for('Add_faq'))

        return render_template("Add_faqs_admin.html")
    else:
        return redirect(url_for("user_login"))


if __name__ == "__main__":
   app.run(debug=True)
