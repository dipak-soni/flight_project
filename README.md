
# Shaan-AI-OCR

Shaan-AI-OCR is a Python-based OCR (Optical Character Recognition) application built with Django, designed to recognize and extract text from images or PDFs. This application requires Python 3.10 or higher.



## Project Setup
### 1. Install Python
Ensure you have Python 3.10 or higher installed. Verify the Python version by running:

bash
```bash
  python3 --version
```

### 2. Set Up a Virtual Environment
Create a virtual environment to isolate project dependencies:

```bash
  python3 -m venv venv
```

### 3. Install Dependencies
Install the required dependencies from the requirements.txt file:

bash
```bash
  pip install -r requirements.txt
```

### 4. Create a .env File
In the project's root directory, create a .env file and add the following environment variables:

```bash
# OpenAI API Key
OPENAI_API_KEY='Your openai api key'

# Database Configuration
DB_NAME='Your database name'
DB_USER='Your Database Username'
DB_PASSWORD='Database Password'
DB_HOST='endpoint'
DB_PORT='port number'

# Django Settings
SECRET_KEY='django-insecure-v0zwt049=r5le$c+!j9^qx(*un#-wjqz^a!3hd##vwc$pgqtb5'
POST_API_URL=''

# Allowed Origins
TRUSTED_ORIGIN=''
ALLOWED_HOSTS=''
```

### 5. Set Up the Database
Run migrations to set up the database schema. Apply all migrations by running the following commands:

```bash
python manage.py migrate
python manage.py migrate --database=mysql
```
### 6. Run the Application
To start the Django application:

For local development: Run the following command:

```bash

python manage.py runserver
```
Access the application locally at http://127.0.0.1:8000.

For production use: Start the application with Waitress or Gunicorn

```bash

python -m waitress --host=0.0.0.0 --port=8000 --threads=4 home.wsgi:application

waitress-serve --host=0.0.0.0 --port=8000 --thresds=4 home.wsgi:application  (If first one does not work)
```
### 7. Access the Application

Local development: Open your browser and go to http://127.0.0.1:8000.

Production: Use the deployed server’s URL.

Thank you! Enjoy using Shaan-AI-OCR for your OCR needs.

