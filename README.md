# PythonDoctorProject_final  

A web‑based platform that connects patients with doctors, enables disease information management, and provides an admin interface for overseeing the entire system. The project showcases a full‑stack Python solution with web crawling capabilities for populating medical data.

---  

## Overview  

`PythonDoctorProject_final` is a Flask application that allows:

* **Patients** to browse doctors, view disease details, and submit inquiries.  
* **Doctors** to register, log in, and manage their own profile and medical information.  
* **Admins** to add/edit doctors and diseases, and to monitor platform activity.  

The repository also contains a crawling module that can scrape medical data from external sources, which can be used to populate the disease database automatically.

---  

## Features  

| Category | Description |
|----------|-------------|
| **User Management** | Doctor registration & login, patient view‑only access, admin authentication. |
| **Disease Catalog** | Add, edit, and delete disease entries with descriptions and symptoms. |
| **Doctor Dashboard** | Doctors can update their personal information and view patient queries. |
| **Admin Dashboard** | Centralised view of all doctors, disease entries, and system statistics. |
| **Web Crawling** | Scripts (`auto.py`, `crawl.py`) to fetch disease data from public websites. |
| **Responsive Templates** | Clean HTML templates using a shared base layout for consistency. |
| **Data Persistence** | SQLite (or any DB supported by SQLAlchemy) for storing doctors, diseases, and user credentials. |

---  

## Tech Stack  

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.x, Flask, SQLAlchemy |
| **Frontend** | HTML5, CSS3 (Bootstrap optional), Jinja2 templating |
| **Data Storage** | SQLite (default) – can be swapped for PostgreSQL/MySQL |
| **Web Crawling** | `requests`, `BeautifulSoup4` |
| **Version Control** | Git (GitHub) |
| **Packaging** | ZIP/RAR archives for source distribution (`CFC-UHRS_finalcode.zip`, `Prototype.rar`) |

---  

## Installation  

1. **Clone the repository**  

   ```bash
   git clone https://github.com/yourusername/PythonDoctorProject_final.git
   cd PythonDoctorProject_final
   ```

2. **Create a virtual environment**  

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**  

   The project uses Flask and a few common libraries. If a `requirements.txt` file is missing, you can install the core packages manually:

   ```bash
   pip install Flask SQLAlchemy requests beautifulsoup4
   ```

4. **Set up environment variables**  

   Create a `.env` file (or export variables in your shell) with at least the following:

   ```env
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=YOUR_OWN_SECRET_KEY
   ```

   > **Note:** Replace `YOUR_OWN_SECRET_KEY` with a strong random string.

5. **Initialize the database**  

   ```bash
   flask db init      # If using Flask-Migrate (optional)
   flask db migrate
   flask db upgrade
   ```

   *If you are not using Flask‑Migrate, simply run the provided script to create the SQLite DB:*

   ```bash
   python app.py --init-db
   ```

---  

## Usage  

### Run the application  

```bash
flask run
```

The server will start at `http://127.0.0