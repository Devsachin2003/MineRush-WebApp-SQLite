from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
import sqlite3
import json
import os
from flask_mail import Mail,Message
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

import google.generativeai as genai
load_dotenv()
app = Flask(__name__)
app.secret_key = "super secret key"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Get email from environment variable
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Get password from environment variable
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')  # Default sender email

mail = Mail(app)

# SQLite database path
DB_PATH = 'users.db'

# File Upload Configuration
app.config['UPLOAD_FOLDER'] = "static/Articles/rules and acts"
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load API key
if os.path.exists("api_key.json"):
    try:
        # Read the api_key.json file
        with open("api_key.json", "r") as file:
            data = json.load(file)
            api_key = data.get("key")  # Safely retrieve the API key from the JSON data

            # If the key doesn't exist in the file, handle it
            if not api_key:
                raise KeyError("API key 'key' not found in the JSON file.")
        
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error loading API key: {e}")
        api_key = None  # Set api_key to None if there's an error
else:
    print("Warning: api_key.json not found.")
    api_key = None  # Set api_key to None if the file doesn't exist

# Check if API key is available
if api_key:
    # Configure the genai client with the API key
    genai.configure(api_key=api_key)

    # Define the generation configuration for the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Initialize the model with required configuration
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="The chatbot should answer queries specifically related to mining laws...",
    )

else:
    print("API key is required to configure the model.")
    
def send_message(message, history):
    history.append({"role": "user", "parts": message})
    chat = model.start_chat(history=history)
    response = chat.send_message(message)
    history.append({"role": "model", "parts": response.text})
    return response.text, history

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def render_act_page(page, template_name):
    if 'loggedin' not in session:
        return redirect(url_for("Userslogin"))

    print(f"[DEBUG] Requested page: {page}")
    
    row = fetch_act_data(page)
    print(f"[DEBUG] Fetched data: {row}")

    if not row:
        return f"Details not found for page: {page}", 404

    data = dict(row)  # Convert sqlite3.Row to dict

    return render_template(
        template_name,
        vid=data.get('video', ''),
        desc=data.get('description', ''),
        doc=data.get('document', '')
    )




@app.route("/")
def welcome():
    return render_template("Welcome.html")

@app.route('/Userlogin', methods=['GET', 'POST'])
def Userslogin():
    message = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM userstable WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()
        if user:
            session['loggedin'] = True
            session['name'] = user['name']
            session['email'] = user['email']
            return redirect(url_for('home'))
        else:
            flash('Please enter correct email / password !')
            return redirect(url_for('Userslogin'))
    return render_template('User login.html', message=message)

@app.route('/Alogin', methods=['GET', 'POST'])
def Adminslogin():
    error = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM admintable WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()
        if admin:
            session['loggedin'] = True
            session['email'] = admin['email']
            return redirect(url_for('admindashboard'))
        else:
            error = 'Please enter correct email / password !'
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

@app.route("/Loginoptions")
def login_options():
    return render_template("Login options.html")

