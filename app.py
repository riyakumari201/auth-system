from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB_NAME = "users.db"
MAX_ATTEMPTS = 5
LOCK_TIME = timedelta(minutes=10)


# ---------- DATABASE ----------
def get_db():
    return sqlite3.connect(DB_NAME, timeout=10)


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                failed_attempts INTEGER DEFAULT 0,
                last_failed_login TEXT
            )
        """)
        conn.commit()


# ---------- ROUTES ----------
@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return "All fields are required"

        hashed_password = generate_password_hash(password)

        try:
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO users (email, password) VALUES (?, ?)",
                    (email, hashed_password)
                )
                conn.commit()
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            return "Email already exists"

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        with get_db() as conn:
            conn.row_factory = sqlite3.Row
            user = conn.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,)
            ).fetchone()

        if not user:
            return "Invalid email or password"

        # Convert last_failed_login
        last_failed = (
            datetime.fromisoformat(user["last_failed_login"])
            if user["last_failed_login"]
            else None
        )

        # 🔒 Check if already locked
        if user["failed_attempts"] >= MAX_ATTEMPTS:
            if last_failed and datetime.now() - last_failed < LOCK_TIME:
                return "Account locked. Try again after 10 minutes."
            else:
                # Unlock after time
                with get_db() as conn:
                    conn.execute(
                        "UPDATE users SET failed_attempts = 0 WHERE id = ?",
                        (user["id"],)
                    )
                    conn.commit()

        # ✅ Correct password
        if check_password_hash(user["password"], password):
            with get_db() as conn:
                conn.execute(
                    """
                    UPDATE users
                    SET failed_attempts = 0, last_failed_login = NULL
                    WHERE id = ?
                    """,
                    (user["id"],)
                )
                conn.commit()

            session["user_id"] = user["id"]
            session["email"] = user["email"]
            return redirect(url_for("dashboard"))

        # ❌ Wrong password → increment FIRST
        else:
            new_attempts = user["failed_attempts"] + 1

            with get_db() as conn:
                conn.execute(
                    """
                    UPDATE users
                    SET failed_attempts = ?, last_failed_login = ?
                    WHERE id = ?
                    """,
                    (new_attempts, datetime.now().isoformat(), user["id"])
                )
                conn.commit()

            if new_attempts >= MAX_ATTEMPTS:
                return "Account locked. Try again after 10 minutes."

            return "Invalid email or password"

    return render_template("login.html")



@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", email=session["email"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------- RUN ----------
if __name__ == "__main__":
    init_db()
    app.run(debug=True, threaded=False)
