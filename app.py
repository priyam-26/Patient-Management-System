from flask import Flask, request, jsonify, render_template
import psycopg
import os
import math
import re

app = Flask(__name__)

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db_connection():
    DATABASE_URL = os.environ.get("DATABASE_URL")

    if not DATABASE_URL:
        raise Exception("DATABASE_URL is not set")

    conn = psycopg.connect(DATABASE_URL)
    return conn

# -----------------------------
# INIT DATABASE
# -----------------------------
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id SERIAL PRIMARY KEY,
            patient_number TEXT UNIQUE,
            name TEXT,
            phone TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# -----------------------------
# HOME PAGE
# -----------------------------
@app.route('/')
def home():
    return render_template('index.html')

# -----------------------------
# ADD PATIENT
# -----------------------------
@app.route('/add', methods=['POST'])
def add_patient():
    data = request.get_json()

    patient_number = data.get('patient_number')
    name = data.get('name')
    phone = data.get('phone')

    # Required field validation
    if not patient_number or not patient_number.strip():
        return jsonify({"message": "Patient number is required"})

    if not name or not name.strip():
        return jsonify({"message": "Patient name is required"})

    # Phone validation (optional)
    if phone:
        if not re.match(r'^(?:\+91|91)?\d{10}$', phone):
            return jsonify({"message": "Invalid Indian phone number"})

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO patients (patient_number, name, phone) VALUES (%s, %s, %s)",
            (patient_number, name, phone)
        )
        conn.commit()
        message = "Patient added successfully"

    except psycopg.errors.UniqueViolation:
        conn.rollback()
        message = "Patient number already exists"

    except Exception:
        conn.rollback()
        message = "Something went wrong"

    finally:
        conn.close()

    return jsonify({"message": message})

# -----------------------------
# SEARCH PATIENT
# -----------------------------
@app.route('/search', methods=['GET'])
def search_patient():
    patient_number = request.args.get('patient_number')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM patients WHERE patient_number = %s",
        (patient_number,)
    )
    patient = cursor.fetchone()

    conn.close()

    if patient:
        return jsonify({
            "found": True,
            "patient": {
                "id": patient[0],
                "patient_number": patient[1],
                "name": patient[2],
                "phone": patient[3]
            }
        })
    else:
        return jsonify({"found": False})

# -----------------------------
# GET ALL PATIENTS (PAGINATION)
# -----------------------------
@app.route('/patients', methods=['GET'])
def get_patients():
    page = int(request.args.get('page', 1))
    per_page = 5

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM patients")
    total = cursor.fetchone()[0]

    total_pages = math.ceil(total / per_page) if total > 0 else 1
    offset = (page - 1) * per_page

    cursor.execute(
        "SELECT * FROM patients ORDER BY id DESC LIMIT %s OFFSET %s",
        (per_page, offset)
    )
    patients = cursor.fetchall()

    conn.close()

    return jsonify({
        "patients": [
            {
                "id": p[0],
                "patient_number": p[1],
                "name": p[2],
                "phone": p[3]
            } for p in patients
        ],
        "total_pages": total_pages
    })

# -----------------------------
# DELETE PATIENT
# -----------------------------
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_patient(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM patients WHERE id = %s", (id,))
    conn.commit()

    deleted = cursor.rowcount
    conn.close()

    if deleted:
        return jsonify({"message": "Patient deleted successfully"})
    else:
        return jsonify({"message": "Patient not found"})

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == '__main__':
    app.run()