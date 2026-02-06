from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

# connect to database
def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# create users table (run once)
conn = get_db_connection()
conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
conn.commit()
conn.close()

@app.route("/")
def home():
    return "Welcome to Auth System"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
            conn.close()
            return "Registration successful!"
        except sqlite3.IntegrityError:
            return "User already exists!"

    return '''
        <h2>Register</h2>
        <form method="post">
            Username: <input name="username"><br><br>
            Password: <input type="password" name="password"><br><br>
            <button type="submit">Register</button>
        </form>
    '''

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            return "Login successful!"
        return "Invalid credentials"

    return '''
        <h2>Login</h2>
        <form method="post">
            Username: <input name="username"><br><br>
            Password: <input type="password" name="password"><br><br>
            <button type="submit">Login</button>
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
