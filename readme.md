This is a simple user authentication system built with FastAPI, SQLAlchemy, Python and JWT.  
It allows users to register, log in, Set up new password incase of forget password , edit personal information , view personal information and receive a JWT token for secure access to protected routes.

Step-by-Step: Run the FastAPI Authentication Project

STEP 1: Set Up MySQL (Workbench + XAMPP)

1.Open XAMPP and start MySQL.
2.Open MySQL Workbench.
3.Create a new database 

STEP 2: Set Up Python Virtual Environment

1.Open your project folder in VS Code or terminal.
2.Create a virtual environment: "python -m venv venv"
3.Activate the virtual environment:
Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate

STEP 3: Install All Required Packages

1.Run this in your activated virtual environment:"pip install fastapi uvicorn sqlalchemy pymysql python-jose[cryptography] passlib[bcrypt] pydantic python-dotenv pytest"

STEP 4: Create .env File

1.In your project root, create a .env file:
JWT_SECRET_KEY=myverysecurekey
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

STEP 5: Create Database Tables

1.Run this command to create the tables in MySQL from your model: "python create_tables.py"
2.Run this command again to create tables of testing Database by changing the routes to test->auth->models->tables.py

STEP 6: Start the FastAPI App

1.Inside the root directory, run the app with Uvicorn: "uvicorn src.appauth.web:app --reload"

STEP 7: Use the API or Frontend

1.On google search Swagger UI:http://127.0.0.1:8000/docs 

Register & Login HTML forms:
2.Open mainscreen.html through open with live server

STEP 8: Run Tests
1.run command : "pytest test/auth/test_auth.py -v"