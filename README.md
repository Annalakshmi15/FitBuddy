# FitBuddy – AI Fitness Plan Generator using Gemini Models

FitBuddy is a FastAPI web application that generates a personalized
7-day general wellness workout plan using Google's Gemini models.

The application also provides a short nutrition/recovery tip and allows
the user to submit feedback to generate an updated workout plan.

## Features

- FastAPI backend
- SQLite database
- SQLAlchemy database operations
- Pydantic input validation
- Gemini AI workout generation
- Gemini Flash nutrition/recovery tip
- Feedback-based workout plan update
- HTML/Jinja2 frontend
- View all stored users and plans
- Environment variable based API key configuration

## Project Structure

FitBuddy/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── schemas.py
│   ├── routes.py
│   │
│   └── ai/
│       ├── __init__.py
│       ├── gemini_client.py
│       ├── gemini_generator.py
│       ├── gemini_flash_generator.py
│       └── updated_plan.py
│
├── templates/
│   ├── index.html
│   ├── result.html
│   └── all_users.html
│
├── static/
│   └── style.css
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

## Requirements

Install:

- Python 3.11 or newer
- Internet connection
- Gemini API key
- VS Code

## Installation

Open the FitBuddy folder in VS Code.

Open the VS Code terminal.

Create a virtual environment:

Windows PowerShell:

    python -m venv .venv

Activate it:

    .venv\Scripts\Activate.ps1

If PowerShell blocks activation, use:

    .venv\Scripts\activate.bat

Install packages:

    pip install -r requirements.txt

## Environment Configuration

Create a file named:

    .env

Add:

    APP_NAME=FitBuddy
    DATABASE_URL=sqlite:///./fitbuddy.db
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY
    GEMINI_MODEL=gemini-3.8-flash
    GEMINI_FLASH_MODEL=gemini-3.8-flash

Replace YOUR_GEMINI_API_KEY with your real Gemini API key.

Never upload the .env file to GitHub.

## Run the Application

Make sure the virtual environment is active.

Run:

    uvicorn app.main:app --reload

You should see a message similar to:

    Uvicorn running on http://127.0.0.1:8000

Open:

    http://127.0.0.1:8000

## API Documentation

FastAPI automatically provides Swagger documentation.

Open:

    http://127.0.0.1:8000/docs

## Main Routes

GET /

Displays the main FitBuddy form.

POST /generate-workout

Receives user information and generates:

- 7-day workout plan
- Nutrition/recovery tip

GET /view-all-users

Displays users and saved plans.

POST /submit-feedback

Receives feedback and generates an updated plan.

## Database

The SQLite database file is automatically created when the
application starts.

Database file:

    fitbuddy.db

The application creates the required table automatically.

## Safety

FitBuddy is a general wellness application.

It does not provide:

- Medical diagnosis
- Medical treatment
- Extreme dieting
- Starvation recommendations
- Dangerous exercise instructions
- Calorie restriction targets
- Supplement recommendations
- Unrealistic transformation promises

## Troubleshooting

### Python command not found

Install Python and restart VS Code.

Then check:

    python --version

### Virtual environment does not activate

Try:

    .venv\Scripts\activate.bat

Or open a new VS Code terminal.

### ModuleNotFoundError

Make sure the virtual environment is active.

Then run:

    pip install -r requirements.txt

### GEMINI_API_KEY missing

Check that:

1. The file is named exactly .env
2. It is inside the FitBuddy folder
3. GEMINI_API_KEY has been entered
4. There are no quotation marks required around the key

Example:

    GEMINI_API_KEY=your_key_here

Restart the FastAPI server after changing .env.

### Gemini model error

Check the Gemini model name in .env.

The default configuration uses:

    GEMINI_MODEL=gemini-3.8-flash
    GEMINI_FLASH_MODEL=gemini-3.8-flash

### Page not found

Make sure the server is running:

    uvicorn app.main:app --reload

Then open:

    http://127.0.0.1:8000

### CSS is not loading

Make sure:

    static/style.css

exists and the application was started from the FitBuddy project root.

Correct command:

    uvicorn app.main:app --reload

### Database error

Stop the server and start it again.

The application automatically creates the database table during startup.

## Project Flow

User
   |
   v
index.html
   |
   v
/ generate-workout
   |
   +----> Pydantic validation
   |
   +----> Gemini workout generator
   |
   +----> Gemini Flash nutrition/recovery tip
   |
   v
SQLite
   |
   v
result.html
   |
   v
User feedback
   |
   v
/submit-feedback
   |
   v
Original plan + feedback
   |
   v
Gemini updated_plan
   |
   v
SQLite
   |
   v
Updated result.html

## Development

Start the application with:

    uvicorn app.main:app --reload

Stop the application with:

    CTRL + C