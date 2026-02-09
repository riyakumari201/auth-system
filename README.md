Flask Authentication System

A secure Flask-based authentication system that allows users to register, log in, access protected routes, and log out using session-based authentication, hashed passwords, and SQLite database.

This project demonstrates backend fundamentals, security best practices, and real-world authentication flow.

Features

User Registration with secure password hashing

User Login with credential verification

Session-based authentication

Protected routes (only logged-in users can access)

Logout functionality

SQLite database integration

Flash messages for user feedback

Clean and simple authentication flow

🛠 Tech Stack

Backend: Flask (Python)

Database: SQLite

Security: Werkzeug password hashing

Session Management: Flask sessions

Version Control: Git & GitHub

📂 Project Structure
auth-system/
│
├── app.py          # Main Flask application
├── users.db        # SQLite database
├── README.md       # Project documentation
└── requirements.txt (optional)