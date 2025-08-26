"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import os
from pathlib import Path

from database import get_db, create_tables, init_sample_data, Activity, Participant

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    """Initialize database and create tables on startup"""
    create_tables()
    init_sample_data()

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities(db: Session = Depends(get_db)):
    """Get all activities with their participants"""
    activities = db.query(Activity).all()
    
    # Transform to the same format as before
    result = {}
    for activity in activities:
        result[activity.name] = {
            "description": activity.description,
            "schedule": activity.schedule,
            "max_participants": activity.max_participants,
            "participants": [p.email for p in activity.participants]
        }
    
    return result


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Sign up a student for an activity"""
    # Find the activity
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check if student is already signed up
    existing_participant = db.query(Participant).filter(
        Participant.email == email,
        Participant.activity_id == activity.id
    ).first()
    
    if existing_participant:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Check if activity is full
    current_participants = db.query(Participant).filter(Participant.activity_id == activity.id).count()
    if current_participants >= activity.max_participants:
        raise HTTPException(
            status_code=400,
            detail="Activity is full"
        )

    # Add student
    participant = Participant(email=email, activity_id=activity.id)
    db.add(participant)
    db.commit()
    
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Unregister a student from an activity"""
    # Find the activity
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Find the participant
    participant = db.query(Participant).filter(
        Participant.email == email,
        Participant.activity_id == activity.id
    ).first()

    if not participant:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    db.delete(participant)
    db.commit()
    
    return {"message": f"Unregistered {email} from {activity_name}"}
