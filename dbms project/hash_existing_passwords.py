from flask import Flask
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbmsproj'

mysql = MySQL(app)

with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute("SELECT UserID, PasswordHash FROM user")
    users = cur.fetchall()

    for user in users:
        user_id, raw_password = user
        # Only hash if not already hashed
        if not raw_password.startswith("pbkdf2:"):
            hashed = generate_password_hash(raw_password)
            cur.execute("UPDATE user SET PasswordHash = %s WHERE UserID = %s", (hashed, user_id))
            print(f"Updated user {user_id} with hashed password.")

    mysql.connection.commit()
    cur.close()
    print("Password update complete.")
