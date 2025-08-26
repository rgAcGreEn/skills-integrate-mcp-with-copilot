# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities

## Getting Started

1. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Configure the database (optional):
   
   By default, the application uses SQLite for development. To use MySQL:
   - Create a MySQL database: `CREATE DATABASE school_activities;`
   - Update the `.env` file with your MySQL connection string
   
3. Run the application:

   ```
   python app.py
   ```
   
   The application will automatically create the database tables and populate them with sample data on first startup.

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |

## Data Model

The application uses SQLAlchemy ORM with automatic table creation and supports both SQLite (development) and MySQL (production):

1. **Activities** - Stored in `activities` table:

   - id (Primary Key)
   - name (Unique activity name)
   - description
   - schedule
   - max_participants (Maximum number of participants allowed)

2. **Participants** - Stored in `participants` table:
   - id (Primary Key)
   - email (Student email address)
   - activity_id (Foreign Key to activities table)

The application automatically creates tables and initializes sample data on startup. Data persists between server restarts.
