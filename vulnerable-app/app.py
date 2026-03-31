# =============================================================================
# MediCare Portal - Patient Management System
# WARNING: THIS APPLICATION IS INTENTIONALLY VULNERABLE FOR TRAINING PURPOSES
# DO NOT DEPLOY THIS IN A REAL ENVIRONMENT
# =============================================================================

from flask import Flask, request, jsonify, render_template_string
import sqlite3
import subprocess
import os
import yaml

app = Flask(__name__)

# =============================================================================
# VULNERABILITY 1: HARDCODED SECRETS
# These should NEVER be in code. They should live in environment variables
# or a secrets manager like AWS Secrets Manager or Azure Key Vault.
# Any scanner (Gitleaks, Truffleog) will immediately flag these.
# =============================================================================
SECRET_KEY = "super_secret_key_12345"
DATABASE_PASSWORD = "MediCare_DB_Pass_2024!"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
API_KEY = "sk-medicareportal-live-abc123def456"

# Database connection helper
def get_db():
    conn = sqlite3.connect('hospital.db')
    return conn


# =============================================================================
# HOME PAGE
# =============================================================================
@app.route('/')
def home():
    return render_template_string('''
    <html>
    <head><title>MediCare Portal</title></head>
    <body style="font-family:Arial; padding:40px; background:#f0f4f8">
        <h1 style="color:#2c5282">🏥 MediCare Patient Portal</h1>
        <p>Internal staff portal for patient record management.</p>
        <h3>Available Endpoints (for testing):</h3>
        <ul>
            <li><a href="/login?username=admin&password=admin123">/login</a> - Staff login</li>
            <li><a href="/patients">/patients</a> - View all patients</li>
            <li><a href="/patient?id=1">/patient?id=1</a> - View specific patient</li>
            <li><a href="/search?name=John">/search?name=John</a> - Search patients</li>
            <li><a href="/read-file?filename=requirements.txt">/read-file</a> - Read server files</li>
            <li><a href="/ping?host=localhost">/ping</a> - Network diagnostics</li>
        </ul>
    </body>
    </html>
    ''')


# =============================================================================
# VULNERABILITY 2: SQL INJECTION in login
# The username input is pasted directly into the SQL query with no sanitisation.
# An attacker can type:   ' OR '1'='1   as the username to bypass login entirely.
# The safe version uses parameterised queries: WHERE username=? AND password=?
# and passes values separately so the database never treats them as code.
# =============================================================================
@app.route('/login')
def login():
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    
    conn = get_db()
    c = conn.cursor()
    
    # VULNERABLE: string is built by joining user input directly into SQL
    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
    
    print(f"[DEBUG] Executing query: {query}")  # Also bad - logging sensitive queries
    
    try:
        c.execute(query)
        user = c.fetchone()
        if user:
            return jsonify({
                "status": "Login successful",
                "user_id": user[0],
                "username": user[1],
                "role": user[3],
                "message": "Welcome to MediCare Portal"
            })
        else:
            return jsonify({"status": "Login failed", "message": "Invalid credentials"}), 401
    except Exception as e:
        # VULNERABILITY: Exposing raw database errors to the user
        return jsonify({"error": str(e), "query": query}), 500
    finally:
        conn.close()


# =============================================================================
# VULNERABILITY 3: SENSITIVE DATA EXPOSURE
# This endpoint returns ALL patient records to ANYONE who calls it.
# There is no authentication check — no "are you logged in?" verification.
# A real endpoint would check a session token or JWT before returning data.
# =============================================================================
@app.route('/patients')
def get_patients():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM patients")
    patients = c.fetchall()
    conn.close()
    
    # Returns full records including NHS numbers and diagnoses with zero auth
    return jsonify({
        "total_patients": len(patients),
        "patients": [
            {
                "id": p[0],
                "name": p[1],
                "date_of_birth": p[2],
                "diagnosis": p[3],
                "nhs_number": p[4]
            } for p in patients
        ]
    })


# =============================================================================
# VULNERABILITY 4: ANOTHER SQL INJECTION (numeric parameter)
# The id parameter is put directly into the query.
# An attacker can input: 1 UNION SELECT username,password,role,null,null FROM users
# This would return the entire users table instead of just one patient.
# =============================================================================
@app.route('/patient')
def get_patient():
    patient_id = request.args.get('id', '')
    
    conn = get_db()
    c = conn.cursor()
    
    # VULNERABLE: no input validation, no parameterisation
    query = f"SELECT * FROM patients WHERE id={patient_id}"
    
    try:
        c.execute(query)
        patient = c.fetchone()
        conn.close()
        if patient:
            return jsonify({
                "id": patient[0],
                "name": patient[1],
                "dob": patient[2],
                "diagnosis": patient[3],
                "nhs_number": patient[4]
            })
        else:
            return jsonify({"error": "Patient not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =============================================================================
# VULNERABILITY 5: SQL INJECTION in search
# Same pattern - raw string concatenation into SQL
# Attack: search for   %' UNION SELECT username,password,role,null,null FROM users--
# =============================================================================
@app.route('/search')
def search_patients():
    name = request.args.get('name', '')
    
    conn = get_db()
    c = conn.cursor()
    
    # VULNERABLE
    query = "SELECT * FROM patients WHERE name LIKE '%" + name + "%'"
    
    try:
        c.execute(query)
        results = c.fetchall()
        conn.close()
        return jsonify({
            "query_used": query,  # Also bad - never expose your SQL queries
            "results": [{"id": r[0], "name": r[1], "diagnosis": r[2]} for r in results]
        })
    except Exception as e:
        return jsonify({"error": str(e), "query": query}), 500


# =============================================================================
# VULNERABILITY 6: PATH TRAVERSAL
# The filename parameter is used directly to open files on the server.
# An attacker can request:  /read-file?filename=../../etc/passwd
# On Linux/Mac this would attempt to read the system password file.
# The safe version would validate the filename against an allowed list.
# =============================================================================
@app.route('/read-file')
def read_file():
    filename = request.args.get('filename', '')
    
    # VULNERABLE: no validation of what directory the file is in
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return jsonify({
            "filename": filename,
            "content": content
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =============================================================================
# VULNERABILITY 7: COMMAND INJECTION
# The host parameter is passed directly to a shell command (ping).
# An attacker can input:  localhost; cat /etc/passwd
# The semicolon ends the ping command and starts a new one.
# subprocess.run() with shell=True is almost always dangerous with user input.
# =============================================================================
@app.route('/ping')
def ping_host():
    host = request.args.get('host', 'localhost')
    
    # VULNERABLE: shell=True + user input = command injection
    result = subprocess.run(
        f"ping -c 2 {host}",
        shell=True,
        capture_output=True,
        text=True
    )
    
    return jsonify({
        "host": host,
        "output": result.stdout,
        "errors": result.stderr
    })


# =============================================================================
# VULNERABILITY 8: INSECURE YAML DESERIALISATION
# yaml.load() without Loader=yaml.SafeLoader can execute arbitrary Python code.
# An attacker sending crafted YAML can run any command on your server.
# The fix is simply: yaml.safe_load(data) instead of yaml.load(data)
# =============================================================================
@app.route('/import-config', methods=['POST'])
def import_config():
    data = request.data.decode('utf-8')
    
    # VULNERABLE: yaml.load without SafeLoader
    try:
        config = yaml.load(data, Loader=yaml.Loader)
        return jsonify({"status": "Config imported", "config": str(config)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # VULNERABILITY: Debug mode ON in production exposes a live Python console
    app.run(debug=True, host='0.0.0.0', port=5000)