@app.route("/Register", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        gender = request.form['gender']
        phone = request.form['phone']
        username = request.form['username']
        organization = request.form['organization']
        pwd = request.form['password']
        pwd1 = request.form['confirmpassword']
        role = request.form['role']

        conn = get_db_connection()
        existing_user = conn.execute("SELECT * FROM userstable WHERE email = ?", (email,)).fetchone()
        if existing_user:
            conn.close()
            error = 'User with this email already exists!'
            return render_template('Sign-up.html', error=error)
        else:
            conn.execute("INSERT INTO userstable (name, email, gender, phone, username, password, confirmpassword, role, organization) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                        (name, email, gender, phone, username, pwd, pwd1, role, organization))
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
    else:
        return render_template("Sign-up.html")

@app.route('/Login', methods=['GET', 'POST'])
def login():
    messages = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM userstable WHERE email = ? AND password = ?', (email, password)).fetchone()
        if user:
            session['loggedin'] = True
            session['name'] = user['name']
            session['email'] = user['email']
            session['responsibility'] = 'user'
            conn.close()
            return redirect(url_for('home'))

        admin = conn.execute('SELECT * FROM admintable WHERE email = ? AND password = ?', (email, password)).fetchone()
        if admin:
            session['loggedin'] = True
            session['email'] = admin['email']
            session['responsibility'] = 'admin'
            conn.close()
            return redirect(url_for('admindashboard'))
        conn.close()
        messages = 'Please enter correct email / password!'
    return render_template('Login.html', messages=messages)

@app.route('/Myprofile')
def profile():
    email = session.get('email')
    if not email:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user_details = conn.execute('SELECT * FROM userstable WHERE email = ?', (email,)).fetchone()
    conn.close()

    if not user_details:
        return "User not found", 404

    return render_template('My_profile.html', user=user_details)

# Admin login page
@app.route("/Adminlogin")
def admin_login():
    return render_template("Admin login.html")

# User login page
@app.route("/Userlogin")
def user_login():
    return render_template("User login.html")

# About page
@app.route("/About")
def about():
    return render_template("About us.html")

# Contact us page
@app.route("/Contactus")
def contact_us():
    return render_template("Contact_us.html")

# Admin homepage
@app.route("/Admindashboard")
def admindashboard():
    if 'loggedin' in session:
        conn = get_db_connection()
        users = conn.execute("SELECT name, email FROM userstable").fetchall()
        applications = conn.execute("SELECT name, email FROM internship_applications").fetchall()
        conn.close()
        return render_template("Admin_homepage.html", users=users, applications=applications)
    return redirect(url_for('Userslogin'))

# Admin profile
@app.route('/Adminmyprofile')
def adminprofile():
    email = session.get('email')
    if not email:
        return redirect(url_for('login'))

    conn = get_db_connection()
    admin_details = conn.execute('SELECT * FROM admintable WHERE email = ?', (email,)).fetchone()
    conn.close()

    if not admin_details:
        return "User not found", 404

    return render_template('Admin_myprofile.html', admin=admin_details)

@app.route('/View_recent_registered_user/<string:name>')
def view_profile(name):
    if 'loggedin' in session:
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM userstable WHERE name = ?", (name,)).fetchone()
        conn.close()
        
        if user:
            # Normalize the picture filename and make sure it's passed correctly
            picture_filename = user['picture'].replace('\\', '/').strip()

            user_data = {
                'picture': picture_filename,
                'name': user['name'],
                'username': user['username'],
                'gender': user['gender'],
                'phone': user['phone'],
                'email': user['email'],
                'organization': user['organization'],
                'role': user['role']
            }

            print("DEBUG: Picture filename = ", picture_filename)  # Optional debug

            return render_template('View_recently_registered_user.html', user=user_data)
        else:
            return "User not found", 404
    return redirect(url_for('Userslogin'))


# User homepage
@app.route("/Userhomepage")
def home():
    if 'loggedin' in session:
        email = session['email']
        conn = get_db_connection()
        intern = conn.execute("SELECT * FROM internship_applications WHERE email = ?", (email,)).fetchone()
        conn.close()

        if intern:
            status = intern['status']
            name = intern['name']
            return render_template("User_homepage.html", name=name, status=status)
        else:
            # No application found yet
            return render_template("User_homepage.html", name=session.get('name'), status="No application submitted")

    return redirect(url_for('Userslogin'))


# User instructions page
@app.route("/User_instructions")
def user_instructions():
    if 'loggedin' in session:
        return render_template("User_instructionpage.html")
    else:
        return redirect(url_for('Userslogin'))

# User chat history
@app.route("/Userhistory")
def userhistory():
    if 'loggedin' in session:
        return render_template("Userchathistory.html")
    else:
        return redirect(url_for('Userslogin'))

# Explore internships
@app.route('/Explore_internships')
def explore_internships():
    if 'loggedin' in session:
        conn = get_db_connection()
        internships = conn.execute("SELECT * FROM internships").fetchall()
        conn.close()
        return render_template('Explore_internships.html', internships=internships)
    else:
        return redirect(url_for('Userslogin'))

@app.route('/Internship_application_form')
def internship_application_form():
    if 'loggedin' in session:
        conn = get_db_connection()
        intern = conn.execute("SELECT * FROM internships").fetchall()
        conn.close()
        return render_template("Internship_application_form.html", intern=intern)
    else:
        return redirect(url_for('Userslogin'))

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
        internship_role = request.form['internship_role']
        
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

            try:
                conn = get_db_connection()
                query = """INSERT INTO internship_applications 
                           (name, gender, dob, phone, email, address, degree_branch, year_of_study, company_name, skills, internship_role, resume) 
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                conn.execute(query, (
                    name, gender, dob, phone, email, address,
                    degree_branch, year_of_study, company_name, skills,
                    internship_role, filename
                ))
                conn.commit()
                conn.close()
                flash('Application submitted successfully!', 'success')
            except Exception as err:
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
        <input type="text" name="internship_role" placeholder="Internship Role">
        <input type="file" name="resume">
        <input type="submit" value="Submit">
    </form>
    '''

@app.route("/Disclaimer")
def Disclaimer():
    if 'loggedin' in session:
        return render_template("Disclaimer.html")
    else:
        return redirect(url_for('Userslogin'))

@app.route("/Rulesandacts")
def Rulesandacts():
    if 'loggedin' in session:
        return render_template("Rules_and_acts.html")
    else:
        return redirect(url_for('Userslogin'))

@app.route("/Manage_users", methods=['GET'])
def manage():
    if 'loggedin' in session:
        conn = get_db_connection()
        users = conn.execute("SELECT * FROM userstable").fetchall()
        conn.close()
        return render_template('manage_users.html', users=users)
    else:
        return redirect(url_for("user_login"))
@app.route('/delete_user', methods=['POST'])
def delete_user():
    try:
        data = request.get_json()

        if not data or 'email' not in data:
            return jsonify({"error": "Email is required"}), 400

        email = data['email']

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM userstable WHERE email = ?", (email,)).fetchone()

        if user:
            conn.execute("DELETE FROM userstable WHERE email = ?", (email,))
            conn.commit()
            message = f"User with email {email} has been deleted."
            status_code = 200
        else:
            message = "User not found"
            status_code = 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()

    return jsonify({"message": message}), status_code


@app.route('/View_recent_intern_applicant/<string:name>')
def view_intern(name):
    if 'loggedin' in session:
        conn = get_db_connection()
        intern = conn.execute("SELECT * FROM internship_applications WHERE name = ? AND status = 'Pending'", (name,)).fetchone()
        conn.close()

        if not intern:
            return "This application is either not found or already processed.", 404

        intern_data = {
            'name': intern['name'],
            'username': intern['email'],
            'gender': intern['gender'],
            'dob': intern['dob'],
            'phone': intern['phone'],
            'email': intern['email'],
            'address': intern['address'],
            'degree_branch': intern['degree_branch'],
            'company_name': intern['company_name'],
            'organization': intern['company_name'],
            'year_of_study': intern['year_of_study'],
            'skills': intern['skills'],
            'internship_role': intern['internship_role'],
            'resume': intern['resume'],
            'status': intern['status']
        }
        return render_template('View_recent_intern_application.html', intern=intern_data)
    return redirect(url_for('Userslogin'))


@app.route('/approve/<string:name>')
def approve(name):
    conn = get_db_connection()
    conn.execute("UPDATE internship_applications SET status = 'Approved' WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    return redirect(url_for('admindashboard'))

@app.route('/cancel/<string:name>')
def cancel(name):
    conn = get_db_connection()
    conn.execute("UPDATE internship_applications SET status = 'Cancelled' WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    return redirect(url_for('admindashboard'))

@app.route("/Update_glossary")
def update_glossary():
    if 'loggedin' in session:
        return render_template("Update_glossary.html")
    return redirect(url_for('Userslogin'))


@app.route("/View_user_detailsD")
def view_user_detailsD():
    return render_template("/View_user_detailsD.html")


@app.route('/view_user_details')
def view_user_details():
    if 'loggedin' in session:
        return render_template("/View_user_detailsD.html")
    return redirect(url_for('Userslogin'))


@app.route("/Add_faqs_admin")
def add_faqs_admin():
    if 'loggedin' in session:
        return render_template("/Add_faqs_admin.html")
    return redirect(url_for('Userslogin'))


@app.route("/Glossary")
def Glossary():
    if 'loggedin' in session:
        return render_template("Glossary.html")
    else:
        return redirect(url_for('Userslogin'))


@app.route("/FAQs")
def openfaqs():
    if 'loggedin' in session:
        conn = get_db_connection()
        faqs = conn.execute("SELECT section, question, answer FROM faqs").fetchall()
        conn.close()

        # Group FAQs by section
        faq_dict = {}
        for faq in faqs:
            section, question, answer = faq['section'], faq['question'], faq['answer']
            if section not in faq_dict:
                faq_dict[section] = []
            faq_dict[section].append({'question': question, 'answer': answer})

        return render_template("FAQs_user.html", faqs=faq_dict, enumerate=enumerate)
    else:
        return redirect(url_for('Userslogin'))

def update_user_details(email, name, username, role, gender, picture):
    conn = sqlite3.connect('users.db')  # Use correct DB
    try:
        cursor = conn.cursor()

        # ✅ Add this check
        cursor.execute("PRAGMA table_info(userstable)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'picture' not in columns:
            cursor.execute("ALTER TABLE userstable ADD COLUMN picture TEXT")

        cursor.execute("""
            UPDATE userstable
            SET name = ?, username = ?, role = ?, gender = ?, picture = ?
            WHERE email = ?
        """, (name, username, role, gender, picture, email))

        conn.commit()
    finally:
        conn.close()



def update_admin_details(email, name, username, role, gender, picture):
    conn = sqlite3.connect('users.db')
    try:
        cursor = conn.cursor()

        # ✅ Check if 'picture' column exists
        cursor.execute("PRAGMA table_info(admintable)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'picture' not in columns:
            cursor.execute("ALTER TABLE admintable ADD COLUMN picture TEXT")

        # ✅ Proceed with the update
        sql = """
            UPDATE admintable
            SET name = ?, username = ?, role = ?, gender = ?, picture = ?
            WHERE email = ?
        """
        cursor.execute(sql, (name, username, role, gender, picture, email))
        conn.commit()
    finally:
        conn.close()



def get_user_details(email):
    conn = get_db_connection()
    try:
        sql = "SELECT * FROM userstable WHERE email = ?"
        user = conn.execute(sql, (email,)).fetchone()
        return user
    finally:
        conn.close()


def get_admin_details(email):
    conn = get_db_connection()
    try:
        sql = "SELECT * FROM admintable WHERE email = ?"  # corrected
        user = conn.execute(sql, (email,)).fetchone()
        return user
    finally:
        conn.close()


@app.route("/Editprofile", methods=['GET', 'POST'])
def edit_user_profile():
    if 'loggedin' not in session:
        return redirect(url_for("Userslogin"))

    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        role = request.form['role']
        gender = request.form['gender']

        picture_file = request.files.get('picture')
        picture_filename = None

        if picture_file and allowed_file(picture_file.filename):
            picture_filename = secure_filename(picture_file.filename)
            picture_path = os.path.join(app.config['UPLOAD_FOLDER'], picture_filename)
            picture_file.save(picture_path)
        else:
            existing_user = get_user_details(session['email'])
            picture_filename = existing_user.get('picture') if existing_user else None

        update_user_details(session['email'], name, username, role, gender, picture_filename)
        return redirect(url_for('profile'))

    user = get_user_details(session['email'])
    return render_template('Edituserprofile.html', user=user)


@app.route("/Admineditprofile", methods=['GET', 'POST'])
def edit_admin_profile():
    if 'loggedin' not in session:
        return redirect(url_for("user_login"))

    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        role = request.form['role']
        gender = request.form['gender']

        picture_file = request.files.get('picture')
        picture_filename = None

        if picture_file and allowed_file(picture_file.filename):
            picture_filename = secure_filename(picture_file.filename)
            picture_path = os.path.join(app.config['UPLOAD_FOLDER'], picture_filename)
            picture_file.save(picture_path)
        else:
            # If picture not uploaded, retain the existing one
            existing_admin = get_admin_details(session['email'])
            picture_filename = existing_admin.get('picture') if existing_admin and 'picture' in existing_admin else None

        # ✅ Safe update with column check inside this function
        update_admin_details(session['email'], name, username, role, gender, picture_filename)
        return redirect(url_for('profile'))

    admin = get_admin_details(session['email'])
    return render_template('Admin_editprofile.html', admin=admin)




@app.route("/Upload_files", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        rulename = request.form.get('rulename')
        description = request.form.get('description')
        video = request.form.get('video')

        document_file = request.files.get('document')
        if document_file and allowed_file(document_file.filename):
            document_filename = secure_filename(document_file.filename)
            document_file.save(os.path.join(app.config['UPLOAD_FOLDER'], document_filename))
        else:
            document_filename = None

        conn = get_db_connection()
        conn.execute("INSERT INTO rulesandacts (rulename, video, description, document) VALUES (?, ?, ?, ?)", 
                     (rulename, video, description, document_filename))
        conn.commit()
        conn.close()

        flash('Files uploaded successfully!', 'success')
        return redirect(url_for('upload_file'))

    return render_template('Upload_files.html')
@app.route("/Upload_doc")
def upload_document():
    return render_template("Upload_document.html")


@app.route("/Upload_video")
def upload_video():
    return render_template("Upload_video.html")


def fetch_act_data(page_name):
    conn = get_db_connection()
    try:
        query = "SELECT * FROM rulesandacts WHERE rulename = ?"
        data = conn.execute(query, (page_name,)).fetchone()
        return data
    finally:
        conn.close()

@app.route("/DisplayCMA1952")
def display_data1():
    return render_act_page("Coal mines act, 1952", "cma_1952.html")

@app.route("/DisplayIEA1884")
def display_data2():
    return render_act_page("Indian explosives act, 1884", "Indian _explosives_act_1884.html")

@app.route("/DisplayCCO2000")
def display_data3():
    return render_act_page("Colliery control act, 2000", "Colliery_control_order_2000.html")

@app.route("/DisplayCCO2004")
def display_data4():
    return render_act_page("Colliery control act, 2004", "Colliery_control_order_2004.html")

@app.route("/DisplayCMR2017")
def display_data5():
    return render_act_page("The coal mines regulations, 2017", "Coal_mines_regulations_2017.html")

@app.route("/DisplayPaymentofwages1956")
def display_data6():
    return render_act_page("Payment of wages(mines) rules, 1956", "Payment_of_wages_1956.html")

@app.route("/DisplayCBAact1957")
def display_data7():
    return render_act_page("CBA ACT, 1957", "CBA_1957.html")

@app.route("/DisplayLandacquisition1894")
def display_data8():
    return render_act_page("Land acquisition act, 1894", "Land_acquisition_act_1894.html")

@app.route("/DisplayRandR")
def display_data9():
    return render_act_page("R&R act, 2013", "R&R act.html")  # <- renamed HTML file (must match your templates folder)


@app.route("/Adddescription", methods=['GET', 'POST'])
def adddescription():
    if 'loggedin' in session:
        if request.method == 'POST':
            page = request.form['page']
            description = request.form['description']

            conn = get_db_connection()
            conn.execute("INSERT INTO description (page, description) VALUES (?, ?)", (page, description))
            conn.commit()
            conn.close()

            flash('Description uploaded successfully!')
            return redirect(url_for("adddescription"))
        else:
            return render_template("Upload_description.html")
    else:
        return redirect(url_for('user_login'))


@app.route("/Add_Glossary", methods=['GET', 'POST'])
def add_glossary():
    if 'loggedin' in session:
        if request.method == 'POST':
            term = request.form['term']
            definition = request.form['definition']

            conn = get_db_connection()
            conn.execute("INSERT INTO glossary (term, definition) VALUES (?, ?)", (term, definition))
            conn.commit()
            conn.close()

            flash('Term added successfully!', 'success')
            return redirect(url_for('add_glossary'))

        return render_template("Update_glossary.html")
    else:
        return redirect(url_for('user_login'))


@app.route("/Displayglossary")
def display_glossary():
    if 'loggedin' in session:
        conn = get_db_connection()
        glossary_entries = conn.execute("SELECT * FROM glossary").fetchall()
        conn.close()

        return render_template('Glossary.html', glossary_entries=glossary_entries)
    else:
        return redirect(url_for("Userslogin"))


@app.route("/Manage_internships")
def manage_internships():
    return render_template("Manage_internships.html")


@app.route("/Admin_internship_options")
def admin_internship_options():
    return render_template("/Admin_internship_options.html")


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

            conn = get_db_connection()
            existing_internship = conn.execute("SELECT * FROM internships WHERE title = ?", (title,)).fetchone()

            if existing_internship:
                conn.close()
                flash('Internship title already exists!')
                return render_template('Add_internship.html')
            else:
                insert_query = '''
                    INSERT INTO internships (
                        title, company, location, duration, description, requirements, stipend,
                        application_process, learning_outcomes, contact_info
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                conn.execute(insert_query, (title, company, location, duration, description,
                                            requirement, stipend, process, outcome, contact))
                conn.commit()
                conn.close()

                flash('Internship added successfully!')
                return redirect(url_for('Add_intern_from_adminside'))
        else:
            return render_template('Add_internship.html')
    else:
        return redirect(url_for("Userslogin"))
@app.route('/Add_faq', methods=['GET', 'POST'])
def Add_faq():
    if 'loggedin' in session:
        if request.method == 'POST':
            section = request.form['section']
            question = request.form['question']
            answer = request.form['answer']

            conn = get_db_connection()
            insert_query = 'INSERT INTO faqs (section, question, answer) VALUES (?, ?, ?)'
            conn.execute(insert_query, (section, question, answer))
            conn.commit()
            conn.close()

            flash('FAQ added successfully!', 'success')
            return redirect(url_for('Add_faq'))

        return render_template("Add_faqs_admin.html")
    else:
        return redirect(url_for("Userslogin"))


@app.route("/bot")
def index():
    if 'loggedin' in session:
        return render_template("chat1.html")
    return redirect(url_for('Userslogin'))


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    history = request.json.get('history')
    response, history = send_message(user_message, history)
    return jsonify({'message': response, "history": history})


if __name__ == "__main__":
    app.run(debug=True)
