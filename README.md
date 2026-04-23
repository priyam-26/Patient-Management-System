# 🏥 Patient Management System

A clean and responsive web-based application for managing patient records.
Designed for doctors or small clinics to quickly add, search, view, and delete patient information.

---

## 🚀 Live Overview

This system replaces manual record-keeping with a simple digital interface:

- Add patient details
- Search instantly by patient number
- View paginated patient list
- Delete records with confirmation
- Works across mobile and desktop

---

## 🧠 Features

- 🔍 **Search Patient** by unique patient number
- ➕ **Add Patient** with validation
- ❌ **Delete Patient** (from table or search result)
- 📄 **Pagination** for large datasets
- 📱 **Responsive UI** (mobile-friendly)
- 🇮🇳 **Indian Phone Number Validation**
- ⚡ **Instant UI updates (no page reloads)**

---

## 🛠️ Tech Stack

**Backend**

- Python (Flask)

**Database**

- PostgreSQL

**Frontend**

- HTML (Jinja Templates)
- CSS (Responsive Design)
- JavaScript (Vanilla JS)

**Deployment**

- Render

---

## 📁 Project Structure

```bash
project/
│
├── app.py
├── requirements.txt
├── Procfile
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
```

---

## ⚙️ Setup & Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/priyam-26/Patient-Management-System.git
cd Patient-Management-System
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Set Environment Variable

**Linux / Mac:**

```bash
export DATABASE_URL=your_postgresql_url
```

**Windows (CMD):**

```bash
set DATABASE_URL=your_postgresql_url
```

---

### 4. Run the application

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## 🗄️ Database

- Uses PostgreSQL for persistent storage
- Table: `patients`

```sql
id SERIAL PRIMARY KEY
patient_number TEXT UNIQUE
name TEXT
phone TEXT
```

---

## 🔐 Validation Rules

- Patient number → Required
- Name → Required
- Phone → Optional
- Indian phone format supported:
  - 10-digit number → `9876543210`
  - With country code → `919876543210`
  - With +91 → `+919876543210`

---

## 🌐 Deployment

This app is designed to be deployed on **Render**.

### Required:

- `Procfile`
- `requirements.txt`
- Environment variable:

  ```
  DATABASE_URL
  ```

---

## ⚠️ Notes

- App uses PostgreSQL placeholders (`%s`) for queries
- Backend handles all validation securely
- Frontend communicates via REST APIs

---

## 🔗 Frontend Reference

The UI is built using a clean layout with dynamic rendering via JavaScript.
A simplified version of the UI structure can be seen here:

---

## 👨‍💻 Author

Developed by **Priyam Prabhat**

---

## 📌 Future Improvements

- ✏️ Edit/Update patient records
- 🔐 Authentication system (doctor login)
- 📊 Dashboard analytics
- ☁️ Multi-user SaaS version

---

## ⭐

If you find this project nice, you can give it a ⭐ on GitHub!
