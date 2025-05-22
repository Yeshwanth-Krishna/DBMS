import MySQLdb
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
from calendar import monthrange
from datetime import date

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
        result = cur.execute("SELECT username, passwordHash, role FROM user WHERE username = %s AND role = %s",
                             (username, role))
        if result > 0:
            user = cur.fetchone()
            stored_username, stored_hash, stored_role = user
            cur.close()

            if check_password_hash(stored_hash, password):
                session['username'] = stored_username
                session['role'] = stored_role.lower()
                return redirect(url_for('dashboard1'))
            else:
                error = 'Invalid credentials.'
        else:
            cur.close()
            error = 'Invalid credentials.'

    return render_template('login.html', error=error)

@app.route('/dashboard1')
def dashboard1():
    if 'username' not in session:
        return redirect(url_for('login'))

    role = session['role']
    username = session['username']

    # Get month and year from query parameters or default to current
    try:
        month = int(request.args.get('month', 0))
        year = int(request.args.get('year', 0))
        filter_year = request.args.get('filterYear', 'All')
    except ValueError:
        month = 0
        year = 0
        filter_year = 'All'

    today = date.today()
    if month < 1 or month > 12:
        month = today.month
    if year < 1900 or year > 2100:
        year = today.year

    start_day, total_days = monthrange(year, month)
    days_in_month = list(range(1, total_days + 1))

    cur = mysql.connection.cursor()
    if filter_year == 'All':
        cur.execute("""
            SELECT EventID, EventName AS name, DATE(EventDate) AS date, EventTime AS time, Venue AS venue, Description AS description, Year
            FROM event
            WHERE MONTH(EventDate) = %s AND YEAR(EventDate) = %s
        """, (month, year))
    else:
        # Remove 'Year ' prefix from filter_year before converting to int
        year_filter_value = filter_year.replace('Year ', '').strip()
        if year_filter_value.lower() == 'all':
            # If 'All' is selected, do not filter by year
            cur.execute("""
                SELECT EventID, EventName AS name, DATE(EventDate) AS date, EventTime AS time, Venue AS venue, Description AS description, Year
                FROM event
                WHERE MONTH(EventDate) = %s AND YEAR(EventDate) = %s
            """, (month, year))
        else:
            try:
                year_filter_int = int(year_filter_value)
            except ValueError:
                year_filter_int = None  # or handle error as needed

            if year_filter_int is not None:
                cur.execute("""
                    SELECT EventID, EventName AS name, DATE(EventDate) AS date, EventTime AS time, Venue AS venue, Description AS description, Year
                    FROM event
                    WHERE MONTH(EventDate) = %s AND YEAR(EventDate) = %s AND Year = %s
                """, (month, year, year_filter_int))
            else:
                # If conversion failed, fallback to no filter or handle accordingly
                cur.execute("""
                    SELECT EventID, EventName AS name, DATE(EventDate) AS date, EventTime AS time, Venue AS venue, Description AS description, Year
                    FROM event
                    WHERE MONTH(EventDate) = %s AND YEAR(EventDate) = %s
                """, (month, year))
    rows = cur.fetchall()
    cur.close()

    # Group events by day
    events_by_day = {}
    for row in rows:
        event_id, name, date_obj, time, venue, description, year_val = row
        date_key = date_obj.strftime('%Y-%m-%d')  # Use full date as key
        if date_key not in events_by_day:
            events_by_day[date_key] = []

    # Fix for time being timedelta instead of time object
        if hasattr(time, 'strftime'):
            time_str = time.strftime('%H:%M')
        else:
            total_seconds = time.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            time_str = f"{hours:02d}:{minutes:02d}"

        events_by_day[date_key].append({
            'EventID': event_id,
            'name': name,
            'time': time_str,
            'venue': venue,
            'description': description,
            'year': year_val
        })

    return render_template('dashboard1.html',
                           username=username,
                           role=role,
                           start_day=start_day,
                           days_in_month=days_in_month,
                           events_by_day=events_by_day,
                           month=month,
                           year=year,
                           filter_year=filter_year)
