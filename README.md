# Secure Authentication System (Flask)

A secure login system built with Flask that implements
password hashing, failed login attempt tracking, and
temporary account lockout to mitigate brute-force attacks.

## Features
- Secure password hashing
- Failed login attempt tracking
- Account lockout after multiple failed attempts
- Automatic unlock after time-based validation
- User feedback using flash messages

## Tech Stack
- Python
- Flask
- SQLite
- HTML/CSS

## How to Run
```bash
pip install -r requirements.txt
python app.py
