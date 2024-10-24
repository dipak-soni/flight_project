# Shaan-AI-OCR

Shaan-AI-OCR is a Python-based OCR (Optical Character Recognition) application designed to recognize and extract text from images or PDFs. This project is built using Django and requires Python 3.10 or higher.

## Project Setup

### 1. Python Version

Ensure you have Python 3.10 or higher installed. You can verify the Python version by running the following command:

```bash
python3 --version
```

### 2. Vertual Environment

Create a virtual environment to isolate project dependencies:
```bash
python3 -m venv venv
```
after this you need to activate the virtual environment

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

Install the required dependencies from the requirements.txt file:


```bash
pip install -r requirements.txt
```

### 4. Create .env file

Create a .env file in the project's root directory and add the following environment variables:\n

here for this project we need to add only 1 variable and that is OPENAI_API_KEY, Here is the example of .env file

```bash
OPENAI_API_KEY = your_api_key
```



### 5. Run the Application

Start the Django development server by running the following command:
```bash
python3 manage.py runserver
```

### 6. Access the Application

Open your web browser and visit http://127.0.0.1:8000/ to access the OCR application.
or open your server link address in your browser




#### Thank You






