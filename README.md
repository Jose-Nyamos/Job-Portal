<<<<<<< HEAD
# Job-Portal
Job recruiting app
=======
Job Portal Application

Introduction

This is a Django-based Job Portal that allows users to register as job seekers or employers. Job seekers can search and apply for jobs, while employers can post and manage job listings.

Prerequisites

Ensure you have the following installed on your system:

Python (>=3.8)

pip (Python package manager)

virtualenv (optional but recommended)

Git (if cloning from a repository)

PostgreSQL or SQLite (default Django database)

Installation Steps

Step 1: Clone the Repository

git clone <repository_url>
cd job_portal

Step 2: Create and Activate a Virtual Environment

python -m venv venv

Activate the virtual environment:

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate

Step 3: Install Dependencies

pip install -r requirements.txt

Step 4: Configure Database

By default, SQLite is used. To use PostgreSQL, update settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

Step 5: Apply Migrations

python manage.py makemigrations
python manage.py migrate

Step 6: Create a Superuser (For Admin Access)

python manage.py createsuperuser

Follow the prompts to enter username, email, and password.

Step 7: Load Initial Data (Optional)

If you have predefined data:

python manage.py loaddata initial_data.json

Step 8: Run the Development Server

python manage.py runserver

Visit http://127.0.0.1:8000/ in your browser.

Usage

Job Seekers:

Register/Login

Create & Update Profile

Search & Apply for Jobs

Employers:

Register/Login

Post Job Listings

View & Manage Applicants

Admin Access

Visit http://127.0.0.1:8000/admin/ and log in with the superuser credentials.
>>>>>>> c0deb27 (Initial commit)
