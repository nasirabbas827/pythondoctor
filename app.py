from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from googletrans import Translator

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Set admin_logged_in to False initially
admin_logged_in = False

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crawl_db'

mysql = MySQL(app)

from flask import session


# Function to search for diseases based on the search query and retrieve relevant information
def search_diseases(query):
    cur = mysql.connection.cursor()
    sql = """
    SELECT diseases.id, diseases.disease_name, diseases.symptoms, diseases.precautions, 
           relevant_information.doctor_name, relevant_information.doctor_advice, 
           relevant_information.doctor_phone, relevant_information.precautions
    FROM diseases
    LEFT JOIN relevant_information ON diseases.id = relevant_information.disease_id
    WHERE diseases.disease_name LIKE %s OR diseases.symptoms LIKE %s OR diseases.precautions LIKE %s
    """
    cur.execute(sql, ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    results = cur.fetchall()
    cur.close()
    return results

# Route for index page with search functionality
@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    if request.method == 'POST':
        search_query = request.form['search_query']
        if search_query:
            # Translate the search query to Urdu
            search_query_urdu = translate_to_urdu(search_query)
            # Search for diseases based on the translated search query
            results = search_diseases(search_query_urdu)
            # Display top 5 recommendations
            recommendations = results[:5] if results else []
    return render_template('index.html', recommendations=recommendations)

@app.route('/admin/adminlogin', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if username and password match with records in database
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password))
        admin = cur.fetchone()
        cur.close()
        if admin:
            # Set admin_logged_in to True in the session upon successful login
            session['admin_logged_in'] = True
            # Redirect to admin dashboard
            return redirect(url_for('admin_dashboard'))
        else:
            # If login unsuccessful, display error message
            error = 'Invalid credentials. Please try again.'
    return render_template('admin_login.html', error=error)

# Function to fetch diseases data from the database
def get_diseases():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM diseases')
    diseases = cur.fetchall()
    cur.close()
    return diseases


@app.route('/admin/dashboard')
def admin_dashboard():
    # Check if admin is logged in
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    # Fetch diseases data from the database
    diseases = get_diseases()
    return render_template('admin_dashboard.html', diseases=diseases)

translator = Translator()

# Function to translate English to Urdu
def translate_to_urdu(text):
    translation = translator.translate(text, src='en', dest='ur')
    return translation.text

