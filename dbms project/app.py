from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv
import os
from calendar import monthrange
from datetime import date
import mysql.connector

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.getenv("DB_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("DB_NAME")

mysql = MySQL(app)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        role = request.form['role'].strip().lower()

        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE username = %s", (username,))
        existing = cur.fetchone()
        if existing:
            flash('Username already exists. Please choose a different one.', 'danger')
            cur.close()
            return redirect(url_for('signup'))

        cur.execute("INSERT INTO user (username, passwordHash, role) VALUES (%s, %s, %s)",
                    (username, hashed_password, role))
        mysql.connection.commit()
        cur.close()

        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        role = request.form['role'].strip().lower()

        cur = mysql.connection.cursor()
        result = cur.execute("SELECT Username, PasswordHash, Role FROM user WHERE Username = %s AND Role = %s",
                             (username, role))
        if result > 0:
            user = cur.fetchone()
            stored_username, stored_hash, stored_role = user
            cur.close()

            if check_password_hash(stored_hash, password):
                session['username'] = stored_username
                session['role'] = stored_role.lower()
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid credentials.'
        else:
            cur.close()
            error = 'Invalid credentials.'

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    role = session['role']
    username = session['username']

    # Current month and year
    today = date.today()
    year = today.year
    month = today.month
    start_day, total_days = monthrange(year, month)

    days_in_month = list(range(1, total_days + 1))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT EventName AS name, DATE(EventDate) AS date, EventTime AS time, Venue AS venue, Description AS description
        FROM event
        WHERE MONTH(EventDate) = %s AND YEAR(EventDate) = %s
    """, (month, year))
    rows = cur.fetchall()
    cur.close()

    # Group events by day
    events_by_day = {}
    for row in rows:
        name, date_obj, time, venue, description = row
        day = date_obj.day
        day_str = str(day)
        if day_str not in events_by_day:
            events_by_day[day_str] = []
        events_by_day[day_str].append({
            'name': name,
            'time': time.strftime('%H:%M'),
            'venue': venue,
            'description': description
        })

    return render_template('dashboard.html',
                           username=username,
                           role=role,
                           start_day=start_day,
                           days_in_month=days_in_month,
                           events_by_day=events_by_day)


@app.route('/add_event', methods=['POST'])
def add_event():
    if 'username' not in session or session['role'] == 'student':
        return redirect(url_for('login'))

    name = request.form['event']
    date = request.form['date']
    time = request.form['time']
    venue = request.form['venue']
    description = request.form['description']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO event (name, date, time, venue, description, created_by) VALUES (%s, %s, %s, %s, %s, %s)",
                (name, date, time, venue, description, session['username']))
    mysql.connection.commit()
    cur.close()

    flash("Event added successfully!", "success")
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

if __name__ == '__main__':
    app.run(debug=True)
