from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)

# Set a secret key for the session
app.secret_key = 'your_secret_key'

# Define user roles and functions
users = {}
jobs = {}

user_roles = {
    'User': ['start', 'stop'],
    'Management': ['view_all'],
    'Department Head': ['view_all'],
}

def check_role(role):
    return role in user_roles.get(session.get('role'), [])

# Routes

@app.route('/')
def index():
    return render_template('Index.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        user = session.get('user')
        user_jobs = jobs.get(user, [])
        return render_template('dashboard.html', user=user, user_jobs=user_jobs, check_role=check_role)
    return redirect(url_for('login'))

@app.route('/start_job', methods=['POST'])
def start_job():
    if 'user' in session:
        user = session.get('user')
        if user not in jobs:
            jobs[user] = []
        jobs[user].append({'start_time': datetime.now(), 'wo_number': request.form['wo_number']})
    return redirect(url_for('dashboard'))

@app.route('/stop_job', methods=['POST'])
def stop_job():
    if 'user' in session:
        user = session.get('user')
        if user in jobs and jobs[user]:
            jobs[user][-1]['stop_time'] = datetime.now()
    return redirect(url_for('dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        password = request.form['password']
        role = request.form['role']

        # You can add user registration logic here
        # For simplicity, we will store user details in a dictionary
        users[name] = {'department': department, 'password': password, 'role': role}
        session['user'] = name
        session['role'] = role
        return redirect(url_for('dashboard'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if name in users and users[name]['password'] == password:
            session['user'] = name
            session['role'] = users[name]['role']
            return redirect(url_for('dashboard'))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
