"""
Database configuration and models for the High School Activities API
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./school_activities.db")

# Create database engine
engine = create_engine(DATABASE_URL, echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


class Activity(Base):
    """Activity model representing an extracurricular activity"""
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    schedule = Column(String(200), nullable=False)
    max_participants = Column(Integer, nullable=False)
    
    # Relationship to participants
    participants = relationship("Participant", back_populates="activity", cascade="all, delete-orphan")


class Participant(Base):
    """Participant model representing a student signed up for an activity"""
    __tablename__ = "participants"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    
    # Relationship to activity
    activity = relationship("Activity", back_populates="participants")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all tables in the database"""
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except SQLAlchemyError as e:
        print(f"Error creating database tables: {e}")
        raise


def init_sample_data():
    """Initialize database with sample data"""
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Activity).first():
            print("Sample data already exists, skipping initialization")
            return
            
        # Sample activities data
        sample_activities = [
            {
                "name": "Chess Club",
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
            },
            {
                "name": "Programming Class",
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20,
                "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
            },
            {
                "name": "Gym Class",
                "description": "Physical education and sports activities",
                "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                "max_participants": 30,
                "participants": ["john@mergington.edu", "olivia@mergington.edu"]
            },
            {
                "name": "Soccer Team",
                "description": "Join the school soccer team and compete in matches",
                "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
                "max_participants": 22,
                "participants": ["liam@mergington.edu", "noah@mergington.edu"]
            },
            {
                "name": "Basketball Team",
                "description": "Practice and play basketball with the school team",
                "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 15,
                "participants": ["ava@mergington.edu", "mia@mergington.edu"]
            },
            {
                "name": "Art Club",
                "description": "Explore your creativity through painting and drawing",
                "schedule": "Thursdays, 3:30 PM - 5:00 PM",
                "max_participants": 15,
                "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
            },
            {
                "name": "Drama Club",
                "description": "Act, direct, and produce plays and performances",
                "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
                "max_participants": 20,
                "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
            },
            {
                "name": "Math Club",
                "description": "Solve challenging problems and participate in math competitions",
                "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
                "max_participants": 10,
                "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
            },
            {
                "name": "Debate Team",
                "description": "Develop public speaking and argumentation skills",
                "schedule": "Fridays, 4:00 PM - 5:30 PM",
                "max_participants": 12,
                "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
            }
        ]
        
        # Create activities and participants
        for activity_data in sample_activities:
            # Create activity
            activity = Activity(
                name=activity_data["name"],
                description=activity_data["description"],
                schedule=activity_data["schedule"],
                max_participants=activity_data["max_participants"]
            )
            db.add(activity)
            db.flush()  # Flush to get the ID
            
            # Create participants
            for email in activity_data["participants"]:
                participant = Participant(
                    email=email,
                    activity_id=activity.id
                )
                db.add(participant)
        
        db.commit()
        print("Sample data initialized successfully")
        
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error initializing sample data: {e}")
        raise
    finally:
        db.close()