@app.route('/admin/add_disease', methods=['GET', 'POST'])
def add_disease():
    # Check if admin is logged in
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Get data from the form
        disease_name = request.form['disease_name']
        symptoms = request.form['symptoms']
        precautions = request.form['precautions']
        prevention_methods = request.form['prevention_methods']
        medication = request.form['medication']
        
        # Translate English data to Urdu
        disease_name_urdu = translate_to_urdu(disease_name)
        symptoms_urdu = translate_to_urdu(symptoms)
        precautions_urdu = translate_to_urdu(precautions)
        prevention_methods_urdu = translate_to_urdu(prevention_methods)
        medication_urdu = translate_to_urdu(medication)
        
        # Store the data in the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO diseases (disease_name, symptoms, precautions, prevention_methods, medication) VALUES (%s, %s, %s, %s, %s)", (disease_name_urdu, symptoms_urdu, precautions_urdu, prevention_methods_urdu, medication_urdu))
        mysql.connection.commit()
        cur.close()
        
        flash('Disease added successfully', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_disease.html')


@app.route('/admin/edit_disease/<int:disease_id>', methods=['GET', 'POST'])
def edit_disease(disease_id):
    # Check if admin is logged in
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get updated data from the form
        updated_data = {
            'disease_name': request.form['disease_name'],
            'symptoms': request.form['symptoms'],
            'precautions': request.form['precautions'],
            'prevention_methods': request.form['prevention_methods'],
            'medication': request.form['medication']
        }

        # Update the disease in the database
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE diseases 
            SET disease_name = %s, symptoms = %s, precautions = %s, prevention_methods = %s, medication = %s
            WHERE id = %s
        """, (updated_data['disease_name'], updated_data['symptoms'], updated_data['precautions'], updated_data['prevention_methods'], updated_data['medication'], disease_id))
        mysql.connection.commit()
        cur.close()

        flash('Disease updated successfully', 'success')
        return redirect(url_for('admin_dashboard'))

    # Fetch the disease data from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM diseases WHERE id = %s", (disease_id,))
    disease = cur.fetchone()
    cur.close()

    return render_template('edit_disease.html', disease=disease)

@app.route('/admin/delete_disease/<int:disease_id>', methods=['GET', 'POST'])
def delete_disease(disease_id):
    # Check if admin is logged in
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    # Delete the disease from the database
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM diseases WHERE id = %s", (disease_id,))
    mysql.connection.commit()
    cur.close()

    flash('Disease deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    # Check if admin is logged in
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Handle form submission to add a new doctor
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO doctors (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        mysql.connection.commit()
        cur.close()

        # Redirect to admin doctors page or show success message
        return redirect(url_for('admin_doctors'))

    return render_template('add_doctor.html')



def get_doctors():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM doctors')
    doctors = cur.fetchall()
    cur.close()
    return doctors

@app.route('/admin/doctors')
def admin_doctors():
    # Check if admin is logged in
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    # Fetch doctors data from the database
    doctors = get_doctors()
    return render_template('admin_doctors.html', doctors=doctors)

from flask import request, redirect, url_for

# Function to fetch a specific doctor's data from the database
def get_doctor(doctor_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM doctors WHERE id = %s', (doctor_id,))
    doctor = cur.fetchone()
    cur.close()
    return doctor

@app.route('/admin/edit_doctor/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    # Check if admin is logged in
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    # Fetch doctor's data from the database
    doctor = get_doctor(doctor_id)

    if request.method == 'POST':
        # Handle form submission to update doctor's data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE doctors SET username = %s, email = %s, password = %s WHERE id = %s", (username, email, password, doctor_id))
        mysql.connection.commit()
        cur.close()

        # Redirect to admin doctors page or show success message
        return redirect(url_for('admin_doctors'))

    return render_template('edit_doctor.html', doctor=doctor)

@app.route('/admin/delete_doctor/<int:doctor_id>', methods=['GET', 'POST'])
def delete_doctor(doctor_id):
    # Check if admin is logged in
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    # Delete doctor's data from the database
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM doctors WHERE id = %s", (doctor_id,))
    mysql.connection.commit()
    cur.close()

    # Redirect to admin doctors page or show success message
    return redirect(url_for('admin_doctors'))



@app.route('/doctor/register', methods=['GET', 'POST'])
def register_doctor():
    if request.method == 'POST':
        # Get doctor's registration details from the form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate form data (e.g., check if passwords match, etc.)
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register_doctor'))

        # Check if the username or email already exists in the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM doctors WHERE username = %s OR email = %s", (username, email))
        existing_doctor = cur.fetchone()
        cur.close()

        if existing_doctor:
            flash('Username or email already exists', 'error')
            return redirect(url_for('register_doctor'))

        # If data is valid and no duplicate exists, register the doctor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO doctors (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        mysql.connection.commit()
        cur.close()

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('doctor_registration.html')

@app.route('/logout')
def logout():
    # Remove admin_logged_in from the session upon logout
    session.pop('admin_logged_in', None)
    # Redirect to the login page after logging out
    return redirect(url_for('login'))

@app.route('/doctor/login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username and password match with records in database
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM doctors WHERE username = %s AND password = %s', (username, password))
        doctor = cur.fetchone()
        cur.close()
        
        if doctor:
            # Set doctor_logged_in to True in the session upon successful login
            session['doctor_logged_in'] = True
            # Redirect to doctor dashboard
            return redirect(url_for('doctor_dashboard'))
        else:
            # If login unsuccessful, display error message
            flash('Invalid credentials. Please try again.', 'error')
            return redirect(url_for('doctor_login'))
    
    return render_template('doctor_login.html')


@app.route('/doctor/logout')
def doctor_logout():
    # Remove doctor_logged_in from the session upon logout
    session.pop('doctor_logged_in', None)
    # Redirect to the login page after logging out
    return redirect(url_for('doctor_login'))


@app.route('/doctor/dashboard')
def doctor_dashboard():
    # Check if doctor is logged in
    if 'doctor_logged_in' not in session:
        return redirect(url_for('doctor_login'))

    # Fetch diseases from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, disease_name FROM diseases")
    diseases = cur.fetchall()
    cur.close()

    return render_template('doctor/doctor_dashboard.html', diseases=diseases)




@app.route('/doctor/add_information/<int:disease_id>', methods=['GET', 'POST'])
def add_information(disease_id):
    if 'doctor_logged_in' not in session:
        return redirect(url_for('doctor_login'))

    if request.method == 'POST':
        doctor_name = translate_to_urdu(request.form['doctor_name'])
        doctor_advice = translate_to_urdu(request.form['doctor_advice'])
        doctor_phone = translate_to_urdu(request.form['doctor_phone'])
        precautions = translate_to_urdu(request.form['precautions'])

        # Insert the translated information into the relevant table
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO relevant_information (disease_id, doctor_name, doctor_advice, doctor_phone, precautions)
            VALUES (%s, %s, %s, %s, %s)
        """, (disease_id, doctor_name, doctor_advice, doctor_phone, precautions))
        mysql.connection.commit()
        cur.close()

        flash('Information added successfully', 'success')
        return redirect(url_for('doctor_dashboard'))

    return render_template('doctor/add_information.html', disease_id=disease_id)


if __name__ == '__main__':
    app.run(debug=True)