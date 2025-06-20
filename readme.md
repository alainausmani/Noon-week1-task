FastAPI User Authentication System

This is a basic yet complete user authentication system built using FastAPI, SQLAlchemy, Python, and JWT.
It provides functionality for:

* User registration
* User login with JWT-based authentication
* Password reset (forgot password)
* Viewing personal profile
* Editing user information
* Secure access to protected routes using JWT tokens

Step-by-Step Guide: Run the FastAPI Authentication Project

Step 1: Set Up MySQL (Workbench and XAMPP)

1. Open XAMPP and start the MySQL service.
2. Launch MySQL Workbench.
3. Create a new database for the project.

Step 2: Set Up a Python Virtual Environment

1. Open your project folder in VS Code or a terminal.
2. Create a virtual environment:
python -m venv venv
3. Activate the virtual environment:
On Windows:
venv\Scripts\activate
On macOS/Linux:
source venv/bin/activate

Step 3: Install Required Python Packages

Run the following command in the activated virtual environment:
pip install fastapi uvicorn sqlalchemy pymysql python-jose[cryptography] passlib[bcrypt] pydantic python-dotenv pytest

Step 4: Create a `.env` File

In the root of your project, create a `.env` file with the following contents:
JWT_SECRET_KEY=myverysecurekey
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

Step 5: Create Database Tables

1. Run the following command to create tables in your main database:
python create_tables.py
2. To create tables in the test database, adjust the path to use `test/auth/models/tables.py` and run the same command.

Step 6: Start the FastAPI Application

From the root directory, run the following command to launch the app:
uvicorn src.appauth.web:app --reload

Step 7: Access the API or Frontend

1. Open the Swagger UI in your browser to test the API endpoints:
   http://127.0.0.1:8000/docs
2. To use the HTML interface for registration and login, open `mainscreen.html` in a browser (preferably using "Open with Live Server" in VS Code).

Step 8: Run Tests

Run the test suite using pytest:
pytest test/auth/test_auth.py -v