@app.route('/add_event', methods=['POST'])
def add_event():
    if 'username' not in session or session['role'] not in ['faculty', 'admin']:
        flash("You do not have permission to add events.", "danger")
        return redirect(url_for('dashboard1'))

    name = request.form['event']
    date = request.form['date']
    time = request.form['time']
    venue = request.form['venue']
    description = request.form['description']
    year = request.form.get('year')  # get year from form
    created_by = session.get('username')  # get current logged-in user

    # semester field is received but not used in DB, ignoring for now

    print(f"DEBUG add_event: name={name}, date={date}, time={time}, venue={venue}, description={description}, year={year}, created_by={created_by}")

    if not date:
        flash("Event date is required.", "danger")
        return redirect(url_for('dashboard1'))

    # Convert 'All' or invalid year to None before insert
    if year == 'All' or not year or not year.isdigit():
        year_value = None
    else:
        try:
            # Remove 'Year ' prefix if present before converting to int
            year_cleaned = year.replace('Year ', '').strip()
            if year_cleaned.lower() == 'all':
                year_value = None
            else:
                year_value = int(year_cleaned)
        except ValueError:
            year_value = None

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO event (EventName, EventDate, EventTime, Venue, Description, Year, CreatedBy) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (name, date, time, venue, description, year_value, created_by))
    mysql.connection.commit()
    cur.close()

    flash("Event added successfully!", "success")
    return redirect(url_for('dashboard1'))

@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    if 'username' not in session or session['role'] not in ['faculty', 'admin']:
        flash("You do not have permission to delete events.", "danger")
        return redirect(url_for('dashboard1'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM event WHERE EventID = %s", (event_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('dashboard1'))

@app.route('/edit_event', methods=['POST'])
def edit_event():
    if 'username' not in session or session['role'] not in ['faculty', 'admin']:
        flash("You do not have permission to edit events.", "danger")
        return redirect(url_for('dashboard1'))

    event_id = request.form.get('event_id')
    name = request.form['event']
    date = request.form['date']
    time = request.form['time']
    venue = request.form['venue']
    description = request.form['description']
    year = request.form.get('year')

    if not event_id:
        flash("Event ID is required for editing.", "danger")
        return redirect(url_for('dashboard1'))

    if not date:
        flash("Event date is required.", "danger")
        return redirect(url_for('dashboard1'))

    # Convert 'All' or invalid year to None before update
    if year == 'All' or not year or not year.isdigit():
        year_value = None
    else:
        try:
            year_cleaned = year.replace('Year ', '').strip()
            if year_cleaned.lower() == 'all':
                year_value = None
            else:
                year_value = int(year_cleaned)
        except ValueError:
            year_value = None

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE event
        SET EventName = %s, EventDate = %s, EventTime = %s, Venue = %s, Description = %s, Year = %s
        WHERE EventID = %s
    """, (name, date, time, venue, description, year_value, event_id))
    mysql.connection.commit()
    cur.close()

    flash("Event updated successfully!", "success")
    return redirect(url_for('dashboard1'))
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('forbidden'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT username AS name, username AS email, role FROM user")
    users = cur.fetchall()
    cur.close()
    return render_template('admin_dashboard.html', users=users)

@app.route('/faculty_dashboard')
def faculty_dashboard():
    if 'username' not in session or session.get('role') != 'faculty':
        return redirect(url_for('forbidden'))
    username = session['username']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT EventName, EventDate, EventTime, Venue, Description, Year
        FROM event
        WHERE CreatedBy = %s
        ORDER BY EventDate DESC, EventTime DESC
    """, (username,))
    rows = cur.fetchall()
    cur.close()

    # Convert EventTime timedelta to string for template
    events = []
    for row in rows:
        event = dict(row)
        time_val = event.get('EventTime')
        if hasattr(time_val, 'strftime'):
            event['EventTime'] = time_val.strftime('%H:%M')
        elif time_val is not None:
            total_seconds = time_val.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            event['EventTime'] = f"{hours:02d}:{minutes:02d}"
        else:
            event['EventTime'] = ''
        events.append(event)

    return render_template('faculty_dashboard.html', username=username, events=events)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.errorhandler(403)
def forbidden(_):
    return render_template('403.html'), 403

if __name__ == "__main__":
    app.run(debug=True)
